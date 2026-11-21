"""Generate the Concise 18-Page Final Academic Research Project Report (.docx and .pdf)."""

import os
import pandas as pd
import numpy as np
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# Page Setup: A4, 1 inch (2.54 cm) margins
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True

    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Experimental Analysis and Optimization of Greedy Graph Coloring Algorithms | JIIT Noida")
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(9.5)
    hrun.font.italic = True
    hrun.font.color.rgb = RGBColor(90, 90, 90)

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun1 = fp.add_run("Page ")
    frun1.font.name = "Times New Roman"
    frun1.font.size = Pt(10)

    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    r_page = fp.add_run()
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(10)
    r_page._r.append(fldChar1)
    r_page._r.append(instrText)
    r_page._r.append(fldChar2)
    r_page._r.append(fldChar3)

    frun2 = fp.add_run(" of ")
    frun2.font.name = "Times New Roman"
    frun2.font.size = Pt(10)

    fldChar4 = OxmlElement("w:fldChar")
    fldChar4.set(qn("w:fldCharType"), "begin")
    instrText2 = OxmlElement("w:instrText")
    instrText2.set(qn("xml:space"), "preserve")
    instrText2.text = "NUMPAGES"
    fldChar5 = OxmlElement("w:fldChar")
    fldChar5.set(qn("w:fldCharType"), "separate")
    fldChar6 = OxmlElement("w:fldChar")
    fldChar6.set(qn("w:fldCharType"), "end")
    r_numpages = fp.add_run()
    r_numpages.font.name = "Times New Roman"
    r_numpages.font.size = Pt(10)
    r_numpages._r.append(fldChar4)
    r_numpages._r.append(instrText2)
    r_numpages._r.append(fldChar5)
    r_numpages._r.append(fldChar6)

# Base Normal Style (12pt Times New Roman, 1.5 spacing, justified)
normal_style = doc.styles["Normal"]
normal_style.font.name = "Times New Roman"
normal_style.font.size = Pt(12)
normal_style.paragraph_format.line_spacing = 1.5
normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
normal_style.paragraph_format.space_after = Pt(3)

h1_style = doc.styles["Heading 1"]
h1_style.font.name = "Times New Roman"
h1_style.font.size = Pt(16)
h1_style.font.bold = True
h1_style.font.color.rgb = RGBColor(0, 0, 0)
h1_style.paragraph_format.space_before = Pt(8)
h1_style.paragraph_format.space_after = Pt(3)
h1_style.paragraph_format.line_spacing = 1.2

h2_style = doc.styles["Heading 2"]
h2_style.font.name = "Times New Roman"
h2_style.font.size = Pt(14)
h2_style.font.bold = True
h2_style.font.color.rgb = RGBColor(0, 0, 0)
h2_style.paragraph_format.space_before = Pt(6)
h2_style.paragraph_format.space_after = Pt(2)
h2_style.paragraph_format.line_spacing = 1.2

h3_style = doc.styles["Heading 3"]
h3_style.font.name = "Times New Roman"
h3_style.font.size = Pt(12)
h3_style.font.bold = True
h3_style.font.color.rgb = RGBColor(0, 0, 0)
h3_style.paragraph_format.space_before = Pt(4)
h3_style.paragraph_format.space_after = Pt(2)
h3_style.paragraph_format.line_spacing = 1.2

def set_cell_shading(cell, color_hex):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), color_hex)
    shading.set(qn("w:val"), "clear")
    cell._tc.get_or_add_tcPr().append(shading)

def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    trPr.append(tblHeader)

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    cantSplit = OxmlElement("w:cantSplit")
    trPr.append(cantSplit)

def add_chapter_heading(text):
    h = doc.add_heading(text, level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for r in h.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_sub_heading(text, level=2):
    h = doc.add_heading(text, level=level)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sz = Pt(14) if level == 2 else Pt(12)
    for r in h.runs:
        r.font.name = "Times New Roman"
        r.font.size = sz
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def add_p(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=Pt(3)):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = space_after
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
    return p

def add_equation(eq_text, eq_num=""):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.25
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(eq_text)
    r.italic = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.5)
    if eq_num:
        r2 = p.add_run(f"      ({eq_num})")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11.5)
    return p

def add_bullet_item(prefix_bold, body_text):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.4
    p.paragraph_format.space_after = Pt(2)
    if prefix_bold:
        r1 = p.add_run(prefix_bold)
        r1.bold = True
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)
    r2 = p.add_run(body_text)
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    return p

def add_pseudocode_box(title_text, lines, font_sz=Pt(8.5)):
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(1)
    p_cap.paragraph_format.keep_with_next = True
    rc = p_cap.add_run(title_text)
    rc.bold = True
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(10.5)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, "F8F9FA")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.05
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    for i, line in enumerate(lines):
        r = p.add_run(line + ("\n" if i < len(lines) - 1 else ""))
        r.font.name = "Consolas"
        r.font.size = font_sz

def add_styled_table(caption, headers, rows, font_size=Pt(8.5)):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(1)
    p_cap.paragraph_format.keep_with_next = True
    rc = p_cap.add_run(caption)
    rc.bold = True
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(10)

    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_repeat_table_header(table.rows[0])
    prevent_row_split(table.rows[0])

    for c_idx, h in enumerate(headers):
        cell = table.rows[0].cells[c_idx]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, "1F4E79")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(str(h))
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = font_size
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(rows):
        row = table.rows[r_idx + 1]
        prevent_row_split(row)
        bg = "F2F5F9" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if bg != "FFFFFF":
                set_cell_shading(cell, bg)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = font_size

    return table

def add_side_by_side_figures(img1, cap1, img2, cap2, width_each=2.95):
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    prevent_row_split(tbl.rows[0])
    prevent_row_split(tbl.rows[1])
    for r_ in tbl.rows:
        for c_ in r_.cells:
            for p_ in c_.paragraphs:
                p_.paragraph_format.keep_with_next = True
    for p_ in tbl.rows[1].cells[0].paragraphs:
        p_.paragraph_format.keep_with_next = False
    for p_ in tbl.rows[1].cells[1].paragraphs:
        p_.paragraph_format.keep_with_next = False
    for idx, (img, cap) in enumerate([(img1, cap1), (img2, cap2)]):
        c_img = tbl.rows[0].cells[idx]
        c_img.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p_i = c_img.paragraphs[0]
        p_i.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_i.paragraph_format.space_before = Pt(1)
        p_i.paragraph_format.space_after = Pt(1)
        p_i.paragraph_format.line_spacing = 1.0
        p_i.paragraph_format.keep_with_next = True
        if os.path.exists(img):
            p_i.add_run().add_picture(img, width=Inches(width_each))

        c_cap = tbl.rows[1].cells[idx]
        p_c = c_cap.paragraphs[0]
        p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_c.paragraph_format.line_spacing = 1.05
        p_c.paragraph_format.space_before = Pt(1)
        p_c.paragraph_format.space_after = Pt(2)
        rc = p_c.add_run(cap)
        rc.bold = True
        rc.italic = True
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(8.5)

def add_figure(img_path, caption_text, width_inches=4.2):
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2)
    p_img.paragraph_format.space_after = Pt(1)
    p_img.paragraph_format.line_spacing = 1.0
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=Inches(width_inches))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.line_spacing = 1.05
    p_cap.paragraph_format.space_after = Pt(2)
    rc = p_cap.add_run(caption_text)
    rc.bold = True
    rc.italic = True
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(9)

# ==============================================================================
# PAGE 1: COVER PAGE (Exact JIIT Format as provided in Synopsis)
# ==============================================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(6)
r = p.add_run("Advanced Algorithms Lab")
r.bold = True
r.italic = True
r.font.name = "Times New Roman"
r.font.size = Pt(18)
r.font.color.rgb = RGBColor(0, 0, 128)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(12)
r = p.add_run("Topic: Experimental Analysis and Optimization of\nGreedy Graph Coloring Algorithms")
r.bold = True
r.font.name = "Times New Roman"
r.font.size = Pt(15)

logo_path = r"H:\COLLEGE\5th Year\10TH SEM\TERM PAPER & SEMINAR\figures\jiit_logo.png"
if os.path.exists(logo_path):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.add_run().add_picture(logo_path, width=Inches(2.0))

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
r = p.add_run("Subject: Advanced Algorithms Lab [17M15CS111]")
r.font.name = "Times New Roman"
r.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
r = p.add_run("Department of Computer Science and Engineering")
r.font.name = "Times New Roman"
r.font.size = Pt(13)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(14)
r = p.add_run("Jaypee Institute of Information Technology, Sector 62, Noida\nAcademic Session: 2026–27")
r.font.name = "Times New Roman"
r.font.size = Pt(13)

dt = doc.add_table(rows=5, cols=2)
dt.style = "Table Grid"
dt.alignment = WD_TABLE_ALIGNMENT.CENTER
for row in dt.rows:
    row.cells[0].width = Cm(4.8)
    row.cells[1].width = Cm(11.2)

cover_fields = [
    ("Document Title", "Final Academic Research Project Report"),
    ("Project Title", "Experimental Analysis and Optimization of Greedy Graph Coloring Algorithms"),
    ("Submitted To", "Dr. Taj Alam and Deepti Singh\nAssistant Professors, Department of CSE, JIIT"),
    ("Submitted By", "Sabeeh Ahsan (22803006)\nHarleen Kaur (22803009)\nTanmay Butta (22803014)\nAryan Khanna (22803028)"),
    ("Academic Session", "2026–27"),
]
for i, (k_str, v_str) in enumerate(cover_fields):
    c0 = dt.rows[i].cells[0]
    c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    set_cell_shading(c0, "1F4E79")
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.line_spacing = 1.2
    r0 = p0.add_run(k_str)
    r0.bold = True
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(12)
    r0.font.color.rgb = RGBColor(255, 255, 255)

    c1 = dt.rows[i].cells[1]
    c1.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.line_spacing = 1.2
    r1 = p1.add_run(v_str)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)

doc.add_page_break()

# ==============================================================================
# PAGE 2: ABSTRACT
# ==============================================================================
add_chapter_heading("Abstract")
p_a1 = add_p(
    "The Graph Vertex Coloring Problem (GCP) is a foundational problem in combinatorial optimization and algorithmic "
    "graph theory with direct real-world applications in examination timetabling, compiler register allocation, wireless "
    "frequency assignment, and planar map coloring. Formally, given a simple undirected graph G = (V, E) with n = |V| "
    "vertices and m = |E| edges, a proper vertex coloring assigns a discrete color label to every vertex such that no "
    "two adjacent vertices share an identical color. Determining the minimum number of colors required—termed the "
    "chromatic number χ(G)—is famously NP-hard, and even approximating χ(G) within a factor of n^(1-ε) for any ε > 0 is "
    "computationally intractable unless P = NP. Consequently, polynomial-time greedy vertex coloring heuristics remain "
    "the primary practical methodology for coloring medium-to-large graphs."
)
p_a2 = add_p(
    "This research project presents a rigorous theoretical and empirical investigation of four greedy graph coloring "
    "algorithms of progressive structural sophistication implemented in our custom Python package (gcol): (1) Basic "
    "Greedy (First-Fit) coloring, (2) the static degree-ordered Welsh-Powell algorithm, (3) Brélaz's dynamic Degree of "
    "Saturation (DSATUR) algorithm implemented with a lazy-deletion binary priority queue, and (4) an Improved DSATUR "
    "algorithm inspired by the preprocessing and reduction paradigms of Schidler and Szeider (2023) [4] and Sewell's "
    "maximum-constraint tie-breaking rule [7]. Specifically, our Improved DSATUR integrates multi-start greedy maximal "
    "clique lower-bound discovery (ω_g ≤ ω(G) ≤ χ(G)) with clique pre-coloring, iterative low-degree core peeling "
    "(deg(v) < LB), pivot-accelerated non-adjacent vertex domination removal (N(u) ⊆ N(v)), and Sewell's shared-available-color "
    "tie-breaking, alongside an interactive web backend (app.py) and HTML5 Canvas visualization workbench (web/index.html)."
)
p_a3 = add_p(
    "We evaluate the four heuristics across 8 standard DIMACS benchmark graphs (myciel3, myciel5, queen5_5, queen8_8, "
    "jean, anna, huck, le450_15a) and 31 synthetic graph configurations spanning Erdős–Rényi G(n, p), Barabási–Albert "
    "scale-free networks, Random Geometric graphs, Cycle graphs, Complete graphs, and adversarial bipartite Crown "
    "graphs over 10 independent seeds, supplemented by an exact DSATUR-based Branch-and-Bound solver for small graphs "
    "(n ≤ 51) and a 6-variant ablation study. Experimental results confirm that dynamic saturation ordering reduces "
    "color usage by up to 51.87% over Basic Greedy on scale-free networks and 24.22% on le450_15a, while Improved "
    "DSATUR achieves a 100% vertex reduction prior to DSATUR on sparse real-world instances (anna, jean, huck) and "
    "lowers the mean coloring of queen8_8 to 11.00 (minimum 10 colors)."
)
for pa in (p_a1, p_a2, p_a3):
    pa.paragraph_format.line_spacing = 1.25
    pa.paragraph_format.space_after = Pt(4)

p_kw = add_p()
p_kw.paragraph_format.line_spacing = 1.25
p_kw.paragraph_format.space_after = Pt(2)
r_kw1 = p_kw.add_run("Keywords: ")
r_kw1.bold = True
r_kw1.font.name = "Times New Roman"
r_kw1.font.size = Pt(12)
r_kw2 = p_kw.add_run(
    "Graph Vertex Coloring, Chromatic Number, DSATUR, Welsh-Powell, Greedy Heuristics, Sewell Tie-Breaking, "
    "Vertex Domination Reduction, Clique Lower Bound, DIMACS Benchmarks, Interactive Web Visualization."
)
r_kw2.italic = True
r_kw2.font.name = "Times New Roman"
r_kw2.font.size = Pt(12)

doc.add_page_break()

# ==============================================================================
# PAGE 3: AUTOMATIC TABLE OF CONTENTS (ON ITS OWN SEPARATE PAGE)
# ==============================================================================
add_chapter_heading("Table of Contents")
p_toc = doc.add_paragraph()
p_toc.paragraph_format.line_spacing = 1.0
p_toc.paragraph_format.space_after = Pt(0)
fldToc1 = OxmlElement("w:fldChar")
fldToc1.set(qn("w:fldCharType"), "begin")
instrToc = OxmlElement("w:instrText")
instrToc.set(qn("xml:space"), "preserve")
instrToc.text = 'TOC \\o "1-2" \\h \\z \\u'
fldToc2 = OxmlElement("w:fldChar")
fldToc2.set(qn("w:fldCharType"), "separate")
fldToc3 = OxmlElement("w:fldChar")
fldToc3.set(qn("w:fldCharType"), "end")
r_toc = p_toc.add_run()
r_toc._r.append(fldToc1)
r_toc._r.append(instrToc)
r_toc._r.append(fldToc2)
r_toc._r.append(fldToc3)

doc.add_page_break()

# ==============================================================================
# CHAPTER 1: INTRODUCTION
# ==============================================================================
add_chapter_heading("Chapter 1: Introduction")

add_sub_heading("1.1 Background, Proper Coloring, and Chromatic Number", level=2)
add_p(
    "Let G = (V, E) be a simple undirected graph with vertex set V (n = |V|) and edge set E ⊆ {{u, v} : u, v ∈ V, u ≠ v} "
    "(m = |E|). For each v ∈ V, let N(v) = {u ∈ V : {u, v} ∈ E} denote its open neighborhood and d(v) = |N(v)| its "
    "degree, with maximum degree Δ(G) = max_{v ∈ V} d(v). A proper k-coloring is a mapping c : V → {0, 1, ..., k - 1} "
    "assigning colors such that adjacent vertices receive distinct colors. The minimum k admitting a proper coloring "
    "is the chromatic number χ(G), bounded below by the clique number ω(G) and above by Δ(G) + 1:"
)
add_equation("G = (V, E),   n = |V|,   m = |E|,   ∀{u, v} ∈ E: c(u) ≠ c(v),   ω(G) ≤ χ(G) = min k ≤ Δ(G) + 1", "1.1")

add_sub_heading("1.2 NP-Hardness, Greedy Heuristics, and Real-World Applications", level=2)
add_p(
    "While 2-colorability is decidable in O(n + m) time, k-colorability for k ≥ 3 is NP-complete (Karp, 1972 [1]), "
    "and approximating χ(G) within n^(1-ε) is NP-hard (Zuckerman, 2007 [6]). Because exact exponential algorithms "
    "fail to scale beyond small dense graphs, polynomial-time sequential greedy heuristics are essential in practice. "
    "Real-world applications directly modeled by vertex coloring include: (1) Examination Scheduling (courses as "
    "vertices, shared students as conflict edges, time slots as colors [3]); (2) Compiler Register Allocation "
    "(assigning live-range interference graphs of temporary variables to CPU registers [5]); (3) Wireless Frequency "
    "Assignment (allocating non-interfering channels to spatially proximate transmitters); and (4) Map Coloring and "
    "parallel scientific mesh partitioning."
)

add_sub_heading("1.3 Motivation, Scope, and Research Questions", level=2)
add_p(
    "This project investigates how static ordering (Welsh-Powell), dynamic saturation ordering (DSATUR), and "
    "preprocessing-driven enhancements inspired by Schidler and Szeider (2023) [4] perform across diverse topologies. "
    "Our scope covers custom data structures, four greedy algorithms, an exact Branch-and-Bound solver, and empirical "
    "evaluation addressing the three synopsis research questions: RQ1: How do different greedy vertex ordering "
    "strategies affect the quality and efficiency of graph coloring? RQ2: Can preprocessing and enhanced tie-breaking "
    "strategies improve DSATUR's performance on diverse graph families? RQ3: What are the empirical trade-offs "
    "between solution quality, execution time, and memory usage across different graph structures and densities?"
)

# ==============================================================================
# CHAPTER 2: PROBLEM STATEMENT AND RESEARCH OBJECTIVES
# ==============================================================================
add_chapter_heading("Chapter 2: Problem Statement and Research Objectives")

add_sub_heading("2.1 Problem Formulation and Role of Vertex Ordering", level=2)
add_p(
    "Given G = (V, E), our objective is to compute a proper coloring c : V → {0, ..., k - 1} that minimizes k, the "
    "approximation ratio ρ_χ = k / χ(G) (or clique lower-bound ratio ρ_ω = k / ω_g), execution time T(G), and peak "
    "memory M(G). In greedy coloring, vertices are colored sequentially along a permutation π = (v_1, ..., v_n) using "
    "the smallest feasible color. Because early color assignments are irrevocable, poor orderings force high color "
    "counts (up to n/2 colors on 2-chromatic Crown graphs). Dynamic ordering (DSATUR) mitigates this by selecting the "
    "vertex with maximum saturation degree sat(v), yet still faces challenges from tie-breaking ambiguity among "
    "equally saturated vertices, lack of clique pre-seeding, and redundant priority-queue overhead from low-degree or "
    "dominated peripheral vertices."
)

add_sub_heading("2.2 Research Objectives", level=2)
add_bullet_item("1. Modular Implementation: ", "Implement Basic Greedy, Welsh-Powell, Standard DSATUR (heap and naive), Improved DSATUR, and Exact Branch-and-Bound under identical conditions on a custom slot-based Graph class.")
add_bullet_item("2. Algorithmic Optimization: ", "Integrate multi-start greedy clique lower-bound pre-coloring, LB-core degree peeling, pivot-accelerated non-adjacent vertex domination reduction, and Sewell tie-breaking into Improved DSATUR.")
add_bullet_item("3. Rigorous Benchmarking: ", "Evaluate all four algorithms across 8 DIMACS instances and 5 synthetic graph families (plus adversarial Crown graphs) over 10 seeds, verifying complexity and component ablations.")

# ==============================================================================
# CHAPTER 3: LITERATURE REVIEW AND RELATED WORK
# ==============================================================================
add_chapter_heading("Chapter 3: Literature Review and Related Work")

add_sub_heading("3.1 Primary Paper (Schidler & Szeider, 2023) and Supporting Literature", level=2)
add_p(
    "Our primary reference is A. Schidler and S. Szeider, \"SAT-boosted Tabu Search for Coloring Massive Graphs\" "
    "(ACM JEA, 2023) [4], which introduces the SLIM framework combining DSATUR/I-DSATUR initial bounds, localized SAT "
    "recoloring, Tabu search, clique lower bounds, and preprocessing graph reductions (peeling vertices with d(v) < LB "
    "and removing dominated vertices). Distinction: Our project does NOT implement SLIM's SAT or Tabu solvers; instead, "
    "our Improved DSATUR adapts their polynomial-time clique lower-bounding, low-degree peeling, and vertex domination "
    "reductions into a constructive DSATUR pipeline enhanced with Sewell's tie-breaking rule [7]. "
    "Supporting foundations include Karp (1972) [1] for NP-completeness of k-coloring (k ≥ 3); Welsh and Powell (1967) "
    "[3] for static decreasing-degree ordering (χ(G) ≤ max_i min(d(v_i)+1, i)); Brélaz (1979) [2] for dynamic "
    "saturation degree (DSATUR) and clique-seeded Branch-and-Bound; Aslan and Baykan (2016) [8] for empirical DIMACS "
    "comparisons; and Lewis (2021) [5] and Sewell (1996) [7] for heap-based DSATUR and maximum-constraint tie-breaking."
)

lit_headers = ["Study", "Methodology & Algorithmic Contribution", "Findings & Limitations", "Relevance to Current Project"]
lit_rows = [
    ["Karp (1972) [1]", "Polynomial-time reduction from 3-SAT to k-Coloring.", "Proved k-coloring (k ≥ 3) is NP-complete.", "Theoretical justification for greedy heuristics."],
    ["Welsh & Powell (1967) [3]", "Static non-increasing degree sort prior to greedy coloring.", "Fast O(n log n + m); blind to dynamic color conflicts.", "Implemented as Algorithm 2 (welsh_powell.py)."],
    ["Brélaz (1979) [2]", "Dynamic selection by max saturation degree sat(v); B&B.", "Exact on bipartite/cycle graphs; arbitrary tie-breaking.", "Implemented as Algorithm 3 (dsatur.py) & Exact Solver."],
    ["Aslan & Baykan (2016) [8]", "Benchmarked FF, WP, DSATUR, RLF on DIMACS graphs.", "DSATUR balances quality and runtime best; no reductions.", "Motivates our multi-seed DIMACS & synthetic evaluation."],
    ["Lewis (2021) [5] & Sewell [7]", "Adversarial bipartite graphs, heap DSATUR, Sewell rule.", "Maximizing shared available colors resolves DSATUR ties.", "Basis for sewell_score() and Crown graph testing."],
    ["Schidler & Szeider (2023) [4]", "SLIM: Hybrid SAT + Tabu + Clique LB + Graph Reductions.", "LB degree peeling & domination shrink massive graphs.", "Primary basis for Improved DSATUR reductions & LB."]
]
add_styled_table("Table 3.1: Comparative Literature Review of Foundational and Modern Graph Coloring Studies", lit_headers, lit_rows, font_size=Pt(8.0))

# ==============================================================================
# CHAPTER 4: PROPOSED METHODOLOGY AND ALGORITHM DESIGN
# ==============================================================================
add_chapter_heading("Chapter 4: Proposed Methodology and Algorithm Design")

add_p(
    "Figure 4.1 illustrates the overall modular architecture of the custom gcol framework, and Figure 4.2 depicts the "
    "five-stage preprocessing and dynamic coloring pipeline of our proposed Improved DSATUR algorithm (adapted from "
    "the preprocessing paradigm of Schidler and Szeider [4] and Sewell's tie-breaking rule [7])."
)

add_side_by_side_figures(
    "Figures/diag1_architecture.png", "Figure 4.1: Overall Modular System Architecture of the gcol Graph Coloring Framework.",
    "Figures/diag7_improved_dsatur.png", "Figure 4.2: Five-Stage Pipeline of Improved DSATUR (Clique LB, Reductions [4] & Sewell Rule [7]).",
    width_each=3.05
)

add_sub_heading("4.1 Basic Greedy (First-Fit) and Welsh-Powell Algorithms", level=2)
add_p(
    "1. Basic Greedy (gcol/algorithms/greedy.py, Figure 4.3): Visits vertices in natural or seed-shuffled order "
    "π = input_order(n, seed) and assigns each vertex v the smallest non-negative integer color absent from its "
    "already-colored neighbors: c(v) = first_fit(adj[v], colors) = min{c ≥ 0 : c ∉ {c(u) : u ∈ N(v)}} [5]. Time: O(n + m); Space: O(n).\n"
    "2. Welsh-Powell (gcol/algorithms/welsh_powell.py, Figure 4.4): Computes static degree order π_WP by sorting "
    "vertices by (-d(v), rank[v]) in O(n log n) time [3], then applies First-Fit greedy coloring (welsh_powell_first_fit, "
    "O(n log n + m)) or classical color-class sweep (welsh_powell, O(n log n + k·n + m)), verified equivalent in unit tests."
)

add_sub_heading("4.2 Standard DSATUR and Improved DSATUR", level=2)
add_p(
    "3. Standard DSATUR (gcol/algorithms/dsatur.py, Figure 4.5): Dynamically tracks each uncolored vertex's saturation "
    "degree sat(v) = |nbr_colors[v]| and uncolored degree udeg(v) = |N(v) ∩ U| [2], selecting v* = arg max_{v ∈ U} "
    "(sat(v), udeg(v), -rank[v]). Our heap engine (dsatur_engine) uses Python's heapq with lazy deletion: new entries "
    "(-sat(u), -udeg(u), rank[u], u) are pushed only when sat(u) strictly increases (at most m times), while stale udeg "
    "entries are refreshed on pop, achieving O((n + m) log n) time and O(n + m) space (matching dsatur_naive's O(n² + m) output).\n"
    "4. Improved DSATUR (gcol/algorithms/improved_dsatur.py, Figure 4.2): Integrates three toggleable enhancements "
    "evaluated via the multi-seed comparative pipeline in Figure 4.6:\n"
    "  (a) Multi-Level Sewell Tie-Breaking [7]: The synopsis suggested 'smallest available color set size' |A(v)|, which "
    "is mathematically invariant for tied vertices since |A(v)| = k - sat(v). Our code implements Sewell's rule [7], [9], "
    "scoring up to max_ties = 8 tied vertices by shared available colors with uncolored neighbors: "
    "SewellScore(v) = Σ_{u ∈ N(v) ∩ U} |A(v) ∩ A(u)|.\n"
    "  (b) Clique Lower-Bound Pre-Coloring [2], [4]: greedy_clique(G, rank, max_starts=20) finds a maximal clique Q "
    "(giving LB = |Q| ≤ ω(G) ≤ χ(G)) and pre-colors Q with {0, ..., |Q|-1} prior to DSATUR.\n"
    "  (c) Iterative Degree & Domination Reduction [4]: reduce_graph() iteratively peels vertices with deg(v) < LB onto a "
    "LIFO stack and removes non-adjacent dominated vertices u where u ≁ v and N(u) ⊆ N(v) (accelerated via u's "
    "minimum-degree neighbor pivot within domination_budget = 2,000,000). After DSATUR colors the reduced subgraph H, "
    "stack vertices are colored in reverse order via First-Fit without adding colors."
)

add_pseudocode_box("Concise Pseudocode of the Four Implemented Algorithms (Basic Greedy, Welsh-Powell, DSATUR, Improved DSATUR)", [
    "// Alg 1: Basic Greedy O(n+m) [5] & Alg 2: Welsh-Powell O(n log n + m) [3]",
    "Greedy(G, order): for v in order: colors[v] = min{c >= 0 : c not in {colors[u] for u in G.adj[v]}}; return colors",
    "WelshPowell(G, s): rank = make_rank(n, s); order = sort(V, key=v: (-|G.adj[v]|, rank[v])); return Greedy(G, order)",
    "// Alg 3: Heap DSATUR O((n+m) log n) [2] & Alg 4: Improved DSATUR (Reductions [4] + Clique Seed + Sewell Rule [7])",
    "ImprovedDSATUR(G, s): Q = greedy_clique(G, max_starts=20); LB = |Q|",
    "  (alive, stack) = reduce_graph(G, LB) // Peel deg(v) < LB; remove u if non-adjacent v has N(u) subseteq N(v)",
    "  H, map = G.induced_subgraph(alive); initial = {Q_H[i]: i for i in 0..|Q_H|-1}",
    "  While H has uncolored vertices: pop top (sat, udeg) candidates from lazy heap; break ties by max SewellScore(v)",
    "    Assign smallest free color c to v*; update nbr_colors[u] and push to heap if sat(u) increases",
    "  Map H colors to G; for v in reversed(stack): colors[v] = first_fit(G.adj[v], colors); return colors"
], font_sz=Pt(7.6))

add_p(
    "Figures 4.3–4.6 present the step-by-step execution flowcharts of Basic Greedy [5], Welsh-Powell [3], Lazy-Heap "
    "Standard DSATUR [2], and the Multi-Seed Comparative Evaluation Pipeline used to benchmark all four heuristics, "
    "followed by the algorithmic and synopsis-vs-code verification summary in Table 4.1."
)

add_side_by_side_figures(
    "Figures/diag4_basic_greedy.png", "Figure 4.3: Execution Flowchart of Basic Greedy (First-Fit) Coloring [5] (gcol/algorithms/greedy.py).",
    "Figures/diag5_welsh_powell.png", "Figure 4.4: Execution Flowchart of Welsh-Powell Degree-Ordered Coloring [3] (gcol/algorithms/welsh_powell.py).",
    width_each=3.05
)
add_side_by_side_figures(
    "Figures/diag6_dsatur.png", "Figure 4.5: Execution Flowchart of Standard DSATUR with Lazy Binary Heap Extraction [2] (gcol/algorithms/dsatur.py).",
    "Figures/diag8_evaluation_pipeline.png", "Figure 4.6: Multi-Seed Comparative Evaluation Metrics and Research Question Synthesis Pipeline.",
    width_each=3.05
)

comp_headers = ["Algorithm / Aspect", "Ordering & Tie-Breaking", "Preprocessing", "Time Complexity", "Space", "Synopsis vs. Code Audit"]
comp_rows = [
    ["Basic Greedy [5]", "Static seed order; First-Fit", "None", "O(n + m)", "O(n + m)", "Matches synopsis; uses custom slot Graph."],
    ["Welsh-Powell [3]", "Static decreasing d(v), rank[v]", "Degree sort", "O(n log n + m)", "O(n + m)", "Implements both First-Fit & class sweep."],
    ["Standard DSATUR [2]", "Dynamic (sat(v), udeg(v), -rank)", "None", "O((n + m) log n)", "O(n + m)", "Lazy binary heap + naive O(n²+m) verifier."],
    ["Improved DSATUR [4],[7]", "Dynamic + Sewell Σ|A(v)∩A(u)|", "Clique + LB Peel + Domination", "O((n+m)log n + R)", "O(n + m)", "Fixes |A(v)| tie invariance via Sewell rule [7]; uses non-adjacent open N(u)⊆N(v) domination [4]."]
]
add_styled_table("Table 4.1: Algorithmic Comparison and Synopsis-vs-Implementation Verification Summary", comp_headers, comp_rows, font_size=Pt(8.0))

# ==============================================================================
# CHAPTER 5: DATASET DESCRIPTION AND EXPERIMENTAL SETUP
# ==============================================================================
add_chapter_heading("Chapter 5: Dataset Description and Experimental Setup")

add_side_by_side_figures(
    "Figures/diag2_experimental_workflow.png", "Figure 5.1: End-to-End Experimental Workflow and Benchmarking Pipeline (run_experiments.py).",
    "Figures/diag3_graph_pipeline.png", "Figure 5.2: Synthetic NetworkX and DIMACS (.col) [11] Graph Ingestion Pipeline into gcol.graph.Graph.",
    width_each=3.05
)

add_p(
    "As illustrated in the end-to-end experimental workflow (Figure 5.1) and dataset ingestion pipeline (Figure 5.2), "
    "we evaluate six graph families implemented in gcol/generators.py and gcol/dimacs.py: "
    "(5.1) Erdős–Rényi G(n, p): Independent edge probability p ∈ {0.1, 0.3, 0.5, 0.7, 0.9} across n up to 1000 "
    "(synopsis lists up to 10,000; benchmark runner caps at n=1000 for multi-seed tractability), featuring binomial "
    "degrees and wide ω-to-χ gaps as density grows. "
    "(5.2) Barabási–Albert BA(n, m): Scale-free preferential attachment networks (n ∈ {100, 500, 1000}, m ∈ {2, 5, 10}) "
    "with power-law degree hubs and sparse peripheries. "
    "(5.3) Random Geometric RGG(n, r): Spatial graphs in [0,1]² with radius r ∈ {0.1, 0.2, 0.3} and high clustering (0.51–0.68). "
    "(5.4) Cycle Graphs C_n: 2-regular rings (n ∈ {50, 51, 100, 500}) where χ(C_n) = 2 for even n and 3 for odd n. "
    "(5.5) Complete Graphs K_n & Crown Graphs: K_n (n ∈ {10, 20, 50, 100}, χ = ω = n) and bipartite Crown graphs (χ = 2) [5]. "
    "(5.6) DIMACS Benchmarks [4], [8]: 8 standard instances in data/—triangle-free myciel3 (χ=4) and myciel5 (χ=6), chessboard "
    "queen5_5 (χ=5) and queen8_8 (χ=9), character networks jean (χ=10), anna (χ=11), huck (χ=11, replacing binary-only "
    "flat300_28), and Leighton graph le450_15a (n=450, m=8168, χ=15). "
    "(5.7) Experimental Environment: Windows 11 (64-bit), AMD Ryzen 5 5625U CPU (6C/12T), 15.35 GB RAM, Python 3.12.4, "
    "NetworkX 3.4.2, NumPy 2.2.6, Pandas 3.0.6, Matplotlib 3.9.2, Pytest 8.3.3, timed via time.perf_counter() and tracemalloc."
)

df_eda = pd.read_csv("Experimental_Results/dataset_eda_summary.csv")
rep_graphs = ["myciel3", "myciel5", "queen5_5", "queen8_8", "jean", "anna", "huck", "le450_15a",
              "ER(n=100,p=0.5)", "ER(n=500,p=0.1)", "ER(n=500,p=0.5)", "ER(n=1000,p=0.1)",
              "BA(n=500,m=2)", "BA(n=500,m=5)", "BA(n=1000,m=5)", "RGG(n=500,r=0.1)", "RGG(n=500,r=0.2)",
              "Cycle(500)", "Complete(100)", "Crown(25)"]
eda_sub = df_eda[df_eda["Graph"].isin(rep_graphs)]
eda_headers = ["Family", "Graph Instance", "n", "m", "Density", "Avg Deg", "Max Δ", "Clustering", "Clique ω_g", "Known χ"]
eda_rows = [[r["Family"], r["Graph"], int(r["n"]), int(r["m"]), f"{r['Density']:.4f}", f"{r['Avg_Degree']:.1f}",
             int(r["Max_Degree"]), f"{r['Avg_Clustering']:.3f}", int(r["Clique_LB_omega"]), str(r["Known_or_Exact_Chi"])]
            for _, r in eda_sub.iterrows()]
add_styled_table("Table 5.1: Structural Summary of DIMACS and Representative Synthetic Benchmark Datasets", eda_headers, eda_rows, font_size=Pt(7.8))

# ==============================================================================
# CHAPTER 6: IMPLEMENTATION DETAILS (CORE ENGINE, BACKEND & FRONTEND)
# ==============================================================================
add_chapter_heading("Chapter 6: Implementation Details")

add_p(
    "1. Core Algorithmic Engine (gcol/): The repository is structured into gcol/ (graph.py, coloring.py, bounds.py, "
    "dimacs.py, generators.py, and algorithms/{greedy, welsh_powell, dsatur, improved_dsatur, exact}.py), data/ (8 "
    "DIMACS .col files), tests/test_algorithms.py (pytest suite), and run_experiments.py. To avoid NetworkX's nested "
    "dictionary overhead during benchmarking, gcol.graph.Graph uses __slots__ = ('n', 'adj', 'name') with list-of-sets "
    "adjacency (adj: list[set[int]]) and O(n + m) induced_subgraph() remapping. Every coloring output is verified via "
    "assert_proper(G, colors) and profiled with time.perf_counter() and tracemalloc.\n"
    "2. Interactive Web Backend (app.py) & Frontend Workbench (web/index.html): To enable interactive demonstration, "
    "we implemented a zero-dependency REST backend using Python's built-in http.server (ColoringRequestHandler) and a "
    "single-page HTML5/CSS3/Canvas frontend. Users configure any DIMACS or synthetic graph (family, n, p/m/r, seed) in "
    "the UI; the frontend sends a POST /api/color JSON request to app.py, which executes all four algorithms in real "
    "time, computes spring/circular 2D vertex coordinates, and returns k, approximation ratio, relative gain (%), "
    "runtime (ms), peak memory (KB), properness status, and vertex color assignments for interactive HTML5 Canvas rendering "
    "(shown in Figures 6.1–6.3)."
)

add_figure(
    "Figures/ui_screenshot1_dashboard.png",
    "Figure 6.1: Interactive Web Application Dashboard Showing Graph Configuration and Live Algorithmic Comparison on ER(n=24, p=0.25, seed=3), Where Welsh-Powell, DSATUR, and Improved DSATUR Achieve Optimal k = χ = 4 Colors (20% Gain Over Basic Greedy's 5 Colors).",
    width_inches=5.8
)
add_side_by_side_figures(
    "Figures/ui_screenshot2_er_canvas.png",
    "Figure 6.2: Interactive HTML5 Canvas Rendering of Proper 4-Coloring (c0..c3) Assigned by DSATUR on ER(n=24, p=0.25).",
    "Figures/ui_screenshot3_cycle_canvas.png",
    "Figure 6.3: Live Comparison and Circular Layout Canvas Visualization of an Odd Cycle Graph C_5 (χ = 3, 0 Conflicts)."
)

# ==============================================================================
# CHAPTER 7: COMPLEXITY ANALYSIS
# ==============================================================================
add_chapter_heading("Chapter 7: Complexity Analysis")

add_p(
    "1. Basic Greedy: O(n + m) time and O(n) working space (1 hash-set construction of size d(v) per vertex).\n"
    "2. Welsh-Powell: O(n log n) Timsort by degree followed by O(n + m) First-Fit gives O(n log n + m) time and O(n) working space.\n"
    "3. Standard DSATUR: Naive linear scan takes O(n² + m) time. Our binary heap engine pushes a tuple only when "
    "sat(u) increases (≤ m pushes) plus ≤ m lazy udeg refreshes in pop_valid(), giving O((n + m) log n) worst-case time. "
    "Because Σ_{v∈V} |nbr_colors[v]| ≤ 2m and heap size ≤ n + m, space is strictly O(n + m).\n"
    "4. Improved DSATUR: Runs in O((n + m) log n + R + T_Sewell) time and O(n + m) space, where multi-start clique "
    "takes O(s·ω·Δ²), LB degree peeling takes O(n + m), pivot domination is capped at domination_budget = 2×10⁶ "
    "operations, and Sewell tie-breaking evaluates at most max_ties = 8 candidates in O(d(v)·k) time per tie. On "
    "sparse graphs where LB peeling removes 100% of vertices, best-case time drops to linear O(n + m). Finally, all "
    "four greedy methods satisfy the universal upper bound χ(G) ≤ k ≤ Δ(G) + 1 (whereas Brooks' Theorem bounds χ(G) ≤ Δ(G) "
    "for connected graphs other than K_n and odd cycles, though NP-hardness prevents guaranteed χ(G) attainment)."
)

# ==============================================================================
# CHAPTER 8: EXPERIMENTAL RESULTS AND ANALYSIS
# ==============================================================================
add_chapter_heading("Chapter 8: Experimental Results and Analysis")

add_sub_heading("8.1 Evaluation Metrics, EDA, and Exact Solver Validation", level=2)
add_p(
    "Each benchmark was evaluated across 10 tie-breaking seeds (and 3 graph instances × 10 seeds for randomized "
    "synthetic families). We measure: (1) Colors Used k (mean ± SD, min), (2) Approximation Ratio ρ_χ = k / χ(G) "
    "(or conservative clique lower-bound ratio ρ_ω = k / ω_g when exact χ is unknown; note ω(G) = χ(G) on RGG/BA/Stanford "
    "graphs but ω(G) << χ(G) on Mycielski and dense ER graphs), (3) Execution Time (ms), (4) Peak Memory (KB), and "
    "(5) Relative Improvement (%) = ((k_Greedy - k_Alg) / k_Greedy) × 100%. Table 8.1 summarizes our exact "
    "Branch-and-Bound solver (gcol/algorithms/exact.py) verification across 8 small graphs (n ≤ 51), proving exact "
    "chromatic numbers and confirming that Improved DSATUR achieves k / χ(G) = 1.00 across every tested instance."
)

df_ex = pd.read_csv("Experimental_Results/exact_solver_results.csv")
ex_sub = df_ex[df_ex["Graph"].isin(["myciel3", "myciel5", "queen5_5", "Cycle(50)", "Cycle(51)", "Complete(20)", "Crown(25)", "ER(30, 0.5)"])]
ex_headers = ["Graph", "n", "m", "Clique LB", "Exact χ(G)", "B&B Nodes", "Exact Time (ms)", "Greedy k", "WP k", "DSATUR k", "ImpDSATUR k", "k/χ"]
ex_rows = [[r["Graph"], int(r["n"]), int(r["m"]), int(r["Clique_LB"]), int(r["Exact_or_UB_Chi"]), int(r["BB_Nodes"]),
            f"{r['Exact_Time_ms']:.2f}", int(r["Greedy_k"]), int(r["WP_k"]), int(r["DSATUR_k"]), int(r["ImpDSATUR_k"]), f"{r['ImpDSATUR_Approx_Ratio']:.2f}"]
           for _, r in ex_sub.iterrows()]
add_styled_table("Table 8.1: Exact Branch-and-Bound Chromatic Number Verification on Small Benchmarks (n ≤ 51)", ex_headers, ex_rows, font_size=Pt(7.8))

df_agg = pd.read_csv("Experimental_Results/comprehensive_summary_results.csv")
dim_agg = df_agg[df_agg["Category"] == "DIMACS"]
dim_headers = ["DIMACS Graph", "n", "m", "χ", "Basic Greedy (k / ms)", "Welsh-Powell (k / ms)", "Std DSATUR (k / ms)", "Imp DSATUR (k / min / ms)", "Imp Gain (%)", "Std vs Imp Mem (KB)"]
dim_rows = []
for gname in ["myciel3", "myciel5", "queen5_5", "queen8_8", "jean", "anna", "huck", "le450_15a"]:
    sub = dim_agg[dim_agg["Graph"] == gname].set_index("Algorithm")
    r0 = sub.loc["Basic Greedy"]
    r1 = sub.loc["Welsh-Powell"]
    r2 = sub.loc["DSATUR"]
    r3 = sub.loc["Improved DSATUR"]
    dim_rows.append([
        gname, int(r0["n"]), int(r0["m_mean"]), int(r0["chi"]),
        f"{r0['colors_mean']:.2f} ({r0['time_ms_mean']:.2f}ms)",
        f"{r1['colors_mean']:.2f} ({r1['time_ms_mean']:.2f}ms)",
        f"{r2['colors_mean']:.2f} ({r2['time_ms_mean']:.2f}ms)",
        f"{r3['colors_mean']:.2f} [min {int(r3['colors_min'])}] ({r3['time_ms_mean']:.2f}ms)",
        f"{r3['rel_improv_pct']:.2f}%",
        f"{r2['memory_kb_mean']:.1f} vs {r3['memory_kb_mean']:.1f}"
    ])
add_styled_table("Table 8.2: Comparative Performance Across All 8 DIMACS Benchmark Instances (10 Independent Seeds)", dim_headers, dim_rows, font_size=Pt(7.5))

add_side_by_side_figures(
    "Figures/fig1_dimacs_colors.png", "Figure 8.1: Colors Used on DIMACS vs. Known χ(G).",
    "Figures/fig2_dimacs_time.png", "Figure 8.2: Execution Time Across DIMACS (Log Scale)."
)

add_sub_heading("8.2 Analysis of DIMACS and Synthetic Benchmark Results", level=2)
add_p(
    "DIMACS Findings (Table 8.1, Figures 8.1–8.2): On literary networks anna (χ=11), jean (χ=10), and huck (χ=11), "
    "DSATUR and Improved DSATUR achieve exact optimality (k/χ = 1.00), while Improved DSATUR's LB-core peeling removes "
    "100% of vertices prior to DSATUR, cutting peak memory by 6×–8× (10.8 KB vs. 64.1 KB on anna). On queen5_5 (χ=5), "
    "DSATUR and Improved DSATUR achieve 5.00 ± 0.00 (32.43% gain over Basic Greedy's 7.40). On queen8_8 (χ=9), "
    "Welsh-Powell degrades to 13.50 colors (-8.87% worse than Basic Greedy's 12.40), Standard DSATUR achieves 11.40, "
    "and Improved DSATUR achieves the lowest mean of 11.00 ± 0.47 and minimum of k = 10 colors. On le450_15a (χ=15), "
    "DSATUR and Improved DSATUR reduce colors by 24.22% over Basic Greedy (16.90 vs. 22.30, min 16)."
)

syn_agg = df_agg[df_agg["Category"] == "Synthetic"]
syn_pick = ["ER(n=100,p=0.1)", "ER(n=100,p=0.5)", "ER(n=100,p=0.9)", "ER(n=500,p=0.1)", "ER(n=500,p=0.5)", "ER(n=1000,p=0.1)",
            "BA(n=100,m=5)", "BA(n=500,m=2)", "BA(n=500,m=5)", "BA(n=1000,m=5)",
            "RGG(n=500,r=0.1)", "RGG(n=500,r=0.2)", "RGG(n=1000,r=0.1)",
            "Cycle(500)", "Complete(100)", "Crown(25)"]
syn_rows_compact = []
for gname in syn_pick:
    sub = syn_agg[syn_agg["Graph"] == gname].set_index("Algorithm")
    r0, r1, r2, r3 = sub.loc["Basic Greedy"], sub.loc["Welsh-Powell"], sub.loc["DSATUR"], sub.loc["Improved DSATUR"]
    syn_rows_compact.append([
        r0["Family"], gname, f"{r0['omega_lb']:.1f}",
        f"{r0['colors_mean']:.2f}", f"{r1['colors_mean']:.2f}",
        f"{r2['colors_mean']:.2f} ({r2['time_ms_mean']:.1f}ms)",
        f"{r3['colors_mean']:.2f} ({r3['time_ms_mean']:.1f}ms)",
        f"{r3['rel_improv_pct']:.2f}%",
        f"{r2['memory_kb_mean']:.0f} / {r3['memory_kb_mean']:.0f}"
    ])
syn_headers_c = ["Family", "Configuration", "ω_g", "Greedy k", "WP k", "DSATUR k (Time)", "Imp DSATUR k (Time)", "Imp Gain (%)", "Mem DSAT/Imp (KB)"]
add_styled_table("Table 8.3: Representative Synthetic Benchmark Results (3 Graph Realizations × 10 Seeds per Config)", syn_headers_c, syn_rows_compact, font_size=Pt(7.5))

df_diag = pd.read_csv("Experimental_Results/improved_dsatur_diagnostics.csv")
diag_sub = df_diag[df_diag["Graph"].isin(["queen8_8", "jean", "anna", "huck", "le450_15a", "ER(n=500,p=0.1)", "BA(n=500,m=2)", "BA(n=500,m=5)", "RGG(n=500,r=0.1)", "RGG(n=500,r=0.2)", "RGG(n=1000,r=0.1)", "Complete(100)"])]
diag_headers = ["Graph Instance", "n", "m", "Clique LB", "Low-Deg Removed", "Dominated Removed", "Reduced n_H", "Shrinkage (%)", "Ties Examined", "Ties Changed"]
diag_rows = [[r["Graph"], int(r["n"]), int(r["m"]), int(r["Clique_LB"]), int(r["Removed_LowDeg"]), int(r["Removed_Dominated"]),
              int(r["n_Reduced"]), f"{r['Reduction_Pct']:.1f}%", int(r["Ties_Examined"]), int(r["Ties_Changed"])]
             for _, r in diag_sub.iterrows()]
add_styled_table("Table 8.4: Diagnostic Telemetry of Improved DSATUR (Vertex Reductions and Sewell Tie-Breaking)", diag_headers, diag_rows, font_size=Pt(7.5))

add_side_by_side_figures(
    "Figures/fig3_colors_vs_n.png", "Figure 8.3: Colors Used vs. Graph Size (n).",
    "Figures/fig4_time_vs_n.png", "Figure 8.4: Runtime vs. n & Heap vs. Naive Speedup."
)
add_side_by_side_figures(
    "Figures/fig5_density_impact.png", "Figure 8.5: Impact of Edge Density p on ER Graphs.",
    "Figures/fig6_synthetic_families.png", "Figure 8.6: Cross-Family Coloring Comparison."
)
add_side_by_side_figures(
    "Figures/fig7_memory_usage.png", "Figure 8.7: Peak Memory Usage (Log Scale).",
    "Figures/fig8_approximation_ratio.png", "Figure 8.8: Empirical Approximation Ratio k/χ(G)."
)
add_side_by_side_figures(
    "Figures/fig9_eda_degree_distributions.png", "Figure 8.9: EDA Vertex Degree Distributions.",
    "Figures/fig10_ablation_and_reduction.png", "Figure 8.10: Ablation Study & Reduction Shrinkage (%)."
)

add_sub_heading("8.3 Ablation Analysis, Reduction Diagnostics, and Research Questions (RQ1–RQ3)", level=2)
add_p(
    "Synthetic, Ablation, and Diagnostic Insights (Table 8.2, Figures 8.3–8.10): "
    "(1) Answering RQ1: Vertex ordering governs solution quality—static degree sorting (Welsh-Powell) improves over "
    "Basic Greedy on scale-free networks (e.g., 6.60 vs. 10.40 on BA(1000, 5)), but fails on regular/bipartite graphs "
    "(using 3.00 colors on even Cycle(500) where χ=2). Dynamic saturation (DSATUR & Improved DSATUR) achieves exact "
    "2-colorings on all even cycles and Crown graphs and saves up to 51.87% colors on BA(500, 2) and 7.70 colors on "
    "ER(500, 0.5) (64.97 vs. 72.67). "
    "(2) Answering RQ2: Our 6-variant ablation study (Figure 8.10a) confirms that Sewell tie-breaking overrides 40%–48% "
    "of DSATUR ties, stabilizing le450_15a to 16.00 ± 0.00 across all 10 seeds and lowering ER(500, 0.1) to 15.10 ± 0.30 "
    "(when paired with clique pre-coloring). Meanwhile, LB degree peeling and non-adjacent domination remove 100% of "
    "vertices on anna, jean, huck, BA(500, 2), RGG(500, 0.1), and Complete(100), 73.5% on RGG(1000, 0.1), and 30.8% on "
    "RGG(500, 0.2) (Figure 8.10b). "
    "(3) Answering RQ3: Welsh-Powell offers the fastest sub-millisecond runtime for low-latency needs; Heap DSATUR "
    "(which achieves a 3.44× speedup over Naive O(n²) DSATUR at n=2000, Figure 8.4b) provides the best general balance "
    "on dense unreducible graphs; and Improved DSATUR excels both in minimum color count on hard combinatorial graphs "
    "(queen8_8, ER) and in memory efficiency on graphs with dense clique cores and sparse peripheries (cutting memory "
    "by 89% on RGG(500, 0.1): 50 KB vs. 443 KB)."
)

# ==============================================================================
# CHAPTER 9: CONCLUSION AND FUTURE SCOPE
# ==============================================================================
add_chapter_heading("Chapter 9: Conclusion and Future Scope")
add_p(
    "This project completed a comprehensive experimental and theoretical investigation of Basic Greedy, Welsh-Powell, "
    "Standard DSATUR, and Improved DSATUR across 8 DIMACS and 31 synthetic graph configurations. By refining the "
    "tertiary tie-breaker to Sewell's maximum shared-available-color rule and implementing pivot-accelerated "
    "non-adjacent vertex domination and LB-core peeling, Improved DSATUR achieved the highest solution quality across "
    "the benchmark suite (saving up to 51.87% colors over Basic Greedy and shrinking sparse/clustered graphs by up to "
    "100% prior to DSATUR). Limitations: On dense homogeneous graphs (e.g., ER(500, 0.5) where d_min >> LB), reductions "
    "remove zero vertices and add 2×–3× preprocessing overhead. Future Scope: Coupling Improved DSATUR warm-starts "
    "with Tabucol local search and localized PySAT recoloring to complete the full hybrid SLIM pipeline [4]."
)

# ==============================================================================
# CHAPTER 10: REFERENCES (IEEE Format, No URLs)
# ==============================================================================
add_chapter_heading("Chapter 10: References")
ieee_references = [
    "[1] R. M. Karp, \"Reducibility among combinatorial problems,\" in Complexity of Computer Computations, R. E. Miller and J. W. Thatcher, Eds. New York, NY, USA: Plenum Press, 1972, pp. 85–104.",
    "[2] D. Brélaz, \"New methods to color the vertices of a graph,\" Communications of the ACM, vol. 22, no. 4, pp. 251–256, Apr. 1979.",
    "[3] D. J. A. Welsh and M. B. Powell, \"An upper bound for the chromatic number of a graph and its application to timetabling problems,\" The Computer Journal, vol. 10, no. 1, pp. 85–86, May 1967.",
    "[4] A. Schidler and S. Szeider, \"SAT-boosted tabu search for coloring massive graphs,\" ACM Journal of Experimental Algorithmics, vol. 28, art. no. 1.5, pp. 1–20, Jul. 2023.",
    "[5] R. Lewis, A Guide to Graph Colouring: Algorithms and Applications, 2nd ed. Cham, Switzerland: Springer, 2021.",
    "[6] M. Zuckerman, \"Linear degree extractors and the inapproximability of Max Clique and Chromatic Number,\" Theory of Computing, vol. 3, no. 1, pp. 103–128, Aug. 2007.",
    "[7] E. C. Sewell, \"An exact algorithm for the graph coloring problem,\" in Cliques, Coloring, and Satisfiability: Second DIMACS Implementation Challenge, vol. 26. Providence, RI, USA: AMS, 1996, pp. 359–373.",
    "[8] M. Aslan and N. O. Baykan, \"A performance comparison of graph coloring algorithms,\" International Journal of Intelligent Systems and Applications in Engineering, vol. 4, Special Issue-1, pp. 1–7, Dec. 2016.",
    "[9] P. San Segundo, \"A new DSATUR-based algorithm for exact vertex coloring,\" Computers & Operations Research, vol. 39, no. 7, pp. 1724–1733, Jul. 2012.",
    "[10] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 3rd ed. Cambridge, MA, USA: MIT Press, 2009."
]
for ref in ieee_references:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.12
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    r = p.add_run(ref)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.0)

# ==============================================================================
# CHAPTER 11: DIVISION OF WORK
# ==============================================================================
add_chapter_heading("Chapter 11: Division of Work")
div_headers = ["Student Name", "Roll Number", "Contribution / Module Responsibility"]
div_rows = [
    ["Sabeeh Ahsan", "22803006", "To be documented/confirmed by team member prior to evaluation"],
    ["Harleen Kaur", "22803009", "To be documented/confirmed by team member prior to evaluation"],
    ["Tanmay Butta", "22803014", "To be documented/confirmed by team member prior to evaluation"],
    ["Aryan Khanna", "22803028", "To be documented/confirmed by team member prior to evaluation"]
]
add_styled_table("Table 11.1: Team Member Division of Work Confirmation Table", div_headers, div_rows, font_size=Pt(9.0))

# ==============================================================================
# CHAPTER 12: APPENDIX – CORE SOURCE CODE
# ==============================================================================
add_chapter_heading("Chapter 12: Appendix – Core Source Code")
p_app = add_p(
    "Below are the core algorithmic implementations from the gcol package (greedy.py, welsh_powell.py, dsatur.py, "
    "bounds.py, improved_dsatur.py, graph.py, exact.py) alongside the interactive web backend (app.py) and frontend "
    "(web/index.html)."
)
p_app.paragraph_format.line_spacing = 1.15
p_app.paragraph_format.space_after = Pt(2)

appendix_snippets = [
    ("12.1 Basic Greedy & Welsh-Powell (gcol/algorithms/greedy.py & welsh_powell.py)", [
        "def greedy_coloring(G: Graph, order: Optional[Iterable[int]] = None, seed: Optional[int] = None) -> list[int]:",
        "    order = input_order(G.n, seed) if order is None else order; colors = [UNCOLORED] * G.n",
        "    for v in order: colors[v] = first_fit(G.adj[v], colors)",
        "    return colors",
        "def welsh_powell_first_fit(G: Graph, seed: Optional[int] = None) -> list[int]:",
        "    rank = make_rank(G.n, seed); order = sorted(range(G.n), key=lambda v: (-len(G.adj[v]), rank[v]))",
        "    return greedy_coloring(G, order=order)"
    ]),
    ("12.2 Heap-Based DSATUR Engine with Sewell Tie-Breaking (gcol/algorithms/dsatur.py)", [
        "def dsatur_engine(G: Graph, rank: list[int], initial: Optional[dict[int, int]] = None,",
        "                  sewell_tiebreak: bool = False, max_ties: int = 8) -> list[int]:",
        "    n, adj, colors = G.n, G.adj, [UNCOLORED] * G.n; nbr_colors = [set() for _ in range(n)]",
        "    udeg = [len(adj[v]) for v in range(n)]; k = 0; colored = 0",
        "    heap = [(-len(nbr_colors[v]), -udeg[v], rank[v], v) for v in range(n)]; heapq.heapify(heap)",
        "    def sewell_score(v: int) -> int:",
        "        avail = {c for c in range(k) if c not in nbr_colors[v]}; la = len(avail)",
        "        return 0 if la == 0 else sum(la - len(nbr_colors[u] & avail) for u in adj[v] if colors[u] == UNCOLORED)",
        "    while colored < n:",
        "        negsat, negdeg, r, v = pop_valid(heap, colors, nbr_colors, udeg)",
        "        if sewell_tiebreak and k > 0: # Score up to max_ties=8 tied vertices by max sewell_score(v)",
        "            v = resolve_sewell_ties(heap, negsat, negdeg, r, v, colors, nbr_colors, udeg, sewell_score, max_ties)",
        "        c = first_fit_from_used(nbr_colors[v]); colors[v] = c; colored += 1; k = max(k, c + 1)",
        "        for u in adj[v]:",
        "            if colors[u] == UNCOLORED:",
        "                udeg[u] -= 1",
        "                if c not in nbr_colors[u]: nbr_colors[u].add(c); heapq.heappush(heap, (-len(nbr_colors[u]), -udeg[u], rank[u], u))",
        "    return colors"
    ]),
    ("12.3 Multi-Start Clique LB, Reductions & Improved DSATUR (gcol/bounds.py & improved_dsatur.py)", [
        "def improved_dsatur(G: Graph, seed: Optional[int] = None, use_tiebreak: bool = True,",
        "                    use_clique: bool = True, use_reduction: bool = True) -> list[int]:",
        "    rank = make_rank(G.n, seed); clique = greedy_clique(G, rank) if (use_clique or use_reduction) else []",
        "    lb = len(clique); alive, stack = reduce_graph(G, lb, rank) if use_reduction else ([True]*G.n, [])",
        "    kept = [v for v in range(G.n) if alive[v]]; H, mapping = G.induced_subgraph(kept)",
        "    inv = {old: new for new, old in enumerate(mapping)}; rank_H = [rank[old] for old in mapping]",
        "    initial = {inv[v]: c for c, v in enumerate(clique if all(v in inv for v in clique) else greedy_clique(H, rank_H))} if use_clique and H.n > 0 else {}",
        "    hcolors = dsatur_engine(H, rank_H, initial=initial, sewell_tiebreak=use_tiebreak)",
        "    colors = [UNCOLORED] * G.n",
        "    for new, old in enumerate(mapping): colors[old] = hcolors[new]",
        "    for v in reversed(stack): colors[v] = first_fit(G.adj[v], colors)",
        "    return colors"
    ]),
    ("12.4 Interactive Web Backend API & Frontend Canvas Workbench (app.py & web/index.html)", [
        "def run_comparison(params: dict) -> dict:",
        "    G, known_chi = build_graph(params); seed = int(params.get('seed', 0)); omega_lb = len(greedy_clique(G, make_rank(G.n, seed)))",
        "    results, colorings, base_k = [], {}, None",
        "    for name, fn in ALGORITHMS:",
        "        tracemalloc.start(); t0 = time.perf_counter(); colors = fn(G, seed=seed)",
        "        elapsed_ms = (time.perf_counter() - t0) * 1000.0; _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()",
        "        k = num_colors(colors); base_k = k if base_k is None else base_k",
        "        results.append({'algorithm': name, 'colors': k, 'time_ms': round(elapsed_ms, 3), 'memory_kb': round(peak/1024.0, 2),",
        "                        'proper': is_proper(G, colors), 'gain_pct': round((base_k - k) / base_k * 100.0, 2) if base_k else 0.0})",
        "        colorings[name] = colors",
        "    return {'graph': {'name': G.name, 'n': G.n, 'm': G.m, 'omega_lb': omega_lb, 'known_chi': known_chi},",
        "            'results': results, 'colorings': colorings, 'nodes': compute_layout(G), 'edges': list(G.edges())}"
    ])
]

for title_s, lines_s in appendix_snippets:
    add_pseudocode_box(title_s, lines_s, font_sz=Pt(6.2))

docx_out = r"H:\COLLEGE\5th Year\10TH SEM\ALGO PROJECT\Advanced_Algorithms_Mini_Project_Report.docx"
doc.save(docx_out)
print(f"[SUCCESS] Saved concise Word report to: {docx_out} ({os.path.getsize(docx_out)/1024:.1f} KB)")
