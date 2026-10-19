"""Prepare serving data from the original GroupLens download, without Spark.

Raw MovieLens records are never stored in this public repository. The official
archive is verified and streamed into a private, ephemeral server-side cache.
"""
from pathlib import Path
import hashlib
import json
import logging
import shutil
import time
import zipfile

import certifi
import numpy as np
import pandas as pd
import requests

SOURCE_URL = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
SOURCE_MD5 = "6b51fb2759a8657d3bfcbfc42b592ada"
SOURCE_SHA256 = "8b21cfb7eb1706b4ec0aac894368d90acf26ebdfb6aced3ebd4ad5bd1eb9c6aa"
SCHEMA_VERSION = 1


def download_archive(archive, report=lambda value, text: None):
    """Verify TLS with the publisher's current chain, then pin release bytes."""
    archive = Path(archive)
    # The publisher currently uses a newer emSign/InCommon chain which some
    # Linux CA stores cannot build. Keep normal roots and add the CA-published
    # chain only for this fixed GroupLens download. Never use verify=False.
    chain = Path(__file__).resolve().parent / "certificates/grouplens-chain.pem"
    bundle = archive.parent / "grouplens-ca-bundle.pem"
    bundle.write_bytes(Path(certifi.where()).read_bytes() + b"\n" + chain.read_bytes())
    for attempt in range(3):
        checksum = hashlib.sha256()
        try:
            with requests.get(SOURCE_URL, stream=True, timeout=(20, 120), verify=str(bundle)) as response:
                response.raise_for_status()
                if not response.url.startswith("https://files.grouplens.org/"):
                    raise ValueError("Unexpected official dataset download redirect")
                total = int(response.headers.get("Content-Length", 261978986))
                received = 0
                with archive.open("wb") as output:
                    for block in response.iter_content(1024 * 1024):
                        if not block:
                            continue
                        output.write(block)
                        checksum.update(block)
                        received += len(block)
                        report(min(.49, .49 * received / total), "�������عٷ��Ƽ����ݡ�")
            if checksum.hexdigest() != SOURCE_SHA256:
                raise ValueError("MovieLens download SHA256 mismatch; please retry")
            return
        except requests.RequestException:
            archive.unlink(missing_ok=True)
            if attempt == 2:
                raise
            logging.warning("GroupLens download attempt %s failed; retrying", attempt + 1, exc_info=True)
            report(0., "����Դ������ʱ�жϣ��������ԡ�")
            time.sleep(2 ** attempt)
        except Exception:
            archive.unlink(missing_ok=True)
            raise


def build_data(archive, target, assets, report=lambda value, text: None):
    """Stream the verified archive; memory use is bounded by one CSV chunk."""
    target, assets = Path(target), Path(assets)
    target.mkdir(parents=True, exist_ok=True)
    stats = json.loads((assets / "dataset_stats.json").read_text(encoding="utf-8"))
    size = int(stats["clean_rows"])
    with zipfile.ZipFile(archive) as release:
        with release.open("ml-25m/movies.csv") as source:
            catalog = pd.read_csv(source)
        aggregates = pd.read_csv(assets / "movie_statistics.csv")
        catalog = catalog.merge(aggregates, on="movieId", how="left", validate="one_to_one")
        catalog["train_count"] = catalog.train_count.fillna(0).astype("int64")
        catalog.sort_values("movieId").to_csv(target / "catalog.csv", index=False)
        (target / "MOVIELENS_README.txt").write_bytes(release.read("ml-25m/README.txt"))
        items = np.lib.format.open_memmap(target / "history_items.npy", mode="w+", dtype="int32", shape=(size,))
        ratings = np.lib.format.open_memmap(target / "history_ratings.npy", mode="w+", dtype="float32", shape=(size,))
        counts, offset, previous = {}, 0, -1
        try:
            with release.open("ml-25m/ratings.csv") as source:
                for chunk in pd.read_csv(source, usecols=["userId", "movieId", "rating"],
                                         dtype={"userId": "int32", "movieId": "int32", "rating": "float32"},
                                         chunksize=250_000):
                    users = chunk.userId.to_numpy()
                    if users[0] < previous or np.any(users[1:] < users[:-1]):
                        raise ValueError("Unexpected MovieLens user ordering")
                    previous = int(users[-1])
                    end = offset + len(chunk)
                    if end > size:
                        raise ValueError("Unexpected MovieLens record count")
                    items[offset:end] = chunk.movieId
                    ratings[offset:end] = chunk.rating
                    ids, frequencies = np.unique(users, return_counts=True)
                    for uid, count in zip(ids, frequencies):
                        counts[int(uid)] = counts.get(int(uid), 0) + int(count)
                    offset = end
                    report(.5 + .48 * offset / size, f"����׼���Ƽ����� {offset / size:.0%}")
            if offset != size or len(counts) != int(stats["users"]):
                raise ValueError("MovieLens record count does not match the trained release")
            items.flush()
            ratings.flush()
        finally:
            # Flush and close the mappings before publishing the ready marker.
            items._mmap.close()
            ratings._mmap.close()
        users = np.array(sorted(counts), dtype="int32")
        offsets = np.r_[0, np.cumsum([counts[int(u)] for u in users], dtype="int64")]
        np.savez_compressed(target / "history_index.npz", user_ids=users, offsets=offsets)
    for source in assets.iterdir():
        if source.is_file() and source.name not in {"movie_statistics.csv", "popular_statistics.csv"}:
            shutil.copy2(source, target / source.name)
    popular = pd.read_csv(assets / "popular_statistics.csv")
    popular = popular.merge(catalog[["movieId", "title", "genres"]], on="movieId", validate="one_to_one")
    popular.to_csv(target / "popular_movies.csv", index=False)


def ensure_assets(assets, target, report=lambda value, text: None):
    assets, target = Path(assets), Path(target)
    marker = target / "ready.json"
    expected = {"schema": SCHEMA_VERSION, "dataset_md5": SOURCE_MD5, "dataset_sha256": SOURCE_SHA256}
    required = ["als_factors.npz", "catalog.csv", "history_index.npz", "history_items.npy",
                "history_ratings.npy", "metrics.json", "dataset_stats.json", "popular_movies.csv",
                "rating_distribution.csv", "genre_stats.csv", "tuning.json", "environment.json"]
    if marker.exists() and json.loads(marker.read_text()) == expected and all((target / p).exists() for p in required):
        return target
    target.mkdir(parents=True, exist_ok=True)
    archive = target / "movielens-download.zip"
    report(0., "�״����������ڴ� GroupLens ׼���Ƽ����ݣ����Ժ�")
    download_archive(archive, report)
    build_data(archive, target, assets, report)
    archive.unlink()
    temporary = marker.with_suffix(".tmp")
    temporary.write_text(json.dumps(expected), encoding="utf-8")
    temporary.replace(marker)
    report(1., "�Ƽ������Ѿ���")
    return target
