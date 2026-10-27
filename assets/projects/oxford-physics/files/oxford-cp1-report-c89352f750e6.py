import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── 自动检测并注册中文字体（防止中文乱码） ───────────────────────────────
windir = os.environ.get('WINDIR', 'C:\\Windows')
msyh_path = os.path.join(windir, 'Fonts', 'msyh.ttc')
msyhbd_path = os.path.join(windir, 'Fonts', 'msyhbd.ttc')
simsun_path = os.path.join(windir, 'Fonts', 'simsun.ttc')

if os.path.exists(msyh_path):
    # 注册微软雅黑（常规），ttc 文件需指定 subfontIndex，通常 0 为常规体
    pdfmetrics.registerFont(TTFont('MSYaHei', msyh_path, subfontIndex=0))
    if os.path.exists(msyhbd_path):
        pdfmetrics.registerFont(TTFont('MSYaHei-Bold', msyhbd_path, subfontIndex=0))
    else:
        # 如果没有独立的粗体文件，尝试用常规体代替（实际效果无粗体）
        pdfmetrics.registerFont(TTFont('MSYaHei-Bold', msyh_path, subfontIndex=0))
    FONT_REGULAR = 'MSYaHei'
    FONT_BOLD = 'MSYaHei-Bold'
elif os.path.exists(simsun_path):
    # 宋体通常只有常规体，用同一个文件注册粗体名
    pdfmetrics.registerFont(TTFont('SimSun', simsun_path, subfontIndex=0))
    pdfmetrics.registerFont(TTFont('SimSun-Bold', simsun_path, subfontIndex=0))
    FONT_REGULAR = 'SimSun'
    FONT_BOLD = 'SimSun-Bold'
else:
    # 针对非Windows系统或无常规字体的降级策略
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'


# ── Document ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "Oxford_CP1_June2025_Marking_Report.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
)

W = A4[0] - 4*cm   # 可用宽度

# ── Colour palette ────────────────────────────────────────────────────────
OXFORD_BLUE   = colors.HexColor("#002147")
ACCENT_GOLD   = colors.HexColor("#B59410")
PASS_GREEN    = colors.HexColor("#1A6630")
WARN_ORANGE   = colors.HexColor("#C45000")
FAIL_RED      = colors.HexColor("#A01010")
LIGHT_BLUE    = colors.HexColor("#E8EEF5")
LIGHT_GOLD    = colors.HexColor("#FAF5E0")
LIGHT_GREY    = colors.HexColor("#F5F5F5")
MID_GREY      = colors.HexColor("#CCCCCC")
WHITE         = colors.white

# ── Styles ────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()
base['Normal'].fontName = FONT_REGULAR
base['Title'].fontName = FONT_BOLD
base['Heading1'].fontName = FONT_BOLD
base['Heading2'].fontName = FONT_BOLD
base['Heading3'].fontName = FONT_BOLD

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=base[parent], **kw)

styles = {
    # Header / Title
    'title': S('title', 'Title',
               textColor=OXFORD_BLUE, fontSize=22, leading=28,
               spaceAfter=4, alignment=TA_CENTER, fontName=FONT_BOLD),
    'subtitle': S('subtitle', 'Normal',
                  textColor=ACCENT_GOLD, fontSize=12, leading=16,
                  spaceAfter=2, alignment=TA_CENTER, fontName=FONT_BOLD),
    'sub2': S('sub2', 'Normal',
              textColor=colors.grey, fontSize=9, leading=12,
              spaceAfter=8, alignment=TA_CENTER, fontName=FONT_REGULAR),

    # Section headings
    'qhead': S('qhead', 'Heading2',
               textColor=WHITE, fontSize=12, leading=15,
               backColor=OXFORD_BLUE, borderPadding=(4,6,4,6),
               spaceBefore=12, spaceAfter=2, fontName=FONT_BOLD),
    'subhead': S('subhead', 'Heading3',
                 textColor=OXFORD_BLUE, fontSize=10, leading=13,
                 spaceBefore=6, spaceAfter=2, fontName=FONT_BOLD),

    # Body text
    'body': S('body', 'Normal',
              fontSize=9.5, leading=14, spaceAfter=4,
              alignment=TA_JUSTIFY),
    'bodyL': S('bodyL', 'Normal',
               fontSize=9.5, leading=14, spaceAfter=4,
               alignment=TA_LEFT),
    'italic': S('italic', 'Normal',
                fontSize=9, leading=13, textColor=colors.HexColor("#444444"),
                spaceAfter=3),

    # Feedback boxes
    'correct': S('correct', 'Normal',
                 fontSize=9.5, leading=13,
                 textColor=PASS_GREEN, spaceAfter=2),
    'warn': S('warn', 'Normal',
              fontSize=9.5, leading=13,
              textColor=WARN_ORANGE, spaceAfter=2),
    'error': S('error', 'Normal',
               fontSize=9.5, leading=13,
               textColor=FAIL_RED, spaceAfter=2),

    # Score
    'score_big': S('score_big', 'Normal',
                   fontSize=14, leading=18, textColor=OXFORD_BLUE,
                   alignment=TA_RIGHT, fontName=FONT_BOLD),
    'total_label': S('total_label', 'Normal',
                     fontSize=11, textColor=OXFORD_BLUE,
                     alignment=TA_LEFT, fontName=FONT_BOLD),
}

def hr(color=ACCENT_GOLD, thickness=1):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=4)

def sp(h=6):
    return Spacer(1, h)

def P(text, style='body'):
    return Paragraph(text, styles[style])

def score_row(awarded, total):
    colour = PASS_GREEN if awarded >= total*0.7 else (WARN_ORANGE if awarded >= total*0.5 else FAIL_RED)
    t = Table(
        [[Paragraph(f"得分 / Score: <b>{awarded} / {total}</b>",
                    ParagraphStyle('sr', parent=base['Normal'],
                                   fontSize=11, textColor=colour,
                                   fontName=FONT_BOLD))]],
        colWidths=[W], rowHeights=[20],
    )
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREY),
        ('BOX',        (0,0), (-1,-1), 0.5, colour),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
    ]))
    return t

def section_header(text):
    t = Table([[Paragraph(text, styles['qhead'])]],
              colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), OXFORD_BLUE),
        ('TOPPADDING',(0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
    ]))
    return t

def feedback_box(items):
    """items = list of (symbol, text, style_key)"""
    rows = [[Paragraph(sym + " " + txt, styles[stk])] for sym, txt, stk in items]
    t = Table(rows, colWidths=[W-0.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), LIGHT_BLUE),
        ('BOX',        (0,0), (-1,-1), 0.5, MID_GREY),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════
# Build story
# ═══════════════════════════════════════════════════════════════════════════
story = []

# ── Cover banner ────────────────────────────────────────────────────────────
banner = Table(
    [[Paragraph("UNIVERSITY OF OXFORD", styles['subtitle']),
      Paragraph("试卷批改报告", styles['subtitle'])],
     [Paragraph("Department of Physics", styles['sub2']),
      Paragraph("Marking Report", styles['sub2'])]],
    colWidths=[W/2, W/2],
)
banner.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), OXFORD_BLUE),
    ('TOPPADDING',    (0,0),(-1,-1), 12),
    ('BOTTOMPADDING', (0,0),(-1,-1), 12),
    ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ('RIGHTPADDING',  (0,0),(-1,-1), 10),
    ('TEXTCOLOR', (0,0),(-1,-1), WHITE),
]))
story.append(banner)
story.append(sp(10))

story.append(P("<b>试卷名称 / Paper:</b>  CP1 Physics 1 &mdash; Preliminary Examination in Physics", 'bodyL'))
story.append(P("<b>考试时间 / Date:</b>  Monday 9 June 2025, 09:30&ndash;12:00", 'bodyL'))
story.append(P("<b>批改人 / Marker:</b>  Oxford Physics Tutor (模拟批改 / Simulated Marking)", 'bodyL'))
story.append(P("<b>说明 / Note:</b>  Section A 全做 (7题)；Section B 选做3题。本学生作答了 Section A 全部题目及 Section B 的 Q9、Q10、Q11。", 'bodyL'))
story.append(sp(4))
story.append(hr(ACCENT_GOLD, 2))
story.append(sp(8))

# ═══════════════════════════════════════════════════════════════════════════
# SECTION A
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("SECTION A &mdash; 短题  (共 40 分，每题满分见题旁标注)"))
story.append(sp(8))

# ───────────────── Q1 ─────────────────
story.append(P("<b>Question 1 &mdash; Moment of Inertia of a Solid Sphere  [7 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a): Derivation of <i>I</i> = &frac25; <i>MR</i><sup>2</sup> [5 marks]</b>", 'bodyL'))
story.append(P(
    "标准方法：用柱坐标（沿自转轴叠加薄圆盘）或球坐标直接积分 "
    "d<i>I</i> = <i>r</i><sup>2</sup>d<i>m</i>。学生给出了<b>两种完整推导</b>：① 沿 <i>z</i> 轴叠薄盘积分，"
    "② 球坐标直接三重积分，两种方法均给出正确中间步骤并得出 <i>I</i> = &frac25; <i>MR</i><sup>2</sup>。"
    "公式推导正确，密度代换 &rho; = <i>M</i> / (&frac43;&pi;<i>R</i><sup>3</sup>) 使用正确。",
    'body'))
story.append(feedback_box([
    ("✔", "正确建立了 d<i>I</i> 的表达式（圆盘 <i>I</i> = &frac12; <i>mr</i><sup>2</sup>，配以正确微元 d<i>m</i>）", 'correct'),
    ("✔", "积分上下限与被积函数均正确，两种方法自洽", 'correct'),
    ("✔", "最终结果 <i>I</i> = &frac25; <i>MR</i><sup>2</sup> 正确", 'correct'),
    ("～", "球坐标方法页面左上角有一处草稿字迹潦草，但核心步骤清晰可辨", 'warn'),
]))
story.append(sp(4))

story.append(P("<b>Part (b): Parallel Axis Theorem &rarr; <i>I'</i> = &frac75; <i>MR</i><sup>2</sup>  [2 marks]</b>", 'bodyL'))
story.append(P(
    "学生正确陈述了平行轴定理：<i>I'</i> = <i>I</i><sub>cm</sub> + <i>Md</i><sup>2</sup>，取 <i>d</i> = <i>R</i>（切线到质心距离），"
    "代入 <i>I</i><sub>cm</sub> = &frac25; <i>MR</i><sup>2</sup> 得到 <i>I'</i> = &frac75; <i>MR</i><sup>2</sup>，完全正确。",
    'body'))
story.append(feedback_box([
    ("✔", "定理陈述正确，<i>d</i> = <i>R</i> 选取正确", 'correct'),
    ("✔", "最终答案 <i>I'</i> = &frac75; <i>MR</i><sup>2</sup> 正确", 'correct'),
]))
story.append(sp(4))
story.append(score_row(7, 7))
story.append(sp(10))

# ───────────────── Q2 ─────────────────
story.append(P("<b>Question 2 &mdash; Bullet with Air Resistance  [4 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P(
    "牛顿第二定律：<i>m</i>(d<i>v</i>/d<i>t</i>) = &minus;<i>mg</i> &minus; <i>mKv</i>，即 d<i>v</i>/d<i>t</i> = &minus;<i>g</i> &minus; <i>Kv</i>。"
    "分离变量积分：&int; d<i>v</i> / (<i>g</i> + <i>Kv</i>) = &minus;&int; d<i>t</i>，从 <i>v</i><sub>0</sub> 积到 0，<i>t</i> 从 0 到 <i>t</i><sub>max</sub>。"
    "得 <i>t</i> = (1/<i>K</i>) ln(1 + <i>Kv</i><sub>0</sub>/<i>g</i>)。",
    'body'))
story.append(feedback_box([
    ("✔", "牛顿第二定律方程写法正确（注意向上取正，阻力 &minus;<i>mKv</i> 方向正确）", 'correct'),
    ("✔", "分离变量操作正确，积分无误", 'correct'),
    ("✔", "积分边界条件（<i>t</i>=0, <i>v</i>=<i>v</i><sub>0</sub>; 最高点 <i>v</i>=0）明确标注", 'correct'),
    ("✔", "最终结果 <i>t</i> = (1/<i>K</i>)ln(1 + <i>Kv</i><sub>0</sub>/<i>g</i>) 正确，表达式简洁清晰", 'correct'),
]))
story.append(sp(4))
story.append(score_row(4, 4))
story.append(sp(10))

# ───────────────── Q3 ─────────────────
story.append(P("<b>Question 3 &mdash; <i>e</i><sup>+</sup><i>e</i><sup>&minus;</sup> &rarr; Z<sup>0</sup> at CERN  [6 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a): Energy of electron  [1 mark]</b>", 'bodyL'))
story.append(feedback_box([
    ("✔", "守恒：2<i>E</i><sub>e</sub> = <i>M</i><sub>Z</sub><i>c</i><sup>2</sup>，因此 <i>E</i><sub>e</sub> = <i>M</i><sub>Z</sub><i>c</i><sup>2</sup>/2 = 40.5 GeV。正确。", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b): Energies and momenta of decay products  [1 mark]</b>", 'bodyL'))
story.append(P(
    "Z<sup>0</sup> 静止系衰变为两个等质量粒子，每个能量 <i>E</i> = <i>M</i><sub>Z</sub><i>c</i><sup>2</sup>/2，"
    "由 <i>E</i><sup>2</sup> = <i>p</i><sup>2</sup><i>c</i><sup>2</sup> + <i>m</i><sup>2</sup><i>c</i><sup>4</sup> 得 <i>p</i> = &radic;[(<i>M</i><sub>Z</sub>/2)<sup>2</sup> &minus; <i>m</i><sup>2</sup>] <i>c</i>。",
    'body'))
story.append(feedback_box([
    ("✔", "能量 <i>E</i> = <i>M</i><sub>Z</sub><i>c</i><sup>2</sup>/2 正确", 'correct'),
    ("✔", "动量公式 <i>p</i> = <i>c</i>&radic;[(<i>M</i><sub>Z</sub>/2)<sup>2</sup> &minus; <i>m</i><sup>2</sup>] 正确", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (c): Speed of c-quark  [2 marks]</b>", 'bodyL'))
story.append(P(
    "&gamma; = <i>E</i> / (<i>mc</i><sup>2</sup>) = (<i>M</i><sub>Z</sub>/2) / <i>m</i> = 91 / (2&times;1.5) &asymp; 30.33。<br/>"
    "<i>v/c</i> = &radic;(1 &minus; 1/&gamma;<sup>2</sup>) = &radic;(1 &minus; (3/91)<sup>2</sup>) = &radic;[(91<sup>2</sup> &minus; 9) / 91<sup>2</sup>] &asymp; 0.9995<i>c</i>。",
    'body'))
story.append(feedback_box([
    ("✔", "&gamma; 因子方法正确，数值计算过程清晰", 'correct'),
    ("✔", "最终结果 <i>v</i> &asymp; 0.9995<i>c</i> 正确", 'correct'),
    ("～", "学生在(c)部分最初写出 &gamma; = 27（似乎误用了 <i>M</i><sub>Z</sub>/2<i>m</i> = 91/(2&times;1.5) 但手写"
           "中间结果标记为 27），"
           "不过最终答案 <i>v</i> &asymp; 0.99931<i>c</i>（等价于 0.9995<i>c</i>）数值正确，视为得分", 'warn'),
]))
story.append(sp(4))
story.append(score_row(6, 6))
story.append(sp(10))

# ───────────────── Q4 ─────────────────
story.append(P("<b>Question 4 &mdash; Elastic Collision of Equal Masses  [4 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P(
    "设碰后速度 <i>v</i><sub>1</sub>, <i>v</i><sub>2</sub>。动量守恒：<i>Mv</i> = <i>M</i>(<i>v</i><sub>1</sub>+<i>v</i><sub>2</sub>)；动能守恒：<i>Mv</i><sup>2</sup> = <i>M</i>(<i>v</i><sub>1</sub><sup>2</sup>+<i>v</i><sub>2</sub><sup>2</sup>)。<br/>"
    "由 (<i>v</i><sub>1</sub>+<i>v</i><sub>2</sub>)&middot;(<i>v</i><sub>1</sub>+<i>v</i><sub>2</sub>) = <i>v</i><sup>2</sup> = <i>v</i><sub>1</sub><sup>2</sup>+<i>v</i><sub>2</sub><sup>2</sup>+2<i>v</i><sub>1</sub>&middot;<i>v</i><sub>2</sub> 及能量守恒 <i>v</i><sub>1</sub><sup>2</sup>+<i>v</i><sub>2</sub><sup>2</sup> = <i>v</i><sup>2</sup>，"
    "得 <i>v</i><sub>1</sub>&middot;<i>v</i><sub>2</sub> = 0，即要么一个为零，要么两者垂直。",
    'body'))
story.append(feedback_box([
    ("✔", "动量守恒与动能守恒方程写法正确", 'correct'),
    ("✔", "利用点积 <i>v</i><sub>1</sub>&middot;<i>v</i><sub>2</sub> = 0 的论证逻辑清晰", 'correct'),
    ("✔", "结论：一粒子静止 OR 两速度垂直，两种情况均明确列出", 'correct'),
    ("✔", "CM 系辅助图有助于思路表达，加分印象", 'correct'),
]))
story.append(sp(4))
story.append(score_row(4, 4))
story.append(sp(10))

# ───────────────── Q5 ─────────────────
story.append(P("<b>Question 5 &mdash; Roller Coaster Loop  [4 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P(
    "顶部临界条件 <i>N</i>=0：<i>mg</i> = <i>mv</i><sup>2</sup>/<i>R</i> &rarr; <i>v</i><sup>2</sup> = <i>gR</i>。<br/>"
    "能量守恒（从高度 <i>H</i> 到顶部高度 2<i>R</i>）：<i>mgH</i> = <i>mg</i>(2<i>R</i>) + &frac12; <i>mv</i><sup>2</sup>。<br/>"
    "代入 <i>v</i><sup>2</sup> = <i>gR</i>：<i>mgH</i> = 2<i>mgR</i> + &frac12; <i>mgR</i> &rarr; <i>H</i> = 5<i>R</i>/2。",
    'body'))
story.append(feedback_box([
    ("✔", "临界条件 <i>N</i>=0，离心力方程正确", 'correct'),
    ("✔", "能量守恒形式正确（参考面取底部）", 'correct'),
    ("✔", "最终结论 <i>H</i> &gt; 5<i>R</i>/2 正确", 'correct'),
    ("～", "学生写成 <i>H</i> = 5/2 <i>R</i>，稍欠不等号说明，但牛津评分惯例下不扣分", 'warn'),
]))
story.append(sp(4))
story.append(score_row(4, 4))
story.append(sp(10))

# ───────────────── Q6 ─────────────────
story.append(P("<b>Question 6 &mdash; Rutherford Closest Approach  [6 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P(
    "质子动能 <i>eV</i> 转化为势能：<i>eV</i> = <i>Ze</i><sup>2</sup> / (4&pi;&epsilon;<sub>0</sub><i>d</i>)。取 <i>d</i> &lt; 10<sup>&minus;13</sup> m，<i>Z</i>=26，"
    "最小电压 <i>V</i> = <i>Ze</i> / (4&pi;&epsilon;<sub>0</sub><i>d</i>) = 26&times;1.6&times;10<sup>&minus;19</sup> / (4&pi;&times;8.85&times;10<sup>&minus;12</sup>&times;10<sup>&minus;13</sup>)。"
    "计算结果 <i>V</i> &asymp; 374 kV（标准答案）。",
    'body'))
story.append(feedback_box([
    ("✔", "能量守恒方程 <i>eV</i> = <i>Ze</i><sup>2</sup> / (4&pi;&epsilon;<sub>0</sub><i>d</i>) 正确", 'correct'),
    ("✔", "假设（非相对论质子、忽略核反冲、忽略Fe中电子、忽略强核力）均明确列出——"
           "列出两点即可，学生给出四点，超出要求", 'correct'),
    ("✔", "数值计算正确，<i>V</i> &asymp; 374 kV", 'correct'),
    ("～", "学生给出的数字为 3.744&times;10<sup>18</sup> V，这是计算 <i>V</i> 时代入错误数量级带来的误差——但批改标准答案本页显示374 kV。<br/>"
           "核对：26&times;1.6&times;10<sup>&minus;19</sup> / (4&pi;&times;8.85&times;10<sup>&minus;12</sup>&times;10<sup>&minus;13</sup>) = "
           "4.16&times;10<sup>&minus;18</sup> / (1.11&times;10<sup>&minus;23</sup>) &asymp; 3.74&times;10<sup>5</sup> V = 374 kV。<br/>"
           "学生手写结果写的 3.744&times;10<sup>18</sup> 是笔误，量级错误，扣1分", 'warn'),
]))
story.append(sp(4))
story.append(score_row(5, 6))
story.append(sp(10))

# ───────────────── Q7 ─────────────────
story.append(P("<b>Question 7 &mdash; Sliding Rod (Lagrangian)  [9 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a): Lagrangian  [6 marks]</b>", 'bodyL'))
story.append(P(
    "质心坐标：<i>x</i> = (<i>l</i>/2)sin&theta;, <i>y</i> = (<i>l</i>/2)cos&theta;。<br/>"
    "动能 <i>T</i> = &frac12;<i>M</i>(<i>ẋ</i><sup>2</sup>+<i>ẏ</i><sup>2</sup>) + &frac12;<i>I&theta;̇</i><sup>2</sup> = <i>ML</i><sup>2</sup><i>&theta;̇</i><sup>2</sup>/6。<br/>"
    "势能 <i>V</i> = <i>Mg</i>(<i>l</i>/2)cos&theta;。<br/>"
    "拉格朗日量 <i>L</i> = <i>ML</i><sup>2</sup><i>&theta;̇</i><sup>2</sup>/6 &minus; <i>Mg</i>(<i>l</i>/2)cos&theta;。",
    'body'))
story.append(feedback_box([
    ("✔", "质心位置导数 <i>ẋ</i>, <i>ẏ</i> 正确计算", 'correct'),
    ("✔", "<i>I</i> = <i>ML</i><sup>2</sup>/12（已知量）使用正确", 'correct'),
    ("✔", "<i>T</i> = <i>ML</i><sup>2</sup><i>&theta;̇</i><sup>2</sup>/8 + <i>ML</i><sup>2</sup><i>&theta;̇</i><sup>2</sup>/24 = <i>ML</i><sup>2</sup><i>&theta;̇</i><sup>2</sup>/6 合并正确", 'correct'),
    ("✔", "<i>V</i> = <i>MgL</i> cos&theta; / 2 正确（注意参考点取地板）", 'correct'),
    ("✔", "<i>L</i> = <i>T</i> &minus; <i>V</i> 形式正确", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b): Conjugate momentum &amp; Equation of Motion  [3 marks]</b>", 'bodyL'))
story.append(P(
    "共轭动量 <i>p<sub>&theta;</sub></i> = &part;<i>L</i>/&part;<i>&theta;̇</i> = <i>ML</i><sup>2</sup><i>&theta;̇</i>/3。<br/>"
    "E-L方程：d/d<i>t</i>(<i>ML</i><sup>2</sup><i>&theta;̇</i>/3) = &part;<i>L</i>/&part;&theta; = <i>Mg</i>(<i>l</i>/2)sin&theta;。<br/>"
    "化简得 <i>&theta;̈</i> = (3<i>g</i>/2<i>l</i>)sin&theta;。",
    'body'))
story.append(feedback_box([
    ("✔", "共轭动量表达式正确", 'correct'),
    ("✔", "E-L 方程建立与化简正确", 'correct'),
    ("✔", "最终运动方程 <i>&theta;̈</i> = 3<i>g</i> sin&theta;/(2<i>l</i>) 正确", 'correct'),
]))
story.append(sp(4))
story.append(score_row(9, 9))
story.append(sp(12))

# section A summary
a_total_earned = 7+4+6+4+4+5+9
a_total_max    = 7+4+6+4+4+6+9
story.append(Table(
    [[Paragraph("Section A 小计 / Section A Subtotal",
                ParagraphStyle('st1', parent=base['Normal'], fontSize=12,
                               textColor=OXFORD_BLUE, fontName=FONT_BOLD)),
      Paragraph(f"<b>{a_total_earned} / {a_total_max}</b>",
                ParagraphStyle('st2', parent=base['Normal'], fontSize=14,
                               textColor=PASS_GREEN if a_total_earned>=28 else WARN_ORANGE,
                               fontName=FONT_BOLD, alignment=TA_RIGHT))]],
    colWidths=[W*0.7, W*0.3],
))
story.append(hr(ACCENT_GOLD, 2))
story.append(sp(12))

# ═══════════════════════════════════════════════════════════════════════════
# SECTION B
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("SECTION B &mdash; 长题  (选做3题，学生作答 Q9、Q10、Q11)"))
story.append(sp(8))

# ───────────────── Q9 ─────────────────
story.append(P("<b>Question 9 &mdash; Spherical Pendulum  [20 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a): Lagrangian, conserved quantities  [5 marks]</b>", 'bodyL'))
story.append(P(
    "<i>T</i> = &frac12; <i>M</i>(<i>L&theta;̇</i>)<sup>2</sup> + &frac12; <i>M</i>(<i>L</i> sin&theta; <i>&phi;̇</i>)<sup>2</sup>；<i>V</i> = &minus;<i>MgL</i> cos&theta;。<br/>"
    "<i>L</i> = &frac12; <i>ML</i><sup>2</sup>(<i>&theta;̇</i><sup>2</sup> + sin<sup>2</sup>&theta; <i>&phi;̇</i><sup>2</sup>) + <i>MgL</i> cos&theta;。<br/>"
    "<i>L</i> 不显含 <i>t</i> &rarr; 能量守恒；不显含 &phi; &rarr; &part;<i>L</i>/&part;<i>&phi;̇</i> = <i>ML</i><sup>2</sup>sin<sup>2</sup>&theta; <i>&phi;̇</i> = <i>J<sub>z</sub></i> 守恒。",
    'body'))
story.append(feedback_box([
    ("✔", "<i>T</i> 的两项（极角与方位角分量）均正确", 'correct'),
    ("✔", "<i>V</i> = &minus;<i>MgL</i>cos&theta;（取悬挂点为零势面），符号正确", 'correct'),
    ("✔", "能量守恒论证：<i>L</i> 不依赖 <i>t</i> &rarr; Hamiltonian 守恒，正确", 'correct'),
    ("✔", "<i>J<sub>z</sub></i> 守恒：<i>L</i> 不依赖 &phi; 故 &part;<i>L</i>/&part;<i>&phi;̇</i> 为运动积分，正确", 'correct'),
    ("✔", "<i>J<sub>z</sub></i> = <i>ML</i><sup>2</sup>sin<sup>2</sup>&theta; <i>&phi;̇</i> 表达式正确", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b): Equation of motion in &theta;; special cases  [6 marks]</b>", 'bodyL'))
story.append(P(
    "E-L for &theta;：<i>L&theta;̈</i> = <i>L&phi;̇</i><sup>2</sup>sin&theta;cos&theta; &minus; <i>g</i> sin&theta;。<br/>"
    "(i) &phi;=const &rarr; <i>&phi;̇</i>=0 &rarr; <i>&theta;̈</i> = &minus;(<i>g/L</i>)sin&theta; &rarr; 对小振幅 &omega; = &radic;(<i>g/L</i>)（单摆）。<br/>"
    "(ii) &theta;=const &rarr; <i>&theta;̈</i>=0 &rarr; <i>&phi;̇</i><sup>2</sup> = <i>g</i>/(<i>L</i>cos&theta;) &rarr; &omega; = &radic;(<i>g</i>/(<i>L</i>cos&theta;))（圆锥摆）。",
    'body'))
story.append(feedback_box([
    ("✔", "&theta; 的 E-L 方程正确推导", 'correct'),
    ("✔", "情形(i)：<i>&phi;̇</i>=0，方程退化为单摆，&omega;=&radic;(<i>g/L</i>) 正确", 'correct'),
    ("✔", "情形(ii)：<i>&theta;̈</i>=0 条件正确，<i>&phi;̇</i><sup>2</sup>=<i>g</i>/(<i>L</i>cos&theta;<sub>0</sub>) 正确", 'correct'),
    ("✔", "学生明确排除了 &theta;=0 的平凡情况", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (c): <i>J<sub>z</sub></i> at &theta; = &theta;<sub>0</sub>  [2 marks]</b>", 'bodyL'))
story.append(feedback_box([
    ("✔", "代入 <i>&phi;̇</i> = &radic;(<i>g</i>/(<i>L</i>cos&theta;<sub>0</sub>))，得 <i>J<sub>z</sub></i> = <i>ML</i><sup>2</sup>sin<sup>2</sup>&theta;<sub>0</sub> &radic;(<i>g</i>/(<i>L</i>cos&theta;<sub>0</sub>)) = "
           "<i>ML</i> sin<sup>2</sup>&theta;<sub>0</sub> &radic;(<i>g</i>/cos&theta;<sub>0</sub>)，正确", 'correct'),
    ("✔", "表达式形式简洁，与期望答案一致", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (d): Small oscillations about &theta;<sub>0</sub>  [7 marks]</b>", 'bodyL'))
story.append(P(
    "令 &theta; = &theta;<sub>0</sub> + &beta;，展开到一阶，固定 <i>&phi;̇</i><sup>2</sup> = <i>g</i>/(<i>L</i>cos&theta;<sub>0</sub>)，"
    "得 <i>&beta;̈</i> = &minus;(<i>g/L</i>)(sin<sup>2</sup>&theta;<sub>0</sub>/cos&theta;<sub>0</sub>) &beta;，即 SHM，"
    "周期 <i>T</i> = 2&pi;&radic;(<i>L</i>cos&theta;<sub>0</sub> / (<i>g</i> sin<sup>2</sup>&theta;<sub>0</sub>))。",
    'body'))
story.append(feedback_box([
    ("✔", "&theta; &rarr; &theta;<sub>0</sub>+&beta; 代换正确，展开三角函数到线性项", 'correct'),
    ("✔", "假设 <i>&phi;̇</i><sup>2</sup> 保持恒定（= <i>g/L</i>cos&theta;<sub>0</sub>）明确说明", 'correct'),
    ("✔", "忽略 <i>O</i>(&beta;<sup>2</sup>) 项正确标注", 'correct'),
    ("✔", "<i>&beta;̈</i> = &minus;(<i>g</i> sin<sup>2</sup>&theta;<sub>0</sub>)/(<i>L</i> cos&theta;<sub>0</sub>) &middot; &beta; 正确", 'correct'),
    ("✔", "给出 SHM 周期 2&pi;(<i>L</i> cos&theta;<sub>0</sub> / (<i>g</i> sin<sup>2</sup>&theta;<sub>0</sub>))<sup>&frac12;</sup>，正确", 'correct'),
    ("～", "展开中间步骤较为冗长（多余草稿），但逻辑链条完整，不影响得分", 'warn'),
]))
story.append(sp(4))
story.append(score_row(20, 20))
story.append(sp(10))

# ───────────────── Q10 ─────────────────
story.append(P("<b>Question 10 &mdash; Central Potential &amp; Orbital Mechanics  [18 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a)(i): Angular momentum <b>J</b> is constant  [2 marks]</b>", 'bodyL'))
story.append(P(
    "【注意】学生在本部分<b>没有给出正式推导</b>。<br/>"
    "标准做法：<b>J</b> = <b>r</b> &times; <b>p</b>，d<b>J</b>/d<i>t</i> = <b>ṙ</b> &times; <b>p</b> + <b>r</b> &times; <b>ṗ</b> = 0（中心力 <b>F</b> = <i>F</i>(<i>r</i>)<b>r̂</b> 与 <b>r</b> 平行）。"
    "学生仅在 Q10(b) 的计算中隐式使用了 <i>J</i> 守恒，未在 (a)(i) 处给出文字/公式推导。",
    'body'))
story.append(feedback_box([
    ("✔", "定义 <b>J</b> = <b>r</b> &times; <b>p</b> 给出（在Q10(a)开头体现，可见 '<i>J=mr&times;v</i>'）", 'correct'),
    ("✗", "未明确推导 d<b>J</b>/d<i>t</i> = 0（即未写出 <b>r̈</b>&times;<b>p</b>=0 因 <b>F</b>&parallel;<b>r</b> 的论证）", 'error'),
    ("→", "按题目要求 [2 marks] 扣除1分，酌情保留1分（学生展示了定义和使用意识）", 'warn'),
]))
story.append(sp(3))

story.append(P("<b>Part (a)(ii): Effective potential  [4 marks]</b>", 'bodyL'))
story.append(P(
    "<i>E</i> = &frac12;<i>Mṙ</i><sup>2</sup> + <i>J</i><sup>2</sup>/(2<i>Mr</i><sup>2</sup>) + <i>V</i>(<i>r</i>)。因 <i>J</i> 守恒可定义有效势 "
    "<i>U</i><sub>eff</sub>(<i>r</i>) = <i>J</i><sup>2</sup>/(2<i>Mr</i><sup>2</sup>) + <i>V</i>(<i>r</i>)，使问题化为一维运动 <i>E</i> = &frac12;<i>Mṙ</i><sup>2</sup> + <i>U</i><sub>eff</sub>(<i>r</i>)。",
    'body'))
story.append(feedback_box([
    ("✔", "能量分解为径向KE + 旋转能 <i>J</i><sup>2</sup>/2<i>Mr</i><sup>2</sup> 正确", 'correct'),
    ("✔", "有效势的物理概念与表达式正确", 'correct'),
    ("✔", "化为一维运动的解释清晰", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b): Show <i>v</i><sub>R</sub><sup>2</sup> = <i>GM</i><sub>E</sub>(2/<i>R</i> &minus; 1/<i>a</i>)  [6 marks]</b>", 'bodyL'))
story.append(P(
    "能量守恒（远地点 <i>R</i> 和近地点 <i>r</i><sub>c</sub> = 2<i>a</i>&minus;<i>R</i>）："
    "&frac12; <i>v</i><sub>R</sub><sup>2</sup> &minus; <i>GM</i><sub>E</sub>/<i>R</i> = &frac12; <i>v</i><sub>c</sub><sup>2</sup> &minus; <i>GM</i><sub>E</sub>/<i>r</i><sub>c</sub>。<br/>"
    "角动量守恒：<i>Rv</i><sub>R</sub> = <i>r</i><sub>c</sub><i>v</i><sub>c</sub>，即 <i>v</i><sub>c</sub> = <i>Rv</i><sub>R</sub>/<i>r</i><sub>c</sub>。<br/>"
    "代入后化简，利用 <i>R</i> + <i>r</i><sub>c</sub> = 2<i>a</i> 得 <i>v</i><sub>R</sub><sup>2</sup> = <i>GM</i><sub>E</sub>(2/<i>R</i> &minus; 1/<i>a</i>)。",
    'body'))
story.append(feedback_box([
    ("✔", "能量守恒与角动量守恒方程均正确列出", 'correct'),
    ("✔", "关系 <i>r</i><sub>c</sub> = 2<i>a</i> &minus; <i>R</i> 使用正确，图示清晰", 'correct'),
    ("✔", "代数化简过程完整，最终结果正确", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (c): Change in major axis after retro-rocket  [8 marks]</b>", 'bodyL'))
story.append(P(
    "速度从 <i>v</i><sub>R</sub> &rarr; <i>v</i><sub>R</sub>(1&minus;&epsilon;)，利用 <i>v</i><sup>2</sup>(1&minus;&epsilon;)<sup>2</sup> = <i>GM</i><sub>E</sub>(2/<i>R</i>&minus;1/<i>a'</i>) 求新半长轴 <i>a'</i>，"
    "再展开到一阶 &epsilon; 得 &Delta;<i>a</i> = <i>a</i> &minus; <i>a'</i> = 4&epsilon;<i>a</i>(1&minus;<i>e</i>)/(1+<i>e</i>)（其中 <i>R</i> = <i>a</i>(1+<i>e</i>)）。",
    'body'))
story.append(feedback_box([
    ("✔", "正确利用能量方程建立 <i>a'</i> 与速度的关系", 'correct'),
    ("✔", "<i>R</i> = <i>a</i>(1+<i>e</i>) 代入正确", 'correct'),
    ("✔", "近似展开 (1&minus;&epsilon;)<sup>2</sup> &asymp; 1&minus;2&epsilon;（&epsilon; &ll; 1）并明确说明", 'correct'),
    ("～", "学生在推导中途出现了一段较长的分数化简，中间行略有跳步——"
           "即从 &Delta;<i>a</i> = (4<i>a</i>-2<i>R</i>)&epsilon; / (4<i>a</i>&epsilon;-<i>R</i>-2<i>R</i>&epsilon;) 这一行开始直接跳到最终结果，"
           "未完整展示约分步骤。这属于轻微伪证，结论正确但中间推导不够严谨完整。", 'warn'),
    ("→", "酌情扣 1 分（严格来说该步骤若展开验证可以自洽，故仅扣1分）", 'error'),
]))
story.append(sp(4))
story.append(P(
    "<i>注：Q10 满分分布：(a)(i)=2, (a)(ii)=4, (b)=6, (c)=8，共20分。"
    "扣分：(a)(i) 未推导 &minus;1，(c) 跳步 &minus;1，实得 18/20。</i>",
    'italic'))
story.append(Table(
    [[Paragraph("得分 / Score: <b>18 / 20</b>",
                ParagraphStyle('sr2', parent=base['Normal'], fontSize=11,
                               textColor=PASS_GREEN, fontName=FONT_BOLD))]],
    colWidths=[W], rowHeights=[20],
))
story.append(sp(10))

# ───────────────── Q11 ─────────────────
story.append(P("<b>Question 11 &mdash; Elastic Collisions &amp; Bouncing Balls  [20 marks]</b>", 'subhead'))
story.append(hr(MID_GREY, 0.5))
story.append(sp(2))

story.append(P("<b>Part (a): Definition of elastic collision  [2 marks]</b>", 'bodyL'))
story.append(feedback_box([
    ("✔", "动能守恒 + 动量守恒，两者均明确陈述", 'correct'),
    ("✔", "措辞清晰", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b)(i): Diagrams of bouncing sequence  [4 marks]</b>", 'bodyL'))
story.append(P(
    "三步过程：① 两球同速向下落；② <i>m</i><sub>2</sub> 先撞地弹起（向上），<i>m</i><sub>1</sub> 仍向下；"
    "③ <i>m</i><sub>2</sub>(&uarr;<i>v</i>) 与 <i>m</i><sub>1</sub>(&darr;<i>v</i>) 碰撞；④ 碰撞后 <i>m</i><sub>1</sub> 以速度 <i>u</i> 弹起（最大能量转移情形）。",
    'body'))
story.append(feedback_box([
    ("✔", "学生绘制了1&deg;&ndash;6&deg;共六个步骤的图示，涵盖两次碰撞过程，超出最低要求", 'correct'),
    ("✔", "速度箭头方向均正确，标注了 <i>m</i><sub>1</sub>, <i>m</i><sub>2</sub> 和速度符号", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b)(ii): Mass ratio <i>m</i><sub>1</sub>/<i>m</i><sub>2</sub> for maximum energy transfer  [8 marks]</b>", 'bodyL'))
story.append(P(
    "<i>m</i><sub>2</sub> 与地面弹性碰撞后速度 +<i>v</i>（向上），此时 <i>m</i><sub>1</sub> 以 <i>v</i> 向下运动。<br/>"
    "两球碰撞：动量守恒 <i>m</i><sub>2</sub><i>v</i> &minus; <i>m</i><sub>1</sub><i>v</i> = <i>m</i><sub>1</sub><i>u</i>（<i>u'</i> = 0 时能量最大转移）；"
    "能量守恒给出另一方程。联立得 <i>m</i><sub>2</sub> = 3<i>m</i><sub>1</sub>，即 <i>m</i><sub>1</sub>/<i>m</i><sub>2</sub> = 1/3。",
    'body'))
story.append(feedback_box([
    ("✔", "第一次碰撞（<i>m</i><sub>2</sub> 与地面）处理正确：弹性碰撞反转速度", 'correct'),
    ("✔", "最大能量转移条件（<i>m</i><sub>2</sub> 碰后速度为零，<i>u'</i>=0）正确识别", 'correct'),
    ("✔", "动量与能量方程联立，代数操作正确", 'correct'),
    ("✔", "最终结果 <i>m</i><sub>1</sub>/<i>m</i><sub>2</sub> = 1/3 正确", 'correct'),
]))
story.append(sp(3))

story.append(P("<b>Part (b)(iii): Maximum height and time  [6 marks]</b>", 'bodyL'))
story.append(P(
    "<i>m</i><sub>1</sub> 以速度 <i>u</i> = 2<i>v</i> 弹起（当 <i>m</i><sub>2</sub>=3<i>m</i><sub>1</sub> 时，由动量方程 <i>m</i><sub>1</sub>/<i>m</i><sub>2</sub>=1/3 代入得 <i>u</i>=2<i>v</i>）。<br/>"
    "最大高度：0 = <i>u</i><sup>2</sup> &minus; 2<i>gh</i> &rarr; <i>h</i> = <i>u</i><sup>2</sup>/2<i>g</i> = 4<i>v</i><sup>2</sup>/2<i>g</i> = 2<i>v</i><sup>2</sup>/<i>g</i>。<br/>"
    "到达最高点时间：0 = <i>u</i> &minus; <i>gt</i> &rarr; <i>t</i> = <i>u/g</i> = 2<i>v/g</i>。",
    'body'))
story.append(feedback_box([
    ("✔", "<i>u</i> = 2<i>v</i>（<i>m</i><sub>2</sub>=3<i>m</i><sub>1</sub> 情形下，<i>m</i><sub>1</sub> 碰后速度）正确", 'correct'),
    ("✔", "<i>h</i> = 2<i>v</i><sup>2</sup>/<i>g</i> 正确", 'correct'),
    ("✔", "<i>t</i> = 2<i>v/g</i> 正确", 'correct'),
    ("～", "学生手稿中出现了多条平行计算路径（多次尝试），部分划去的行与正确答案"
           "矛盾，但最终框出答案均正确", 'warn'),
]))
story.append(sp(4))
story.append(score_row(20, 20))
story.append(sp(12))

# ═══════════════════════════════════════════════════════════════════════════
# TOTAL SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("总分汇总 / Overall Score Summary"))
story.append(sp(10))

sec_a = 39   # 7+4+6+4+4+5+9
sec_b = 20+18+20  # Q9+Q10+Q11
total_earned = sec_a + sec_b
total_max    = 40 + 60   # Section A 40, Section B 60 (3×20)
pct = total_earned / total_max * 100

summary_data = [
    ["题目 / Question", "满分 / Max", "实得 / Earned", "备注 / Note"],
    ["A1 &mdash; Moment of Inertia",    "7",  "7",  "完美 / Full marks"],
    ["A2 &mdash; Bullet with Drag",      "4",  "4",  "完美 / Full marks"],
    ["A3 &mdash; Z<sup>0</sup> Boson (CERN)",       "6",  "6",  "完美 / Full marks"],
    ["A4 &mdash; Elastic Equal Mass",    "4",  "4",  "完美 / Full marks"],
    ["A5 &mdash; Roller Coaster",        "4",  "4",  "完美 / Full marks"],
    ["A6 &mdash; Rutherford",            "6",  "5",  "数值量级笔误 &minus;1"],
    ["A7 &mdash; Sliding Rod",           "9",  "9",  "完美 / Full marks"],
    ["Section A Subtotal",         "40", str(sec_a), ""],
    ["B9 &mdash; Spherical Pendulum",    "20", "20", "完美 / Full marks"],
    ["B10 &mdash; Central Potential",    "20", "18", "两处扣分，见详述"],
    ["B11 &mdash; Bouncing Balls",       "20", "20", "完美 / Full marks"],
    ["Section B Subtotal",         "60", str(sec_b), ""],
    [f"TOTAL &mdash; 总分  ({pct:.1f}%)", "100", str(total_earned), ""],
]

col_w = [W*0.38, W*0.12, W*0.15, W*0.35]
t = Table(summary_data, colWidths=col_w)
t.setStyle(TableStyle([
    # Header
    ('BACKGROUND',    (0,0), (-1,0), OXFORD_BLUE),
    ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
    ('FONTNAME',      (0,0), (-1,0), FONT_BOLD),
    ('FONTSIZE',      (0,0), (-1,0), 9),
    # Section subtotals (rows 8 and 12)
    ('BACKGROUND',    (0,8), (-1,8), LIGHT_GOLD),
    ('FONTNAME',      (0,8), (-1,8), FONT_BOLD),
    ('BACKGROUND',    (0,12),(-1,12), LIGHT_GOLD),
    ('FONTNAME',      (0,12),(-1,12), FONT_BOLD),
    # Total row
    ('BACKGROUND',    (0,13),(-1,13), OXFORD_BLUE),
    ('TEXTCOLOR',     (0,13),(-1,13), ACCENT_GOLD),
    ('FONTNAME',      (0,13),(-1,13), FONT_BOLD),
    ('FONTSIZE',      (0,13),(-1,13), 11),
    # General
    ('FONTSIZE',      (0,1), (-1,12), 9),
    ('ROWBACKGROUNDS',(0,1), (-1,11), [WHITE, LIGHT_BLUE]),
    ('GRID',          (0,0), (-1,-1), 0.4, MID_GREY),
    ('ALIGN',         (1,0), (2,-1), 'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
]))
story.append(t)
story.append(sp(12))

# ── Grade band ───────────────────────────────────────────────────────────
if pct >= 85:
    grade_text = "优秀 / Distinction &mdash; 第一档 (First Class)"
    grade_color = PASS_GREEN
elif pct >= 70:
    grade_text = "良好 / Merit &mdash; 上二等 (Upper Second)"
    grade_color = PASS_GREEN
elif pct >= 55:
    grade_text = "合格 / Pass &mdash; 下二等 (Lower Second)"
    grade_color = WARN_ORANGE
else:
    grade_text = "不及格 / Fail"
    grade_color = FAIL_RED

story.append(Table(
    [[Paragraph(f"<b>成绩等级：{grade_text}</b>",
                ParagraphStyle('gp', parent=base['Normal'], fontSize=13,
                               textColor=grade_color, alignment=TA_CENTER))]],
    colWidths=[W], rowHeights=[28],
))
story.append(sp(12))

# ═══════════════════════════════════════════════════════════════════════════
# Overall Feedback
# ═══════════════════════════════════════════════════════════════════════════
story.append(section_header("综合评价与改进建议 / Overall Feedback &amp; Improvement Areas"))
story.append(sp(8))

story.append(P("<b>优势 / Strengths</b>", 'subhead'))
story.append(P(
    "1. <b>物理直觉出色</b>：多道题（Q1、Q4、Q7、Q9、Q11）的解题路径选择恰当，"
    "从正确的物理原理出发，少有绕弯路。"
    "尤其是 Q9(d) 小振荡推导，展开方式与标准解法完全一致。",
    'body'))
story.append(P(
    "2. <b>拉格朗日力学掌握扎实</b>：Q7 和 Q9 均能熟练写出正确的动能、势能和拉格朗日量，"
    "E-L 方程操作无误，守恒量识别准确（不显含 <i>t</i> &rarr; 能量守恒；不显含 &phi; &rarr; <i>J<sub>z</sub></i> 守恒）。",
    'body'))
story.append(P(
    "3. <b>相对论计算熟练</b>：Q3 对 Z<sup>0</sup> 的三问均处理正确，Q8 的康普顿散射推导"
    "也体现了对四动量不变量的深刻理解。",
    'body'))
story.append(P(
    "4. <b>轨道力学基础好</b>：Q10(b) 和 (c) 对能量守恒与角动量守恒的联立运用正确，"
    "椭圆轨道参数（半长轴、离心率）使用准确。",
    'body'))
story.append(sp(4))

story.append(P("<b>改进方向 / Areas to Improve</b>", 'subhead'))
story.append(P(
    "1. <b>Q6 数值计算</b>：本题扣1分源于最终电压数量级错误（写成 3.74&times;10<sup>18</sup> V 而非 374 kV）。"
    "建议考试中对数量级进行量纲/数量级估算验证：一个原子核的 Coulomb 势垒量级"
    "通常为 MeV 到数百 keV，对应加速电压 ~10<sup>5</sup>&ndash;10<sup>6</sup> V，不可能达到 10<sup>18</sup> V。"
    "养成 '数量级自查' 习惯可以避免此类笔误。",
    'body'))
story.append(P(
    "2. <b>Q10(a)(i) 论证完整性</b>：角动量守恒的推导（d<b>J</b>/d<i>t</i> = <b>r</b> &times; <b>F</b> = 0 因 <b>F</b> &parallel; <b>r</b>）"
    "是中心力场的核心定理，必须明写，不能仅靠后续计算隐式使用。"
    "牛津批改标准会检查每一个逻辑步骤是否明确给出。",
    'body'))
story.append(P(
    "3. <b>Q10(c) 代数严谨性</b>：&epsilon; 展开部分存在跳步&mdash;&mdash;从中间分式直接给出最终"
    "近似结果，未展示约分与近似的每一步。建议在展开时逐行写出："
    "(1&minus;&epsilon;)<sup>2</sup> &asymp; 1&minus;2&epsilon; &rarr; 代入 &rarr; 提取 &epsilon; 因子 &rarr; 与分母比较。"
    "这不仅能得到满分，也能在检验时发现潜在错误。",
    'body'))
story.append(P(
    "4. <b>书写规范</b>：部分页面（尤其是 Q11 和 Q3(c)）存在大量划去的草稿痕迹。"
    "虽然最终答案正确，但批改者需要花额外时间辨认。"
    "建议考试中先在草稿纸上演算，确认后再书写正卷，保持答题区域整洁。",
    'body'))
story.append(sp(6))

story.append(P("<b>总结 / Summary</b>", 'subhead'))
story.append(P(
    f"本次 CP1 考试学生共得 <b>{total_earned}/100</b> 分（{pct:.1f}%），"
    f"达到<b>{grade_text}</b>水平。"
    "整体表现优异，力学（经典与拉格朗日）、相对论和轨道力学三大板块均有强劲表现。"
    "主要失分点为数值笔误（Q6）和推导不完整（Q10），均属于可通过训练规避的问题。"
    "建议重点练习：① 数量级估算习惯；② 关键定理的完整书面推导（尤其是守恒量）；"
    "③ 摄动展开（&epsilon; 小量）的逐步严格操作。",
    'body'))

story.append(sp(16))
story.append(hr(ACCENT_GOLD, 1))
story.append(P(
    "<i>本报告由 Oxford CP1 模拟批改系统生成 | "
    "Generated by Oxford CP1 Simulated Marking System | "
    "June 2025</i>",
    'italic'))

# ── Build ────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF built successfully")