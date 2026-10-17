#!/usr/bin/env python3
"""
Generates the complete 16:9 widescreen PowerPoint presentation (PPTX)
for the Parallel Mandelbrot Set project with OpenMP.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path="Parallel_Mandelbrot_OpenMP.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_DARK_BG = RGBColor(30, 19, 56)      # #1e1338
    C_LIGHT_BG = RGBColor(248, 250, 252)  # #f8fafc
    C_CARD_BG = RGBColor(255, 255, 255)
    C_CARD_BORDER = RGBColor(226, 232, 240)
    C_TEXT_DARK = RGBColor(15, 23, 42)
    C_TEXT_MUTED = RGBColor(100, 116, 139)
    C_TEXT_LIGHT = RGBColor(255, 255, 255)
    C_PURPLE = RGBColor(88, 28, 135)
    C_ACCENT_ROSE = RGBColor(225, 29, 72)
    C_ACCENT_BLUE = RGBColor(2, 132, 199)
    C_ACCENT_GREEN = RGBColor(5, 150, 105)

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="PARALLEL COMPUTING PROJECT"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = C_PURPLE

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, C_DARK_BG)

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.5), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Parallel Mandelbrot Set\nwith OpenMP"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_LIGHT
    p.space_after = Pt(20)

    p2 = tf.add_paragraph()
    p2.text = "Static scheduling vs. dynamic load balancing,\nbenchmarked by self-relative speedup."
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(30)

    p3 = tf.add_paragraph()
    p3.text = "Parallel Computing | Project Presentation"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(168, 85, 247)

    # Right side Mandelbrot image
    if os.path.exists("output/mandelbrot.png"):
        s1.shapes.add_picture("output/mandelbrot.png", Inches(7.5), Inches(1.5), Inches(5.0), Inches(4.5))

    # -------------------------------------------------------------
    # SLIDE 2: Introduction: The Task and The Tool
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, C_LIGHT_BG)
    add_header(s2, "Introduction: the task and the tool")

    # Card 1: The Task
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    c1.fill.solid(); c1.fill.fore_color.rgb = C_CARD_BG
    c1.line.color.rgb = C_CARD_BORDER
    tf1 = c1.text_frame; tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = Inches(0.3)
    p = tf1.paragraphs[0]; p.text = "📌 The Task"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(14)
    bullets1 = [
        "Compute the Mandelbrot set using the escape-time algorithm, then render it as an image.",
        "Pixel computational cost is highly non-uniform: boundary points escape in 1–5 iterations, while interior points require all 1000 iterations.",
        "Compare static block scheduling with dynamic chunk load balancing across multiple CPU cores.",
        "Measure and analyze self-relative speedup and parallel efficiency."
    ]
    for b in bullets1:
        p = tf1.add_paragraph(); p.text = "• " + b; p.font.size = Pt(13); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(10)

    # Card 2: The Tool (OpenMP)
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0))
    c2.fill.solid(); c2.fill.fore_color.rgb = C_CARD_BG
    c2.line.color.rgb = C_CARD_BORDER
    tf2 = c2.text_frame; tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = Inches(0.3)
    p = tf2.paragraphs[0]; p.text = "⚙️ The Tool: OpenMP"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(14)
    bullets2 = [
        "Industry-standard compiler-directed API for shared-memory parallel programming in C, C++, and Fortran.",
        "Parallelism is introduced declaratively via pragmas (e.g. #pragma omp parallel for) and compiled with -fopenmp.",
        "Provides runtime scheduling clauses (schedule(static) vs schedule(dynamic, chunk)) without rewriting algorithm logic.",
        "Includes standard runtime routines: omp_set_num_threads() and omp_get_wtime()."
    ]
    for b in bullets2:
        p = tf2.add_paragraph(); p.text = "• " + b; p.font.size = Pt(13); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 3: Parallel Computing Environment
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, C_LIGHT_BG)
    add_header(s3, "Parallel computing environment")

    # Left box: Hardware Architecture Diagram
    c_arch = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    c_arch.fill.solid(); c_arch.fill.fore_color.rgb = RGBColor(241, 245, 249)
    c_arch.line.color.rgb = RGBColor(148, 163, 184)
    tf = c_arch.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Intel Core i5-13420H (SMP, 12 Hardware Threads)"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(10)
    arch_details = [
        "• 4 Performance Cores (P-cores): 8 threads via Hyper-Threading (up to 4.6 GHz)",
        "• 4 Efficient Cores (E-cores): 4 single-threaded cores for background throughput",
        "• Total Hardware Execution Units: 8 physical cores, 12 logical threads",
        "• L1 Cache: 320 KB Data / 384 KB Instruction",
        "• L2 Cache: 7 MB dedicated cache",
        "• L3 Cache: 12 MB shared unified cache across all cores",
        "• Memory Architecture: Unified Main Memory (UMA) in a single physical address space"
    ]
    for d in arch_details:
        p = tf.add_paragraph(); p.text = d; p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(6)

    # Right side: 4 Key Hardware Features
    features = [
        ("8 Cores, 12 Hardware Threads", "Thread counts of 1, 2, 4, 8, and 12 map cleanly onto physical P-cores, E-cores, and Hyper-Threads."),
        ("Uniform Shared Memory (UMA)", "All OpenMP worker threads see a unified 64-bit address space, writing directly into the output image buffer."),
        ("Cache-Friendly Row Layout", "Each row is stored contiguously in memory, maximizing L1 and L2 spatial cache line hit rates."),
        ("Disjoint Lock-Free Writes", "Each thread computes independent rows, completely eliminating mutex contention and false sharing.")
    ]
    y_pos = Inches(1.6)
    for title, desc in features:
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.7), y_pos, Inches(5.8), Inches(1.15))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = C_CARD_BORDER
        tf_f = box.text_frame; tf_f.word_wrap = True
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = Inches(0.15)
        p = tf_f.paragraphs[0]; p.text = title; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_PURPLE
        p2 = tf_f.add_paragraph(); p2.text = desc; p2.font.size = Pt(10.5); p2.font.color.rgb = C_TEXT_MUTED
        y_pos += Inches(1.35)

    # -------------------------------------------------------------
    # SLIDE 4: OpenMP: Main Capabilities
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, C_LIGHT_BG)
    add_header(s4, "OpenMP: main capabilities")

    caps = [
        ("Worksharing [Used here]", "#pragma omp parallel for partitions loop iterations across a team of worker threads. Supports sections, single, and reduction operations.", C_ACCENT_ROSE),
        ("Loop Scheduling [Used here]", "Controls iteration dispatching: schedule(static), schedule(dynamic, chunk), guided, and auto allow flexible trade-offs between overhead and load balance.", C_ACCENT_ROSE),
        ("Tasks & Dependencies", "omp task with depend clauses constructs dynamic task graphs for irregular parallelism; taskloop divides irregular nested iterations into tasks.", C_ACCENT_BLUE),
        ("SIMD & Heterogeneous Offloading", "omp simd enforces data vectorization; target directives offload compute kernels to GPUs, DSPs, and attached accelerators.", C_ACCENT_GREEN)
    ]
    coords = [
        (Inches(0.8), Inches(1.6)),
        (Inches(6.8), Inches(1.6)),
        (Inches(0.8), Inches(4.3)),
        (Inches(6.8), Inches(4.3))
    ]
    for (title, text, badge_col), (x, y) in zip(caps, coords):
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.4))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = text; p2.font.size = Pt(12); p2.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 5: Where OpenMP is Used in Practice
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, C_LIGHT_BG)
    add_header(s5, "Where OpenMP is used in practice")

    real_apps = [
        ("🌐 Weather & Climate Modeling", "ECMWF's Integrated Forecasting System (IFS) and the Weather Research and Forecasting (WRF) model combine OpenMP on multicore nodes with MPI across cluster nodes."),
        ("🔬 Molecular Dynamics", "GROMACS, LAMMPS, and NAMD distribute inter-atomic particle force calculations across threads on shared-memory nodes."),
        ("📊 High-Performance Numerical Libraries", "OpenBLAS, Intel oneMKL, and LAPACK leverage OpenMP to parallelize dense linear algebra operations (GEMM, matrix inversions)."),
        ("⚙️ Engineering Simulation & CFD", "OpenFOAM and ANSYS Fluent employ hybrid MPI + OpenMP models for aerodynamic and fluid dynamic simulations.")
    ]
    y_pos = Inches(1.6)
    for title, desc in real_apps:
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(11.7), Inches(1.15))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_PURPLE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(11); p2.font.color.rgb = C_TEXT_DARK
        y_pos += Inches(1.35)

    # -------------------------------------------------------------
    # SLIDE 6: The Task: Escape-Time Mandelbrot
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, C_LIGHT_BG)
    add_header(s6, "The task: escape-time Mandelbrot")

    c_task = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.0))
    c_task.fill.solid(); c_task.fill.fore_color.rgb = C_CARD_BG
    c_task.line.color.rgb = C_CARD_BORDER
    tf = c_task.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Mathematical Definition"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(12)
    t_points = [
        "Map each screen pixel (x, y) to a complex number c = cr + i*ci in the region x in [-2.0, 0.5], y in [-1.25, 1.25].",
        "Iterate the quadratic recurrence: z_{n+1} = z_n^2 + c with z_0 = 0.",
        "Escape condition: if |z|^2 = zr^2 + zi^2 > 4.0, sequence diverges.",
        "Stop at escape or when max_iter (1000) is reached. Iteration count is the escape time.",
        "Resolution: 1920 x 1080 Full HD (2,073,600 individual pixels).",
        "Coloring: Escaped pixels colored via standard sine palette; interior set points remain obsidian black."
    ]
    for pt in t_points:
        p = tf.add_paragraph(); p.text = "• " + pt; p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(6)

    # Image
    if os.path.exists("output/mandelbrot.png"):
        s6.shapes.add_picture("output/mandelbrot.png", Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.0))

    # -------------------------------------------------------------
    # SLIDE 7: How the Task is Parallelized
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, C_LIGHT_BG)
    add_header(s7, "How the task is parallelized")

    # Three major cards
    cards = [
        ("No Task Dependencies", "Embarrassingly Parallel", "A pixel's value depends exclusively on its own complex coordinate c. No thread ever needs to read data written by another thread.", C_ACCENT_ROSE),
        ("No Locks on Data Buffer", "Disjoint Memory Writes", "Each thread computes independent scanlines and writes directly into its assigned slice of the shared 1D buffer: index = y * width + x.", C_ACCENT_BLUE),
        ("Distribution is the Problem", "Spatial Load Imbalance", "Computing cost varies from 1 to 1000 iterations per pixel. Equal row division creates severe bottlenecks, requiring dynamic scheduling.", C_ACCENT_GREEN)
    ]
    x_pos = Inches(0.8)
    for title, subtitle, desc, col in cards:
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.8), Inches(3.7), Inches(4.8))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = col; p.space_after = Pt(4)
        p_sub = tf.add_paragraph(); p_sub.text = subtitle; p_sub.font.size = Pt(12); p_sub.font.bold = True; p_sub.font.color.rgb = C_PURPLE; p_sub.space_after = Pt(14)
        p_desc = tf.add_paragraph(); p_desc.text = desc; p_desc.font.size = Pt(11.5); p_desc.font.color.rgb = C_TEXT_DARK
        x_pos += Inches(4.0)

    # -------------------------------------------------------------
    # SLIDE 8: Static vs. Dynamic Scheduling
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, C_LIGHT_BG)
    add_header(s8, "Static vs. dynamic scheduling")

    # Static Box
    b_stat = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    b_stat.fill.solid(); b_stat.fill.fore_color.rgb = C_CARD_BG; b_stat.line.color.rgb = C_CARD_BORDER
    tf = b_stat.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "schedule(static)"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_ACCENT_ROSE; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "Equal Contiguous Blocks, Fixed at Start"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = C_TEXT_MUTED; p.space_after = Pt(12)
    code_stat = "#pragma omp parallel for schedule(static)\nfor (int y = 0; y < H; ++y) {\n    compute_row(y);\n}"
    p = tf.add_paragraph(); p.text = code_stat; p.font.size = Pt(11); p.font.name = "Courier New"; p.font.color.rgb = C_PURPLE; p.space_after = Pt(14)
    stat_pts = [
        "• Deterministic block division: Thread i gets rows [i*H/P, (i+1)*H/P).",
        "• Near-zero scheduling overhead at runtime.",
        "• Critical Flaw: Threads 1 & 2 handle the dense central cardioid, while Threads 0 & 3 finish outer rows early and sit idle at the barrier."
    ]
    for pt in stat_pts:
        p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(6)

    # Dynamic Box
    b_dyn = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    b_dyn.fill.solid(); b_dyn.fill.fore_color.rgb = C_CARD_BG; b_dyn.line.color.rgb = C_CARD_BORDER
    tf = b_dyn.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "schedule(dynamic, 4)"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_ACCENT_BLUE; p.space_after = Pt(6)
    p = tf.add_paragraph(); p.text = "Idle Threads Request Next 4 Rows at Runtime"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = C_TEXT_MUTED; p.space_after = Pt(12)
    code_dyn = "#pragma omp parallel for schedule(dynamic, 4)\nfor (int y = 0; y < H; ++y) {\n    compute_row(y);\n}"
    p = tf.add_paragraph(); p.text = code_dyn; p.font.size = Pt(11); p.font.name = "Courier New"; p.font.color.rgb = C_PURPLE; p.space_after = Pt(14)
    dyn_pts = [
        "• Shared work queue dispatches chunks of 4 rows on demand.",
        "• Small synchronization overhead per chunk fetch.",
        "• Major Advantage: Threads finishing fast exterior rows immediately pull more work, dynamically distributing the cardioid load across all cores."
    ]
    for pt in dyn_pts:
        p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 9: Why the Workload is Uneven
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, C_LIGHT_BG)
    add_header(s9, "Why the workload is uneven")

    # Left Card: Analysis
    c_anal = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.0))
    c_anal.fill.solid(); c_anal.fill.fore_color.rgb = C_CARD_BG; c_anal.line.color.rgb = C_CARD_BORDER
    tf = c_anal.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Spatial Workload Imbalance Analysis"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(12)
    imbalance_pts = [
        "Mandelbrot has extreme spatial irregularity:",
        "• Middle 25% of rows contain 59% of all computational work (main cardioid and period bulbs).",
        "• Outer 50% of rows contain only 6% of total work (quick escape outside the set).",
        "• In a 4-thread static run, middle threads receive ~47% of total work each, while outer threads receive only ~3%.",
        "• Result: Middle threads become severe stragglers. The parallel runtime is determined by the slowest thread!"
    ]
    for pt in imbalance_pts:
        p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(12); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(8)

    # Right side: 3 Big Metric Cards
    m_cards = [
        ("59%", "of all computation sits in the middle 25% of rows", C_ACCENT_ROSE),
        ("6%", "of all computation sits in the outer 50% of rows", C_ACCENT_BLUE),
        ("47% vs 3%", "work given to middle vs outer threads under 4-way static chunking", C_PURPLE)
    ]
    y_pos = Inches(1.6)
    for stat, label, col in m_cards:
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), y_pos, Inches(5.7), Inches(1.4))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG; box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)
        p = tf.paragraphs[0]; p.text = stat; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = col
        p2 = tf.add_paragraph(); p2.text = label; p2.font.size = Pt(11); p2.font.color.rgb = C_TEXT_MUTED
        y_pos += Inches(1.6)

    # -------------------------------------------------------------
    # SLIDE 10: OpenMP Features That Enabled It
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10, C_LIGHT_BG)
    add_header(s10, "OpenMP features that enabled it")

    # Table of Features
    rows = 7; cols = 2
    table_shape = s10.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(7.5), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(3.0)
    table.columns[1].width = Inches(4.5)

    headers = ["OpenMP Directive / Feature", "How It is Used in Project"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = C_PURPLE
        p = cell.text_frame.paragraphs[0]; p.font.bold = True; p.font.size = Pt(12); p.font.color.rgb = C_TEXT_LIGHT

    data = [
        ("#pragma omp parallel for", "Splits the outer row loop (y) across the thread team"),
        ("schedule(static)", "Divides rows into equal contiguous blocks fixed at loop start"),
        ("schedule(dynamic, 4)", "Assigns 4-row chunks on-demand via shared runtime queue"),
        ("omp_set_num_threads(t)", "Configures worker thread count for 1, 2, 4, 8, 12 benchmark runs"),
        ("Implicit barrier", "Guarantees all threads finish before stopping the timer"),
        ("std::chrono", "High-precision wall-clock timing in milliseconds for benchmarks")
    ]
    for r, (feat, usage) in enumerate(data, start=1):
        cell0 = table.cell(r, 0); cell0.text = feat
        cell1 = table.cell(r, 1); cell1.text = usage
        for cell in (cell0, cell1):
            cell.fill.solid(); cell.fill.fore_color.rgb = C_CARD_BG if r % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]; p.font.size = Pt(10.5); p.font.color.rgb = C_TEXT_DARK

    # Right Card: Why Dynamic Wins
    c_win = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.7), Inches(1.6), Inches(3.8), Inches(5.0))
    c_win.fill.solid(); c_win.fill.fore_color.rgb = C_CARD_BG; c_win.line.color.rgb = C_CARD_BORDER
    tf = c_win.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Why Dynamic Wins"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_ACCENT_BLUE; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.text = "schedule(dynamic, 4)"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(14)
    win_desc = [
        "The OpenMP runtime maintains an atomic shared queue of 4-row chunks.",
        "When an exterior thread finishes early, it immediately pulls another chunk.",
        "Faster threads shoulder more total rows, balancing total execution time.",
        "Eliminates the straggler problem completely!"
    ]
    for d in win_desc:
        p = tf.add_paragraph(); p.text = "• " + d; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 11: Benchmark: Method and Measured Times
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11, C_LIGHT_BG)
    add_header(s11, "Benchmark: method and measured times")

    # Left: Method Box
    c_meth = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.8), Inches(5.0))
    c_meth.fill.solid(); c_meth.fill.fore_color.rgb = C_CARD_BG; c_meth.line.color.rgb = C_CARD_BORDER
    tf = c_meth.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
    p = tf.paragraphs[0]; p.text = "Speedup Method"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(8)
    p = tf.add_paragraph(); p.text = "S(p) = T(1) / T(p)"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_ACCENT_ROSE; p.space_after = Pt(12)
    m_pts = [
        "• Self-Relative Speedup: Each parallel strategy is compared against single-thread baseline.",
        "• Efficiency: E(p) = S(p) / p * 100%.",
        "• Thread Counts: 1, 2, 4, 8, 12 threads tested on Intel Core i5-13420H.",
        "• Same C++ code executed across all configurations."
    ]
    for pt in m_pts:
        p = tf.add_paragraph(); p.text = pt; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(8)

    # Right: Results Table
    t_shape = s11.shapes.add_table(6, 6, Inches(4.9), Inches(1.6), Inches(7.6), Inches(5.0))
    t = t_shape.table
    cols_w = [Inches(1.0), Inches(1.3), Inches(1.3), Inches(1.3), Inches(1.4), Inches(1.3)]
    for idx, w in enumerate(cols_w): t.columns[idx].width = w

    t_headers = ["Threads", "Static (ms)", "Dynamic (ms)", "Static Spd", "Dynamic Spd", "Dynamic Eff"]
    for c, h in enumerate(t_headers):
        cell = t.cell(0, c); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = C_PURPLE
        p = cell.text_frame.paragraphs[0]; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = C_TEXT_LIGHT

    t_data = [
        ("1", "1345.43", "1338.51", "1.00x", "1.00x", "100.0%"),
        ("2", "679.81", "670.41", "1.98x", "2.00x", "99.8%"),
        ("4", "638.49", "338.92", "2.11x", "3.95x", "98.7%"),
        ("8", "416.64", "207.43", "3.23x", "6.45x", "80.7%"),
        ("12", "339.12", "157.33", "3.97x", "8.51x", "70.9%")
    ]
    for r, row in enumerate(t_data, start=1):
        for c, val in enumerate(row):
            cell = t.cell(r, c); cell.text = val
            cell.fill.solid(); cell.fill.fore_color.rgb = C_CARD_BG if r % 2 == 1 else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]; p.font.size = Pt(10.5); p.font.color.rgb = C_TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 12: Self-Relative Speedup Results
    # -------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12, C_LIGHT_BG)
    add_header(s12, "Self-relative speedup results")

    # Plot Image
    if os.path.exists("output/benchmark_comparison.png"):
        s12.shapes.add_picture("output/benchmark_comparison.png", Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.2))

    # Right Callout Cards
    res_cards = [
        ("3.95x vs. 2.11x (at 4 threads)", "Dynamic scheduling achieves 98.7% parallel efficiency. Static scheduling hits a ceiling of 2.11x due to cardioid stragglers.", C_ACCENT_BLUE),
        ("8.51x vs. 3.97x (at 12 threads)", "Dynamic scheduling delivers more than double the speedup of static scheduling (71% vs. 33% efficiency).", C_ACCENT_ROSE),
        ("Why efficiency drops after 8 threads", "Threads 9–12 run on Intel's Efficient cores (E-cores) and Hyper-Threading shares execution pipelines on P-cores.", C_TEXT_MUTED)
    ]
    y_pos = Inches(1.6)
    for title, desc, col in res_cards:
        box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), y_pos, Inches(4.6), Inches(1.5))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG; box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = col
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(10.5); p2.font.color.rgb = C_TEXT_DARK
        y_pos += Inches(1.75)

    # -------------------------------------------------------------
    # SLIDE 13: Live Interactive Demonstration (The Web Visualizer)
    # -------------------------------------------------------------
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13, C_LIGHT_BG)
    add_header(s13, "Live visualizer: watching calculations in real time")

    features_demo = [
        ("🧵 Core Allocation Map", "Color-codes every row by the thread that calculated it. Visually confirms how static chunks form rigid bands while dynamic chunks interleave dynamically."),
        ("⚡ Flexible Core Scaling", "Interactive toggle for 1, 2, 4, 8, 12, or 16 cores with live CPU load meters showing iteration balance."),
        ("🎨 Multiple Color Themes", "Royal Amethyst, Quanta Cyan, Classic Electric, Sunset, and Cyber Emerald palettes."),
        ("🔍 Real-Time Pixel Telemetry", "Inspects HEX/RGB codes, iteration counts, complex plane coordinates, and thread owners on mouse hover.")
    ]
    x_pos = Inches(0.8)
    for title, desc in features_demo[:2]:
        box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.8), Inches(5.6), Inches(2.3))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG; box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(11.5); p2.font.color.rgb = C_TEXT_DARK
        x_pos += Inches(6.0)

    x_pos = Inches(0.8)
    for title, desc in features_demo[2:]:
        box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(4.5), Inches(5.6), Inches(2.3))
        box.fill.solid(); box.fill.fore_color.rgb = C_CARD_BG; box.line.color.rgb = C_CARD_BORDER
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.25)
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(11.5); p2.font.color.rgb = C_TEXT_DARK
        x_pos += Inches(6.0)

    # -------------------------------------------------------------
    # SLIDE 14: Key Takeaways & Conclusions
    # -------------------------------------------------------------
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14, C_DARK_BG)

    tb = s14.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.8))
    tf = tb.text_frame
    p = tf.paragraphs[0]; p.text = "Key takeaways"; p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = C_TEXT_LIGHT

    # 3 Summary Cards
    t_cards = [
        ("3.95x vs. 2.11x", "Dynamic vs. Static Speedup at 4 Threads", "Eliminates the cardioid bottleneck, maintaining near-100% CPU utilization."),
        ("8.51x", "Peak Dynamic Speedup at 12 Threads", "Static scheduling caps at 3.97x (less than half the performance)."),
        ("59%", "of All Work Sits in Middle 25% of Rows", "Why static block partitioning fundamentally fails on fractal algorithms.")
    ]
    x_pos = Inches(0.8)
    for num, title, desc in t_cards:
        box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x_pos, Inches(1.8), Inches(3.7), Inches(3.6))
        box.fill.solid(); box.fill.fore_color.rgb = RGBColor(45, 27, 84)
        box.line.color.rgb = RGBColor(107, 33, 168)
        tf = box.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.3)
        p = tf.paragraphs[0]; p.text = num; p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = RGBColor(216, 180, 254); p.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = title; p2.font.size = Pt(13); p2.font.bold = True; p2.font.color.rgb = C_TEXT_LIGHT; p2.space_after = Pt(12)
        p3 = tf.add_paragraph(); p3.text = desc; p3.font.size = Pt(11); p3.font.color.rgb = RGBColor(203, 213, 225)
        x_pos += Inches(4.0)

    # Bottom summary box
    b_bot = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.1))
    b_bot.fill.solid(); b_bot.fill.fore_color.rgb = RGBColor(24, 15, 45)
    b_bot.line.color.rgb = RGBColor(76, 29, 149)
    tf = b_bot.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "• Uneven computational cost causes static scheduling to stall. Dynamic scheduling cures load imbalance with a one-clause change.\n• Efficiency scales near-linearly up to physical P-cores, then tapers off as E-cores and Hyper-Threads are utilized."
    p.font.size = Pt(11.5); p.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------
    # SLIDE 15: References
    # -------------------------------------------------------------
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15, C_LIGHT_BG)
    add_header(s15, "References & resources")

    c_ref = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    c_ref.fill.solid(); c_ref.fill.fore_color.rgb = C_CARD_BG; c_ref.line.color.rgb = C_CARD_BORDER
    tf = c_ref.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = Inches(0.4)
    p = tf.paragraphs[0]; p.text = "Academic & Technical Literature"; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_PURPLE; p.space_after = Pt(16)

    refs = [
        "1. OpenMP Architecture Review Board, 'OpenMP Application Programming Interface Specification', Version 5.2, November 2021. Available: https://www.openmp.org/",
        "2. R. Chandra, L. Dagum, D. Kohr, D. Maydan, J. McDonald, and R. Menon, 'Parallel Programming in OpenMP', Morgan Kaufmann Publishers, 2001.",
        "3. P. Pacheco, 'An Introduction to Parallel Programming', Morgan Kaufmann / Elsevier, 2011.",
        "4. B. B. Mandelbrot, 'The Fractal Geometry of Nature', W. H. Freeman and Company, New York, 1982.",
        "5. Intel Corporation, '13th Gen Intel Core Processor Datasheet, Volume 1: Architecture and Hybrid Multiprocessing', 2023."
    ]
    for r in refs:
        p = tf.add_paragraph(); p.text = r; p.font.size = Pt(12); p.font.color.rgb = C_TEXT_DARK; p.space_after = Pt(14)

    # Save
    prs.save(output_path)
    print(f"[Success] Generated PowerPoint presentation: {output_path}")

if __name__ == "__main__":
    create_presentation()
