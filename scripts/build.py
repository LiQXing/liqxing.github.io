"""Build the independent blog from content/posts.json using Python's standard library."""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape
from datetime import datetime
from xml.sax.saxutils import escape as xml
import json

ROOT=Path(__file__).resolve().parents[1]
POSTS=json.loads((ROOT/'content/posts.json').read_text(encoding='utf-8'))
ORIGIN='https://liqxing.github.io/'
MOTTO='夜雨声烦扰清梦，桃花碎落乱春风。'
COUNTS=Counter(p['category'] for p in POSTS)
E=lambda s:escape(str(s),quote=True)

def head(title,description,path='',prefix=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#283b55"><meta name="description" content="{E(description)}"><title>{E(title)}</title><link rel="canonical" href="{ORIGIN}{path}"><link rel="icon" href="{prefix}icon.svg" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" title="LiQXing 的博客" href="{prefix}feed.xml"><link rel="stylesheet" href="{prefix}assets/vendor/long-cang.css"><link rel="stylesheet" href="{prefix}style.css"><link rel="stylesheet" href="{prefix}assets/vendor/APlayer.min.css"><script>try{{document.documentElement.dataset.theme=localStorage.getItem('liqxing-theme')||'light'}}catch(e){{}}</script></head><body><a class="skip" href="#main">跳到正文</a><div id="reading-progress" aria-hidden="true"></div>'''

def nav(prefix=''):
    return f'''<header class="top-nav"><button id="menu-toggle" class="menu-toggle" aria-controls="site-menu" aria-expanded="false">☰ MENU</button><a class="nav-brand" href="{prefix}index.html">LiQXing</a><nav aria-label="主要导航"><a href="{prefix}index.html#posts">文章</a><a href="{prefix}archive.html">归档</a><a href="{prefix}about.html">关于</a><button id="theme-toggle" class="theme-toggle" aria-label="切换昼夜模式">◐</button></nav></header><div id="menu-backdrop" hidden></div><aside id="site-menu" class="site-menu" aria-label="网站菜单" inert><button id="menu-close" aria-label="关闭菜单">×</button><div class="menu-profile"><span class="profile-mark">L.</span><h2>LiQXing</h2><p>{MOTTO}</p></div><div class="menu-stats"><span><b>{len(POSTS)}</b>文章</span><span><b>{len(COUNTS)}</b>分类</span><span><b>2023</b>开始记录</span></div><nav aria-label="侧栏导航"><a href="{prefix}index.html">⌂ <span>首页</span></a><a href="{prefix}archive.html">▤ <span>文章归档</span></a><a href="{prefix}categories.html">◇ <span>文章分类</span></a><a href="{prefix}about.html">○ <span>关于我</span></a><a href="https://www.cnblogs.com/LiQXing/" target="_blank" rel="noopener noreferrer">↗ <span>博客园</span></a><a href="https://github.com/LiQXing" target="_blank" rel="noopener noreferrer">⌘ <span>GitHub</span></a><a href="https://msg.cnblogs.com/send/LiQXing" target="_blank" rel="noopener noreferrer">✉ <span>联系</span></a><a href="{prefix}feed.xml">◔ <span>RSS 订阅</span></a></nav><p class="menu-foot">愿每一次思考，都有所回响。</p></aside>'''

def hero(title,subtitle='',kind='inner',meta=''):
    content=f'<section class="hero hero-{kind}"><div class="hero-shade"></div><div class="hero-orbs" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div class="hero-content"><p class="hero-kicker">ALGORITHMS · NOTES · LIFE</p><h1>{E(title)}</h1>'
    if subtitle:content+=f'<p class="hero-subtitle">{E(subtitle)}</p>'
    return content+meta+'</div>'+('<a class="scroll-down" href="#posts" aria-label="向下浏览文章">⌄</a>' if kind=='home' else '')+'</section>'

def footer(prefix=''):
    return f'''<footer class="footer"><a class="footer-name" href="{prefix}index.html">LiQXing</a><p>{MOTTO}</p><div><a href="https://www.cnblogs.com/LiQXing/">博客园</a><span>·</span><a href="https://github.com/LiQXing/liqxing.github.io">GitHub</a><span>·</span><a href="{prefix}feed.xml">RSS</a></div><small>美化灵感：<a href="https://github.com/BNDong/Cnblogs-Theme-SimpleMemory">SimpleMemory</a> / <a href="https://www.cnblogs.com/lingyunvoid/">凌云_void</a></small></footer><a class="back-top" href="#" aria-label="返回顶部">↑</a><a class="music-fallback" href="https://music.163.com/#/playlist?id=7002443469" target="_blank" rel="noopener noreferrer">♫ 我的歌单 ↗</a><!-- Owner's original playlist configuration --><div id="aplayer" class="aplayer" data-order="random" data-id="7002443469" data-server="netease" data-type="playlist" data-fixed="true" data-autoplay="true" data-volume="0.6" data-listfolded="true"></div><script defer src="{prefix}assets/vendor/jquery.min.js"></script><script defer src="{prefix}assets/vendor/APlayer.min.js"></script><script defer src="{prefix}script.js"></script><script defer src="https://cdn.jsdelivr.net/gh/kaygb/kaygb@master/js/v3.js"></script><!-- 必须使用原地址 --><script defer src="{prefix}assets/vendor/Meting.min.js"></script><script defer src="https://blog-static.cnblogs.com/files/blogs/693306/layer.js"></script></body></html>'''

def card(p):
    cover=f'<a class="post-cover" href="{p["path"]}" tabindex="-1" aria-hidden="true"><img src="{p["cover"]}" alt="" loading="lazy"></a>' if p['cover'] else ''
    return f'<article class="post-card{" has-cover" if cover else ""}" data-id="{p["id"]}" data-category="{E(p["category"])}"><div class="post-card-content"><div class="post-meta"><time datetime="{p["date"].replace(" ","T")}+08:00">{p["date"][:10]}</time><span>·</span><a href="categories.html#{E(p["category"])}">{E(p["category"])}</a></div><h2><a href="{p["path"]}">{E(p["title"])}</a></h2><p class="post-excerpt">{E(p["excerpt"])}</p><a class="read-more" href="{p["path"]}">阅读全文 <span>→</span></a></div>{cover}</article>'

def write(path,content):
    dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(content,encoding='utf-8')

filters=''.join(f'<button type="button" data-filter="{E(c)}" aria-pressed="false">{E(c)} <span>{n}</span></button>' for c,n in COUNTS.items())
home=f'''<main id="main" class="blog-shell"><section id="posts" class="post-section"><div class="section-title"><div><p class="eyebrow">THINK. SOLVE. WRITE.</p><h2>写下思考，也记录生活。</h2></div><span class="total-count">{len(POSTS)} 篇文章</span></div><form class="search-form" role="search"><label class="sr-only" for="post-search">搜索文章标题或正文</label><span aria-hidden="true">⌕</span><input id="post-search" type="search" placeholder="搜索题解、算法，或一个念头……" autocomplete="off"><kbd>/</kbd></form><div class="filters" aria-label="筛选文章分类"><button type="button" data-filter="all" class="active" aria-pressed="true">全部 <span>{len(POSTS)}</span></button>{filters}</div><p id="result-count" class="result-count" role="status"></p><div id="post-list">{''.join(card(p) for p in POSTS)}</div><div id="empty-state" hidden><span>⌕</span><h3>暂时没有找到这篇文章。</h3><p>换个关键词，或看看其他分类吧。</p><button id="clear-search" type="button">查看全部文章</button></div><nav id="pagination" aria-label="文章分页"></nav><noscript><p>这里展示全部 {len(POSTS)} 篇文章。</p></noscript></section></main><script defer src="assets/search-index.js"></script>'''
write('index.html',head('LiQXing 的博客 · 夜雨与春风',MOTTO)+nav()+hero('LiQXing',MOTTO,'home')+home+footer())

groups=defaultdict(list)
for p in POSTS:groups[p['date'][:4]].append(p)
def rows(items,dates='short'):
    return '<ol>'+''.join(f'<li><time>{p["date"][5:10] if dates=="short" else p["date"][:10]}</time><a href="{p["path"]}">{E(p["title"])}</a><span class="archive-category">{E(p["category"])}</span></li>' for p in items)+'</ol>'
archive=f'<main id="main" class="blog-shell"><section class="standard-page"><div class="section-title"><div><p class="eyebrow">ALL THE MOMENTS</p><h2>文章归档</h2></div><span class="total-count">共 {len(POSTS)} 篇</span></div>'
for year,items in groups.items():archive+=f'<section class="archive-group"><h2>{year}<span>{len(items)} 篇</span></h2>{rows(items)}</section>'
write('archive.html',head('文章归档 · LiQXing','LiQXing 的全部文章归档。','archive.html')+nav()+hero('文章归档','把走过的路，慢慢整理成文字。')+archive+'</section></main>'+footer())
categories='<main id="main" class="blog-shell"><section class="standard-page"><p class="eyebrow">FIND YOUR WAY</p><h2 class="page-heading">文章分类</h2><p class="page-intro">题解与笔记，竞赛与生活。</p>'
for c,n in COUNTS.items():categories+=f'<section class="archive-group" id="{E(c)}"><h2>{E(c)}<span>{n} 篇</span></h2>{rows([p for p in POSTS if p["category"]==c],"full")}</section>'
write('categories.html',head('文章分类 · LiQXing','AtCoder、Codeforces、算法笔记、比赛记录与随笔。','categories.html')+nav()+hero('文章分类','在不同的思考之间，找到你的入口。')+categories+'</section></main>'+footer())
about=f'''<main id="main" class="blog-shell"><article class="standard-page about-page"><p class="eyebrow">A LITTLE ABOUT ME</p><h2 class="page-heading">你好，我是 LiQXing。</h2><p class="about-lead">写题解，也写生活。<br>记录推敲一个解法时的思绪，也留下那些想说的话。</p><p>这里有 AtCoder、Codeforces 和各类竞赛的题解，有线段树与算法模板的学习笔记，也有关于成长、阅读和生活的随笔。</p><blockquote>{MOTTO}</blockquote><p>这些文字最初写在博客园。如今，我把它们整理到这个独立的小站里，继续留下一点自己的声音。</p><div class="about-links"><a href="https://www.cnblogs.com/LiQXing/">我的博客园 ↗</a><a href="https://github.com/LiQXing">我的 GitHub ↗</a><a href="https://msg.cnblogs.com/send/LiQXing">给我留言 ↗</a></div><div class="about-numbers"><div><b>{len(POSTS)}</b><span>篇文章</span></div><div><b>{len(COUNTS)}</b><span>个分类</span></div><div><b>2023 — 2026</b><span>文字里的时光</span></div></div></article></main>'''
write('about.html',head('关于我 · LiQXing','LiQXing：写题解，也写生活。','about.html')+nav()+hero('关于我','于文字之间，留下一点自己的声音。')+about+footer())

for i,p in enumerate(POSTS):
    meta=f'<p class="hero-meta"><time datetime="{p["date"].replace(" ","T")}+08:00">{p["date"]}</time><span>·</span><a href="../categories.html#{E(p["category"])}">{E(p["category"])}</a></p>'
    body=f'<main id="main" class="blog-shell article-shell"><article class="article-panel"><div class="source-note">最初发表于 <a href="{E(p["source"])}" target="_blank" rel="noopener noreferrer">博客园 ↗</a><span>作者 LiQXing</span></div><div id="cnblogs_post_body" class="article-body">{p["html"]}</div><div class="article-copyright"><strong>LiQXing</strong><p>除特殊说明外，转载请注明出处。知识共享署名-相同方式共享 4.0 国际许可协议。</p><a href="{E(p["source"])}" target="_blank" rel="noopener noreferrer">查看博客园原文 ↗</a></div><nav class="post-neighbors" aria-label="相邻文章">'
    if i+1<len(POSTS):
        prev=POSTS[i+1];body+=f'<a href="{prev["id"]}.html"><small>← 上一篇</small><span>{E(prev["title"])}</span></a>'
    else:body+='<span></span>'
    if i>0:
        nextp=POSTS[i-1];body+=f'<a href="{nextp["id"]}.html"><small>下一篇 →</small><span>{E(nextp["title"])}</span></a>'
    body+='</nav></article><aside class="toc-panel"><details open><summary>文章目录</summary><nav id="toc" aria-label="文章目录"></nav></details></aside></main><dialog id="image-dialog"><button aria-label="关闭图片">×</button><img alt=""></dialog>'
    math=r'''<script>window.MathJax={tex:{inlineMath:[['\\(','\\)'],['$','$']],displayMath:[['\\[','\\]'],['$$','$$']],processEscapes:true},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script><script async src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script><script defer src="../assets/vendor/highlight.min.js"></script>'''
    write(p['path'],head(p['title']+' · LiQXing',p['excerpt'],p['path'],'../')+nav('../')+hero(p['title'],'','article',meta)+body+math+footer('../'))

search=[{k:p[k] for k in ['id','title','text','category','date','path']} for p in POSTS]
write('assets/search-index.js','window.BLOG_SEARCH='+json.dumps(search,ensure_ascii=False).replace('</','<\\/')+';\n')
urls=['','archive.html','categories.html','about.html']+[p['path'] for p in POSTS]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+xml(ORIGIN+u)+'</loc></url>' for u in urls)+'</urlset>')
write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'sitemap.xml\n')
items=''.join(f'<item><title>{xml(p["title"])}</title><link>{ORIGIN}{p["path"]}</link><guid>{ORIGIN}{p["path"]}</guid><pubDate>{datetime.strptime(p["date"],"%Y-%m-%d %H:%M").strftime("%a, %d %b %Y %H:%M:00 +0800")}</pubDate><description>{xml(p["excerpt"])}</description></item>' for p in POSTS)
write('feed.xml','<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>LiQXing 的博客</title><link>'+ORIGIN+'</link><description>'+MOTTO+'</description><language>zh-cn</language>'+items+'</channel></rss>')
write('404.html',head('页面未找到 · LiQXing','这个页面暂时不在这里。','404.html','/')+nav('/')+hero('这条路，暂时没有尽头。','也许你想找的文字，正在另一个地方。')+'<main id="main" class="blog-shell"><section class="standard-page"><h2 class="page-heading">404</h2><p>文章已整理进新的归档。</p><a href="/archive.html">去文章归档看看 →</a></section></main><script>const m=location.pathname.match(/\\/p\\/(\\d+)\\/?$/);if(m)location.replace("/p/"+m[1]+".html"+location.hash);</script>'+footer('/'))
print(f'Built homepage, archive, categories, about, {len(POSTS)} article pages, RSS and sitemap.')
