"""Run with: python -m streamlit run app.py"""
from pathlib import Path
from html import escape
import json
import tempfile
import requests
from cloud_bootstrap import ensure_assets
import pandas as pd
import streamlit as st
from recommender import MovieRecommender
from localization import GENRES_ZH, chinese_genres, display_title, with_chinese_titles

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title="光影推荐 · Spark ALS", page_icon="🎬", layout="wide")
st.markdown("""<style>
.stApp {background:#0c1220;color:#e6edf7}
h1,h2,h3 {letter-spacing:-.02em}
[data-testid="stSidebar"] {background:#141d30}
.film {padding:20px 0;border-bottom:1px solid #29344a;min-height:120px}
.film .rank {font-size:13px;color:#6fe0ce;letter-spacing:2px}
.film .title {font-size:21px;font-weight:650;margin:7px 0}
.film .original {font-size:13px;color:#a4b3c9;margin:0 0 9px;line-height:1.5}
.film .genre {font-size:13px;color:#a4b3c9}
.film .score {font-size:13px;color:#6fe0ce;margin-top:8px}
</style>""",unsafe_allow_html=True)
st.title("光影推荐")
st.caption("基于 Spark MLlib ALS 的电影推荐系统 · MovieLens 25M · 在线推荐")
@st.cache_resource(show_spinner=False)
def prepare_cloud_data():
    # This release includes the current GroupLens CA chain and a SHA256 pin.
    progress = st.progress(0., text="正在准备推荐数据…")
    try:
        return ensure_assets(ROOT / "model", Path(tempfile.gettempdir()) / "liqxing-movielens25m-v1",
                             lambda value, text: progress.progress(value, text=text))
    finally:
        progress.empty()

try:
    ARTIFACTS = prepare_cloud_data()
except Exception as exc:
    import logging
    logging.exception("MovieLens cloud preparation failed")
    if isinstance(exc, requests.exceptions.SSLError):
        st.error("官方数据源的证书验证未通过，请将下方故障标识发给站点维护者。")
    elif isinstance(exc, (requests.exceptions.Timeout, requests.exceptions.ConnectionError)):
        st.error("暂时无法连接官方数据源，自动重试后仍未成功。请稍后重试。")
    else:
        st.error("推荐数据准备失败，请将下方故障标识发给站点维护者。")
    st.caption(f"故障标识：{type(exc).__name__} · 服务版本：20261019.2")
    if st.button("重新准备数据"):
        st.cache_resource.clear()
        st.rerun()
    st.stop()

required=["metrics.json","als_factors.npz","catalog.csv","history_index.npz","history_items.npy","history_ratings.npy"]
if any(not (ARTIFACTS/f).exists() for f in required):
    st.info("请先运行 python download_data.py，再运行 python train.py 生成模型和实验结果。")
    st.stop()

@st.cache_resource
def load_engine():
    return MovieRecommender(ARTIFACTS)

engine=load_engine()
metrics=engine.metrics
with st.sidebar:
    st.header("已有用户演示")
    st.caption("以下设置用于「按用户 ID 推荐」页。选片推荐无需用户 ID。")
    user_id=st.number_input("用户 ID",min_value=1,max_value=2_147_483_647,value=1,step=1)
    method=st.radio("推荐方式",["ALS 个性化推荐","热门电影基线"])
    all_genres=sorted(set(g for s in engine.catalog.genres.dropna() for g in s.split("|") if g!="(no genres listed)"))
    genre=st.selectbox("电影类型",["全部类型"]+all_genres,format_func=lambda g:GENRES_ZH.get(g,g))
    st.caption("可尝试用户 1、2、100。输入 999999 可展示新用户兜底。")
    st.caption("已评分电影会被过滤。仅展示训练集中至少有 50 条评分的电影。")

def load_selection_example():
    st.session_state["liked_movie_ids"]=[2571,79132,109487]
    st.session_state["next_movie_genre"]="跟随所选电影"

def skip_current_movie(movie_id):
    st.session_state["next_movie_skipped"].append(int(movie_id))

@st.cache_data
def selection_options():
    # Use well-observed, learned films, ordered by popularity for easy discovery.
    choices=engine.catalog.loc[engine.movie_ids]
    choices=choices[choices.train_count>=metrics["protocol"]["min_item_ratings"]]
    choices=choices.sort_values(["train_count","movieId"],ascending=[False,True])
    ids=[int(mid) for mid in choices.index]
    labels={int(mid):(f"{display_title(mid,row.title)} · {row.title} · ID {mid}" if display_title(mid,row.title)!=row.title else f"{row.title} · ID {mid}") for mid,row in choices.iterrows()}
    return ids,labels

tabs=st.tabs(["选电影找下一部","按用户 ID 推荐","评分与电影分析","模型评估"])
with tabs[0]:
    st.subheader("下一部看什么？")
    st.write("选几部你喜欢的电影，推荐一部接下来值得看的。无需填写用户 ID。")
    options,labels=selection_options()
    liked=st.multiselect("选择你喜欢的电影",options=options,format_func=lambda mid:labels[mid],key="liked_movie_ids",max_selections=20,placeholder="搜索中文或英文片名，可选择多部")
    st.caption("可以先选 3–5 部；已选影片会自动从推荐结果中排除。")
    st.button("试试科幻电影组合",on_click=load_selection_example,key="selection_example")
    guest_genre=st.selectbox("下一部电影类型",["跟随所选电影","全部类型"]+all_genres,format_func=lambda g:GENRES_ZH.get(g,g),key="next_movie_genre")
    context=(tuple(sorted(liked)),guest_genre)
    if st.session_state.get("next_movie_context")!=context:
        st.session_state["next_movie_context"]=context
        st.session_state["next_movie_skipped"]=[]
        st.session_state["next_movie_started"]=False
    if st.button("推荐下一部",type="primary",disabled=not liked,key="suggest_next"):
        st.session_state["next_movie_skipped"]=[]
        st.session_state["next_movie_started"]=True
    if not liked:
        st.info("先选择你喜欢的电影，或试试上面的科幻组合。")
    elif not st.session_state["next_movie_started"]:
        st.caption(f"已选择 {len(liked)} 部电影，点击「推荐下一部」查看结果。")
    else:
        next_recs=with_chinese_titles(engine.recommend_from_movies(liked,k=6,genre=None if guest_genre in ["跟随所选电影","全部类型"] else guest_genre,exclude_movie_ids=st.session_state["next_movie_skipped"],match_selected_genres=guest_genre=="跟随所选电影"))
        if next_recs.empty:
            st.info("当前类型没有更多符合条件的电影，请更换类型或重新推荐。")
        else:
            row=next_recs.iloc[0]
            title=row.title_zh or row.title
            original=row.title if row.title_zh else "暂未收录可靠中文译名"
            st.markdown("### 为你推荐下一部")
            st.markdown(f'<div class="film"><div class="rank">下一部 / 电影 {int(row.movieId)}</div><div class="title">{escape(str(title))}</div><div class="original">{escape(str(original))}</div><div class="genre">{escape(chinese_genres(row.genres))}</div><div class="score">预测评分（参考） {row.score:.2f}</div></div>',unsafe_allow_html=True)
            st.caption(f"根据你选的 {len(liked)} 部电影生成，已排除所选影片及本轮跳过的影片。预测分数不是喜欢的概率。")
            if next_recs.attrs.get("preferred_genres"):
                st.caption("本次优先匹配类型："+"、".join(GENRES_ZH.get(g,g) for g in next_recs.attrs["preferred_genres"]))
            st.button("换一部",on_click=skip_current_movie,args=(int(row.movieId),),key="another_movie")
            with st.expander("再看看其他备选电影"):
                alternatives=next_recs.iloc[1:][["movieId","title_zh","title","genres"]].copy()
                alternatives["genres"]=alternatives.genres.map(chinese_genres)
                st.dataframe(alternatives.rename(columns={"movieId":"电影 ID","title_zh":"中文片名","title":"原始片名","genres":"类型"}),hide_index=True,width="stretch")
            download=next_recs.rename(columns={"title_zh":"中文片名","title":"原始片名","genres":"原始类型"})
            st.download_button("下载本次选片推荐",download.to_csv(index=False).encode("utf-8-sig"),file_name="my_next_movies.csv",mime="text/csv")
    with st.expander("这些推荐如何根据我的选择生成？"):
        st.write("将你选中的电影视为喜欢的电影，利用已训练的电影向量估计本次偏好，再给其他候选电影打分。默认优先匹配所选电影的共同类型，也可以选择全部类型。更换选择后会重新计算。本次选择保留在当前会话，不会改写数据集用户的评分记录。")
with tabs[1]:
    recs,strategy=engine.recommend(int(user_id),method="als" if method.startswith("ALS") else "popular",genre=None if genre=="全部类型" else genre)
    recs=with_chinese_titles(recs)
    history=with_chinese_titles(engine.history(int(user_id)))
    a,b,c=st.columns(3)
    a.metric("历史评分",f"{len(history):,}")
    b.metric("本次推荐",len(recs))
    c.metric("推荐策略",strategy)
    st.subheader(f"用户 {user_id} 的电影清单")
    if strategy=="新用户热门兜底":
        st.info("这个用户没有训练评分记录，当前根据训练集评分次数推荐热门电影。")
    if not len(recs):
        st.info("当前类型没有符合条件且未评分的电影，请选择其他类型。")
    cols=st.columns(2)
    for i,row in recs.iterrows():
        score=(f"ALS 预测评分 {row['score']:.2f}" if strategy=="ALS 个性化推荐" else f"训练集评分 {int(row['train_count']):,} 次")
        title=row["title_zh"] or row["title"]
        original=row["title"] if row["title_zh"] else "暂未收录可靠中文译名"
        with cols[i%2]:
            st.markdown(f'<div class="film"><div class="rank">{int(row["rank"]):02d} / 电影 {int(row["movieId"])}</div><div class="title">{escape(str(title))}</div><div class="original">{escape(str(original))}</div><div class="genre">{escape(chinese_genres(row["genres"]))}</div><div class="score">{score}</div></div>',unsafe_allow_html=True)
    st.caption("优先展示常用中文译名，英文原名保留供核对；暂未收录译名的电影显示原名。")
    st.caption("ALS 分数是未截断的显式评分预测值，可能超出 0.5–5.0；分数不是喜欢的概率。")
    export=recs.rename(columns={"title_zh":"中文片名","title":"原始片名","genres":"原始类型"})
    st.download_button("下载推荐清单",export.to_csv(index=False).encode("utf-8-sig"),file_name=f"recommendations_user_{user_id}.csv",mime="text/csv")
    with st.expander("查看该用户评分历史与类型偏好"):
        if len(history):
            shown=history.sort_values(["rating","movieId"],ascending=[False,True]).head(30)
            shown=shown[["movieId","title_zh","title","rating","genres"]].rename(columns={"movieId":"电影 ID","title_zh":"中文片名","title":"原始片名","rating":"评分","genres":"类型"})
            shown["类型"]=shown["类型"].map(chinese_genres)
            st.dataframe(shown,hide_index=True,width="stretch")
            prefs=history.assign(genre=history.genres.fillna("").str.split("|")).explode("genre").groupby("genre").agg(评分次数=("rating","size"),平均评分=("rating","mean")).sort_values("评分次数",ascending=False)
            prefs.index=prefs.index.map(lambda g:GENRES_ZH.get(g,g));prefs.index.name="电影类型"
            st.dataframe(prefs,width="stretch")
            st.caption("多类型电影会在每个所属类型中计入一次；该偏好仅用于解释展示。")
with tabs[2]:
    stats=json.loads((ARTIFACTS/"dataset_stats.json").read_text(encoding="utf-8"))
    a,b,c=st.columns(3)
    a.metric("真实评分",f"{stats['clean_rows']:,}");b.metric("用户",f"{stats['users']:,}");c.metric("有评分电影",f"{stats['rated_movies']:,}")
    st.caption("本页统计使用全部原始评分进行探索分析。训练、调参与评估另行按时间划分。")
    a,b=st.columns(2)
    with a:
        st.subheader("热门电影 Top 15")
        popular=pd.read_csv(ARTIFACTS/"popular_movies.csv").head(15)
        popular["title"]=[display_title(mid,title) for mid,title in zip(popular.movieId,popular.title)]
        st.bar_chart(popular.set_index("title")["ratings"],horizontal=True)
    with b:
        st.subheader("评分分布")
        st.bar_chart(pd.read_csv(ARTIFACTS/"rating_distribution.csv").set_index("rating"))
    st.subheader("用户群体的类型偏好")
    genre_stats=pd.read_csv(ARTIFACTS/"genre_stats.csv")
    genre_stats["genre"]=genre_stats["genre"].map(lambda g:GENRES_ZH.get(g,g))
    st.dataframe(genre_stats.rename(columns={"genre":"电影类型","ratings":"评分次数","mean_rating":"平均评分"}),hide_index=True,width="stretch")
with tabs[3]:
    st.subheader("同一测试集上的评分预测")
    reg=metrics["regression"]
    st.dataframe(pd.DataFrame([{"模型":m,"RMSE":reg[m]["rmse"],"MAE":reg[m]["mae"],"评分数":reg[m]["n"]} for m in ["ALS","ItemMean","GlobalMean"]]),hide_index=True,width="stretch")
    st.caption(f"按每个用户的评分时间划分训练/验证/测试为 80%/10%/10%，仅验证集选择参数。测试评分预测覆盖率 {reg['test_coverage']:.2%}。各回归基线使用相同的可预测评分行。")
    st.subheader("未评分电影的 Top 10 推荐")
    rank=metrics["ranking"]
    st.dataframe(pd.DataFrame([{"方法":m,"Precision@10":rank[m]["precision_at_10"],"Recall@10":rank[m]["recall_at_10"],"NDCG@10":rank[m]["ndcg_at_10"],"评估用户":rank[m]["users"]} for m in ["ALS","Popular"]]),hide_index=True,width="stretch")
    st.caption(f"固定 {rank['ALS']['users']} 名具备可评估正样本的用户，正样本为测试集中评分至少 4 分的电影。对全部 {rank['candidate_movies']:,} 部训练评分数至少 50 的电影排序，逐用户过滤训练和验证历史，两种方法使用相同候选集。")
    st.caption("上述指标对应已有用户的离线实验；新增的选片推荐使用临时偏好向量，尚未单独进行离线准确率评估。")
    st.warning("未评分电影不等于不喜欢。上述离线指标是历史数据上的实验结果，不能直接解释为线上点击率或所有用户的满意度。")
    st.subheader("验证集参数选择")
    st.dataframe(pd.read_json(ARTIFACTS/"tuning.json"),hide_index=True,width="stretch")
    with st.expander("原始训练实验环境与数据来源"):
        st.caption("以下为模型离线训练时的环境，云端仅运行推荐推理。")
        st.json(json.loads((ARTIFACTS/"environment.json").read_text(encoding="utf-8")))
        st.markdown("数据来源：[GroupLens MovieLens 25M](https://grouplens.org/datasets/movielens/25m/)；算法文档：[Spark ALS](https://spark.apache.org/docs/4.0.1/ml-collaborative-filtering.html)")
