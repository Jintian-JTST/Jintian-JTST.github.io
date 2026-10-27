"""Build the static, progressively enhanced Oxford resource directory."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = "/projects/oxford-physics/"
ASSETS = "/assets/projects/oxford-physics/"
TYPES = {
    "lecture": "课程讲义", "problem": "习题册", "official-solution": "课程提供的解答",
    "personal-solution": "个人解答", "revision": "复习笔记", "mock": "模拟题",
    "feedback": "个人复习反馈", "past-paper": "历年试卷", "report": "个人实验记录",
    "lab-manual": "实验讲义", "code": "代码", "notebook": "Notebook",
    "data": "实验数据", "image": "图表与选题", "handbook": "课程手册",
    "selected": "我的题单", "archive": "配套文件",
    "reference-solution": "手写参考解答（来源未注明）",
}
STAGES = {"year1": "大一", "year2": "大二", "other": "其他课程"}


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def size_label(size: int) -> str:
    return f"{size / 1048576:.1f} MB" if size >= 1048576 else f"{max(1, round(size / 1024))} KB"


def shell(title: str, body: str, *, reader: bool = False, extra_head: str = "") -> str:
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} · Jintian Wang / JTST</title>
  <meta name="description" content="Oxford Physics 学习资料：习题与个人解答、课程讲义、历年试卷、实验和代码。">
  <link rel="icon" type="image/png" href="/assets/images/square.png">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <link rel="stylesheet" href="{ASSETS}library.css">
  {extra_head}
</head>
<body class="oxford-library{' library-reading' if reader else ''}">
  <a class="library-skip" href="#library-main">跳至内容</a>
  <header class="navbar"><div class="container nav-inner">
    <a class="brand" href="/" aria-label="Jintian JTST home"><span class="logo" aria-hidden="true"></span><span>Jintian JTST</span></a>
    <nav class="nav-links" aria-label="Primary navigation"><a href="/">Home</a><a class="active" aria-current="page" href="/projects/">Projects</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
  </div></header>
  <main id="library-main" class="container library-main">{body}</main>
  <footer class="footer"><div class="container footer-inner"><div>© <span data-year>2026</span> Jintian JTST</div><a class="small-link" href="{ROOT}">Oxford Physics</a></div></footer>
  <script src="/assets/js/main.js"></script>
</body></html>
'''


def row(resource: dict) -> str:
    r = resource
    groups = r["categories"]
    text = " ".join([r["title"], r["course"], TYPES[r["type"]], r["originalName"],
                     STAGES[r["stage"]], str(r.get("examYear") or ""), r.get("session", "")])
    badges = [r["course"], TYPES[r["type"]]]
    if r.get("examYear"):
        badges.append(str(r["examYear"]) + (" · September" if r.get("session") == "September" else ""))
    if r.get("pages"):
        badges.append(f'{r["pages"]} 页')
    reading = (f'<a class="resource-read" href="{esc(r["viewUrl"])}">阅读 <span aria-hidden="true">↗</span></a>'
               if r.get("viewUrl") else '<span class="resource-download-note">下载阅读</span>')
    related = ''.join(f'<a class="resource-related" href="{esc(link["url"])}">{esc(link["label"])}</a>'
                      for link in r.get("related", []))
    return f'''<li class="resource" id="{esc(r['id'])}" data-groups="{' '.join(groups)}" data-course="{esc(r['course'])}" data-courses="{esc('|'.join(r.get('courses', [r['course']])))}" data-type="{esc(r['type'])}" data-exam-year="{r.get('examYear') or ''}" data-search="{esc(text.casefold())}">
      <span class="resource-format" aria-hidden="true">{esc(r['format'])}</span>
      <div class="resource-copy"><h3><a href="{esc(r.get('viewUrl') or r['downloadUrl'])}">{esc(r['title'])}</a></h3>
      <p class="resource-meta">{'<span aria-hidden="true"> / </span>'.join(esc(b) for b in badges)}</p>
      {f'<div class="resource-relations">{related}</div>' if related else ''}</div>
      <div class="resource-actions">{reading}<a class="resource-download" href="{esc(r['downloadUrl'])}" download="{esc(r['originalName'])}">下载 <span class="resource-size">{size_label(r['bytes'])}</span></a></div>
    </li>'''


def write_directory(repo: Path, catalog: dict) -> None:
    resources = catalog["resources"]
    destination = repo / "projects/oxford-physics"
    destination.mkdir(parents=True, exist_ok=True)
    featured = next((r for r in resources if r.get("featured") == "answers"), None)
    selected = next((r for r in resources if r.get("featured") == "selected"), None)
    feature_html = ""
    if featured:
        chapters = featured.get("chapters", [])
        chapter_links = ''.join(f'<a href="{esc(featured["downloadUrl"])}#page={c["page"]}"><span>{esc(c["label"])}</span><span aria-hidden="true">↗</span></a>' for c in chapters)
        feature_html = f'''<section class="library-feature" aria-labelledby="answers-title">
          <div class="feature-book" aria-hidden="true"><span>CP<br>1—4</span><small>ANSWERS</small></div>
          <div class="feature-copy"><p class="library-eyebrow">JINTIAN WANG / PERSONAL NOTES</p>
            <h2 id="answers-title">大一习题答案合集<span class="feature-edition">修订版</span></h2>
            <p>Classical Mechanics · Electricity &amp; Magnetism · Mathematical Methods · Calculus &amp; Waves</p>
            <div class="feature-links"><a class="button primary" href="{esc(featured['viewUrl'])}">在线阅读 · {featured['pages']} 页 <span aria-hidden="true">↗</span></a><a class="small-link" href="{esc(featured['downloadUrl'])}" download="{esc(featured['originalName'])}">下载 PDF · {size_label(featured['bytes'])}</a></div>
          </div><div class="feature-chapters" aria-label="按章节阅读">{chapter_links}</div>
        </section>'''
    categories = [("all", "全部资料"), ("year1", "大一"), ("year2", "大二"),
                  ("other", "其他课程"), ("exams", "历年考试"), ("mine", "我的解答"), ("lab", "实验与代码")]
    buttons = ''.join(f'<button type="button" class="library-tab{" is-active" if key == "all" else ""}" data-category="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}<span>{len(resources) if key == "all" else sum(key in r["categories"] for r in resources)}</span></button>' for key, label in categories)
    courses = sorted({c for r in resources for c in r.get("courses", [r["course"]])})
    course_options = ''.join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in courses)
    present_types = sorted({r["type"] for r in resources}, key=lambda key: TYPES[key])
    type_options = ''.join(f'<option value="{esc(t)}">{TYPES[t]}</option>' for t in present_types)
    years = sorted({r["examYear"] for r in resources if r.get("examYear")}, reverse=True)
    year_options = ''.join(f'<option value="{y}">{y}</option>' for y in years)
    selected_link = f'<a class="library-quick-link" href="{esc(selected["viewUrl"])}"><span>我的选题清单</span><span>{catalog["selectionCount"]} 条记录 <span aria-hidden="true">↗</span></span></a>' if selected else ""
    bundle_links = ''.join(f'<a href="{esc(b["url"])}">{esc(b["title"])} <span>{size_label(b["bytes"])}</span></a>' for b in catalog.get("bundles", []))
    body = f'''
    <div class="library-breadcrumb"><a href="/projects/">Projects</a><span aria-hidden="true">/</span><span>Oxford Physics</span></div>
    <header class="library-hero"><div><p class="library-eyebrow">THE OXFORD PHYSICS COLLECTION</p><h1>牛津物理<span>学习资料库</span></h1><p class="library-intro">课程、习题、解答与实验。把学习中用到的资料，放在一起。</p></div>
      <dl class="library-stats"><div><dt>份资料</dt><dd>{len(resources)}</dd></div><div><dt>个课程 / 专题</dt><dd>{len(courses)}</dd></div><div><dt>个人答案</dt><dd>{featured['pages'] if featured else 0}<small> 页</small></dd></div></dl>
    </header>
    {feature_html}
    <div class="library-toolbar" id="library-controls" hidden>
      <label class="library-search" for="library-search"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="m16 16 5 5"></path></svg><span class="sr-only">搜索资料</span><input id="library-search" type="search" placeholder="搜索课程、题单、解答或年份…" autocomplete="off"><kbd>/</kbd></label>
      <div class="library-tabs" role="group" aria-label="资料分类">{buttons}</div>
    </div>
    <div class="library-layout"><aside class="library-sidebar">
      <form id="library-filter-form" hidden><h2>筛选资料</h2><label for="filter-course">课程 / 专题</label><select id="filter-course"><option value="">全部课程</option>{course_options}</select><label for="filter-type">资料类型</label><select id="filter-type"><option value="">全部类型</option>{type_options}</select><label for="filter-year">考试年份</label><select id="filter-year"><option value="">全部年份</option>{year_options}</select><button class="filter-reset" type="reset">重置筛选 <span aria-hidden="true">↺</span></button></form>
      {selected_link}
      <div class="library-note"><p class="library-eyebrow">ABOUT THIS COLLECTION</p><p>由 Jintian Wang 整理的个人学习资料。个人解答与复习反馈供学习参考。</p><p>课程讲义和试卷保留原作者与课程标识。本页面为个人资料库。</p><span class="library-updated">更新于 {catalog['updatedAt']}</span></div>
      {f'<details class="library-bundles"><summary>按课程打包下载</summary>{bundle_links}</details>' if bundle_links else ''}
    </aside><section class="library-results" aria-labelledby="results-title">
      <div class="results-heading"><h2 id="results-title">全部资料</h2><p id="result-count" role="status" aria-live="polite">{len(resources)} 份资料</p></div>
      <noscript><p class="library-noscript">下方为完整资料目录。开启 JavaScript 后可搜索与筛选；阅读和下载无需 JavaScript。</p></noscript>
      <ul class="resource-list">{''.join(row(r) for r in resources)}</ul>
      <div class="library-empty" id="library-empty" hidden><h3>没有找到匹配的资料</h3><p>试试更短的关键词，或清除课程与年份筛选。</p><button class="button" id="empty-reset" type="button">清除全部筛选</button></div>
      <button class="button library-more" id="library-more" type="button" hidden>显示更多资料</button>
    </section></div>
    <script src="{ASSETS}library.js" defer></script>'''
    (destination / "index.html").write_text(shell("牛津物理学习资料库 · Oxford Physics", body), encoding="utf-8")


def reading_page(resource: dict, content: str, *, extra_head: str = "") -> str:
    r = resource
    body = f'''<div class="library-breadcrumb"><a href="{ROOT}">Oxford Physics</a><span aria-hidden="true">/</span><span>{esc(TYPES[r['type']])}</span></div>
      <header class="reading-header"><p class="library-eyebrow">{esc(r['course'])} / {esc(STAGES[r['stage']])}</p><h1>{esc(r['title'])}</h1><div class="reading-meta"><span>{esc(r['format'])} · {size_label(r['bytes'])}</span><a class="button" href="{esc(r['downloadUrl'])}" download="{esc(r['originalName'])}">下载原格式文件 <span aria-hidden="true">↓</span></a><a class="small-link" href="{ROOT}">返回资料库</a></div></header>
      <article class="reading-content">{content}</article>'''
    return shell(r["title"], body, reader=True, extra_head=extra_head)
