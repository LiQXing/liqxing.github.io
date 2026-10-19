# 光影推荐：个人网站的电影推荐子页面

GitHub Pages 入口：<https://liqxing.github.io/movie-recommender/>。

已连接的云端应用：<https://liqxingappio-ijwrtfv4rdappamp4ns8pe.streamlit.app/>。

页面通过 iframe 嵌入公开的 Streamlit 应用。GitHub Pages 提供静态子页面，Python 推荐推理运行在 Streamlit Community Cloud。两者需要分别发布；仅推送仓库不会创建云端 Python 应用。

## 第一次部署

1. 登录 <https://share.streamlit.io/>，连接自己的 GitHub 账号，点击 **Create app**，选择已有应用。
2. 填写仓库 `LiQXing/liqxing.github.io`、分支 `main`、入口文件 `movie-recommender/streamlit_app.py`。
3. 在 Advanced settings 选择 **Python 3.13**。应用无需 secrets、Spark 或 Java。
4. 点击 Deploy，等待安装依赖和首次数据准备。将应用设为 **公开**，访问应用，确认能推荐电影。
5. 将生成的真实 `https://xxx.streamlit.app/` 地址填入同目录 `app-config.json` 的 `appUrl`，例如 `{"appUrl":"https://你的实际子域名.streamlit.app/"}`，提交到 main。
6. 打开 GitHub Pages 入口，界面将自动嵌入。若嵌入加载受网络或浏览器限制，点击“独立窗口打开”。

`appUrl` 已配置为上方的云端应用地址。以后更换应用地址时，修改该字段即可；设为 null 时页面会显示“云端应用待部署”。

## 功能

- 输入已有用户 ID：复用 Spark ALS 训练得到的用户向量和电影向量，过滤用户全部已评分电影，返回 Top 10；未知用户使用热门电影兜底。
- 选择喜欢的电影：将选择视为 4.5 分，固定电影向量，通过正则化最小二乘求临时偏好向量，推荐下一部，并支持“换一部”和类型筛选。
- 中文译名、原名核对、CSV 导出、评分分析、模型评估。中文译名仅覆盖人工整理的常见电影，其余保留原名。

## 数据、模型与资源

数据来自 [GroupLens MovieLens 25M](https://grouplens.org/datasets/movielens/25m/)，原始数据使用条件见[官方 README](https://files.grouplens.org/datasets/movielens/ml-25m-README.html)。本仓库提供训练好的 ALS 参数、按电影聚合的统计和评估结果，不上传原始评分、完整电影目录或逐用户历史。

首次启动从 GroupLens 官方下载约 262 MB ZIP，校验 MD5 `6b51fb2759a8657d3bfcbfc42b592ada`。随后流式生成全部 25,000,095 条评分的紧凑历史索引，以及电影目录，存入服务器临时目录。CSV 按每批 250,000 行处理，不将整个评分表载入内存；完成后删除下载 ZIP，保留约 220 MB 服务数据。重启或云端临时目录重置后可能需要重新下载。下载依赖云端能够访问 GroupLens。

原始训练实验使用 Windows、Spark 4.0.1、rank=16；云端只进行 NumPy 推理。“原始训练实验环境与数据来源”展示训练时的配置，不代表托管服务器硬件。

本应用用于课程学习、研究演示，不接入商业付费功能。引用数据集请注明：F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems 5, 4, Article 19. https://doi.org/10.1145/2827872。

## 本地运行此发布版

```powershell
python -m pip install -r movie-recommender/requirements.txt
python -m streamlit run movie-recommender/streamlit_app.py
```

本地首次运行同样会下载官方数据。离线原项目仍可使用原有 `app.py`，无需改动。

参考：[部署应用](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)、[嵌入公开应用](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app/embed-your-app)。
