# LiQXing 的独立博客

网站：[https://liqxing.github.io/](https://liqxing.github.io/)

文章来源：[LiQXing 的博客园](https://www.cnblogs.com/LiQXing/)。已迁移公开归档中的 **33 篇文章**（2023–2026），保留标题、发布日期、正文、代码和公式。博客园原站未做删除或修改。

## 美化与功能

- 依据用户提供的 SimpleMemory v2 配置与凌云_void v5.7 CSS 重新实现静态布局，保留 Long Cang 手写标题、全屏头图、半透明阅读区、侧栏、昼夜切换与点击诗句和粒子效果。
- 原配置的头图数组为空、侧栏图片返回 404，使用原主题附带的首页和文章页默认背景。
- 音乐保留网易云歌单 `7002443469`，使用原 APlayer、Meting 和指定原地址的 `v3.js`。第三方接口不可用时仍可通过网易云歌单链接打开。自动播放受浏览器策略影响。
- 文章独立页、归档、分类、全文搜索、分页、代码高亮与复制、目录、图片放大、RSS、站点地图。
- 分类按原文标题整理，原站没有公开的自定义分类列表。

## 迁移情况

31 张原始文章图片已保存为本地文件。另有 **9 个原始图片不可获取**（8 个 URL 返回 403/404，1 个返回“已过期”占位图），文章中保留来源链接并显示原图不可用提示，没有替换为其他图片。具体地址见 `content/migration-report.json` 的 `mediaFailures`。

正文和元数据位于 `content/posts.json`，迁移清单位于 `content/migration-report.json`。图片在 `assets/images/`，其中两张 banner 是原主题资源。

## 修改内容

编辑 `content/posts.json` 后，在项目目录运行：

```powershell
python scripts/build.py
```

脚本使用 Python 标准库，重新生成文章页、首页、归档、搜索索引、RSS 和站点地图。修改整体美化可编辑 `style.css` 与 `script.js`，修改页面模板可编辑 `scripts/build.py`。

将改动提交到 `main` 分支后由 GitHub Pages 自动发布。博客园后续新增文章不会自动同步。

## 致谢与内容说明

美化参考 [BNDong / Cnblogs-Theme-SimpleMemory](https://github.com/BNDong/Cnblogs-Theme-SimpleMemory) 与用户提供的 [凌云_void](https://www.cnblogs.com/lingyunvoid/) CSS。文章沿用作者在原主题中设置的知识共享署名-相同方式共享 4.0 国际许可说明，具体文章中的特殊说明优先。

当前未运行自动化或浏览器测试；浏览器连接在本机初始化失败。发布结果通过 GitHub Pages 部署状态确认。
