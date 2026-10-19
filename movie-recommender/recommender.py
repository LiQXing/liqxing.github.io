"""Exact dot-product inference from factors learned by Spark MLlib ALS.

Serving does not require Spark or Java. It uses the same user/item factors.
"""
from pathlib import Path
import json
from numbers import Integral
from collections import Counter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent

def top_k(scores, movie_ids, k=10):
    """Deterministic descending order, with movie ID as tie breaker."""
    scores = np.asarray(scores)
    finite = np.flatnonzero(np.isfinite(scores))
    if not len(finite):
        return finite
    k = min(k, len(finite))
    # Partition once, then include ties at the boundary before sorting.
    cutoff = np.partition(scores[finite], len(finite) - k)[len(finite) - k]
    shortlist = finite[scores[finite] >= cutoff]
    return shortlist[np.lexsort((movie_ids[shortlist], -scores[shortlist]))][:k]

class MovieRecommender:
    def __init__(self, artifacts=None):
        self.path = Path(artifacts or ROOT / "artifacts")
        f = np.load(self.path / "als_factors.npz")
        self.user_ids, self.user_factors = f["user_ids"], f["user_factors"]
        self.movie_ids, self.item_factors = f["movie_ids"], f["item_factors"]
        self.catalog = pd.read_csv(self.path / "catalog.csv").set_index("movieId")
        self.history_index = np.load(self.path / "history_index.npz")
        self.history_items = np.load(self.path / "history_items.npy", mmap_mode="r")
        self.history_ratings = np.load(self.path / "history_ratings.npy", mmap_mode="r")
        self.metrics = json.loads((self.path / "metrics.json").read_text(encoding="utf-8"))

    def history(self, user_id):
        users = self.history_index["user_ids"]
        pos = np.searchsorted(users, user_id)
        if pos == len(users) or users[pos] != user_id:
            return pd.DataFrame(columns=["movieId", "rating", "title", "genres"])
        a, b = self.history_index["offsets"][pos:pos+2]
        h = pd.DataFrame({"movieId": self.history_items[a:b], "rating": self.history_ratings[a:b]})
        return h.join(self.catalog[["title", "genres"]], on="movieId")

    def recommend(self, user_id, k=10, method="als", genre=None):
        ids = self.movie_ids
        c = self.catalog.reindex(ids)
        history = self.history(user_id)
        eligible = (c["train_count"].fillna(0).to_numpy() >= self.metrics["protocol"]["min_item_ratings"])
        eligible &= ~np.isin(ids, history.movieId.to_numpy())
        if genre:
            eligible &= c.genres.fillna("").str.split("|").apply(lambda gs: genre in gs).to_numpy()
        upos = np.searchsorted(self.user_ids, user_id)
        known = upos < len(self.user_ids) and self.user_ids[upos] == user_id
        strategy = "ALS 个性化推荐" if known and method == "als" else "热门电影推荐"
        if method == "als" and not known:
            strategy = "新用户热门兜底"
        scores = self.item_factors @ self.user_factors[upos] if known and method == "als" else c.train_count.fillna(0).to_numpy(dtype=float)
        scores = np.where(eligible, scores, -np.inf)
        ix = top_k(scores, ids, k)
        result = c.iloc[ix].reset_index()
        result["score"] = scores[ix]
        result.insert(0, "rank", np.arange(1, len(result)+1))
        return result, strategy

    def recommend_from_movies(self, liked_movie_ids, k=10, genre=None, exclude_movie_ids=(), match_selected_genres=True):
        """Fold in a temporary user from liked films with the item factors fixed.

        A selection is interpreted as an explicit 4.5 rating. Solve the user
        least-squares update with the saved model's ALS-WR regularization:
        (Q.T Q + regParam * n * I) p = Q.T r. This does not change the trained
        model or any dataset user's history. Skip selected and dismissed films.
        """
        selections = list(liked_movie_ids)
        if any(isinstance(mid, bool) or not isinstance(mid, Integral) for mid in selections):
            raise ValueError("电影 ID 必须为整数。")
        selections = sorted(set(int(mid) for mid in selections))
        if not 1 <= len(selections) <= 20:
            raise ValueError("请选择 1–20 部喜欢的电影。")
        if isinstance(k, bool) or not isinstance(k, Integral) or k < 1:
            raise ValueError("推荐数量必须为正整数。")
        positions = np.searchsorted(self.movie_ids, selections)
        in_range = positions < len(self.movie_ids)
        if not in_range.all() or not np.array_equal(self.movie_ids[positions], selections):
            raise ValueError("所选电影没有可用的模型向量，请从列表中重新选择。")

        selected_factors = self.item_factors[positions].astype(np.float64)
        reg = float(self.metrics["selected_model"]["regParam"])
        lhs = selected_factors.T @ selected_factors
        lhs += reg * len(selections) * np.eye(selected_factors.shape[1])
        rhs = selected_factors.T @ np.full(len(selections), 4.5)
        temporary_user = np.linalg.solve(lhs, rhs)

        ids = self.movie_ids
        catalog = self.catalog.reindex(ids)
        eligible = catalog.train_count.fillna(0).to_numpy() >= self.metrics["protocol"]["min_item_ratings"]
        eligible &= ~np.isin(ids, selections + list(exclude_movie_ids))
        preferred_genres = []
        if genre:
            eligible &= catalog.genres.fillna("").str.split("|").apply(lambda gs: genre in gs).to_numpy()
        elif match_selected_genres:
            support = Counter(g for gs in self.catalog.loc[selections, "genres"].fillna("") for g in set(gs.split("|")) if g not in ["", "IMAX", "(no genres listed)"])
            strongest = max(support.values(), default=0)
            # Only constrain the list when at least 60% of selections share
            # a theme. Tied strongest themes are allowed; mixed tastes stay broad.
            if strongest >= .6 * len(selections):
                preferred_genres = sorted(g for g, count in support.items() if count == strongest)
                eligible &= catalog.genres.fillna("").str.split("|").apply(lambda gs:bool(set(gs) & set(preferred_genres))).to_numpy()
        scores = self.item_factors @ temporary_user
        indices = top_k(np.where(eligible, scores, -np.inf), ids, int(k))
        result = catalog.iloc[indices].reset_index()
        result["score"] = scores[indices]
        result.insert(0, "rank", np.arange(1, len(result) + 1))
        result.attrs["preferred_genres"] = preferred_genres
        return result
