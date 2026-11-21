================================================================================
FINAL ACADEMIC RESEARCH PROJECT REPORT — DELIVERABLES & DOCUMENTATION
================================================================================

Project Title    : Experimental Analysis and Optimization of Greedy Graph Coloring Algorithms
Subject          : Advanced Algorithms Lab [17M15CS111]
Institute        : Jaypee Institute of Information Technology (JIIT), Sector 62, Noida
Department       : Department of Computer Science and Engineering
Academic Session : 2026-27
Submitted To     : Dr. Taj Alam and Deepti Singh, Assistant Professors, Dept. of CSE, JIIT
Submitted By     :
  - Sabeeh Ahsan (22803006)
  - Harleen Kaur (22803009)
  - Tanmay Butta (22803014)
  - Aryan Khanna (22803028)

--------------------------------------------------------------------------------
1. OVERVIEW OF GENERATED DELIVERABLES
--------------------------------------------------------------------------------
1. Advanced_Algorithms_Mini_Project_Report.docx
   - Complete, editable Microsoft Word report formatted to university specifications
     (A4 page size, 1-inch margins, Times New Roman 12pt justified body text,
     16pt bold Chapter headings, 14pt bold subheadings, 1.5 line spacing, automatic
     Table of Contents, headers, page numbering, 12 tables, 18 embedded figures,
     IEEE references, and full source code appendix).

2. Advanced_Algorithms_Mini_Project_Report.pdf
   - High-resolution PDF export generated directly from Microsoft Word with all
     Table of Contents and page number fields updated.

3. Figures/ (18 High-DPI PNG Diagrams & Experimental Plots)
   - diag1_architecture.png          : Overall system architecture of gcol
   - diag2_experimental_workflow.png : End-to-end benchmarking workflow
   - diag3_graph_pipeline.png        : Synthetic & DIMACS graph ingestion pipeline
   - diag4_basic_greedy.png          : Basic Greedy (First-Fit) workflow
   - diag5_welsh_powell.png          : Welsh-Powell degree-ordered workflow
   - diag6_dsatur.png                : Standard DSATUR lazy binary-heap workflow
   - diag7_improved_dsatur.png       : Improved DSATUR 5-stage pipeline
   - diag8_evaluation_pipeline.png   : Comparative evaluation metrics pipeline
   - fig1_dimacs_colors.png          : Colors used across 8 DIMACS benchmarks
   - fig2_dimacs_time.png            : Execution time across DIMACS benchmarks (log scale)
   - fig3_colors_vs_n.png            : Colors vs. graph size (n) on ER and BA graphs
   - fig4_time_vs_n.png              : Time vs. n and Heap vs. Naive DSATUR verification
   - fig5_density_impact.png         : Coloring performance vs. edge probability (p)
   - fig6_synthetic_families.png     : Cross-family synthetic comparison
   - fig7_memory_usage.png           : Peak memory usage (tracemalloc, KB, log scale)
   - fig8_approximation_ratio.png    : Empirical approximation ratio k / chi(G)
   - fig9_eda_degree_distributions.png : EDA degree histograms (ER, BA, RGG, le450_15a)
   - fig10_ablation_and_reduction.png  : Improved DSATUR ablation & reduction shrinkage

4. Experimental_Results/ (9 CSV Data Files)
   - baseline_raw_results.csv          : Original run_experiments.py raw output
   - baseline_summary_results.csv      : Original run_experiments.py summary table
   - comprehensive_raw_results.csv     : Full 4,400-run dataset across all 39 configs
   - comprehensive_summary_results.csv : Aggregated mean, SD, min, max, time, memory, ratios
   - dataset_eda_summary.csv           : Structural EDA (n, m, density, degrees, clustering, omega_g)
   - exact_solver_results.csv          : Exact Branch-and-Bound chromatic numbers (n <= 51)
   - ablation_study_results.csv        : 6-variant component ablation study of Improved DSATUR
   - improved_dsatur_diagnostics.csv   : Telemetry of low-degree/domination removals & Sewell ties
   - dsatur_heap_vs_naive.csv          : Scaling comparison of Heap O((n+m)log n) vs Naive O(n^2)

--------------------------------------------------------------------------------
2. LIST OF EXPERIMENTS PERFORMED
--------------------------------------------------------------------------------
- Experiment 1 (DIMACS Benchmark Evaluation):
  Evaluated Basic Greedy, Welsh-Powell, DSATUR, and Improved DSATUR across 8 DIMACS
  instances (myciel3, myciel5, queen5_5, queen8_8, jean, anna, huck, le450_15a)
  with 10 random tie-breaking seeds per instance.
- Experiment 2 (Synthetic Topology & Density Evaluation):
  Evaluated 31 synthetic configurations across Erdos-Renyi G(n,p) (n in {100, 500, 1000},
  p in {0.1, 0.3, 0.5, 0.7, 0.9}), Barabasi-Albert BA(n,m) (n in {100, 500, 1000},
  m in {2, 5, 10}), Random Geometric RGG(n,r) (n in {100, 500, 1000}, r in {0.1, 0.2, 0.3}),
  Cycle graphs (n in {50, 51, 100, 500}), Complete graphs (n in {10, 20, 50, 100}),
  and adversarial bipartite Crown(25) (3 instances x 10 seeds = 30 runs per config).
- Experiment 3 (Exact Chromatic Number Verification):
  Executed the DSATUR Branch-and-Bound exact solver (gcol/algorithms/exact.py) on 12
  small graphs (n <= 51) to prove exact chromatic numbers chi(G) and verify heuristic
  approximation ratios.
- Experiment 4 (Improved DSATUR Component Ablation & Reduction Telemetry):
  Evaluated all 6 combinations of (use_tiebreak, use_clique, use_reduction) and logged
  exact counts of low-degree peeled vertices, dominated vertices, and Sewell tie-break
  overrides.
- Experiment 5 (Priority Queue vs. Naive Linear Scan Verification):
  Benchmarked dsatur() vs. dsatur_naive() across n in {100, 250, 500, 1000, 2000} on
  ER(n, 0.1), confirming identical output colorings and up to 3.44x speedup.

--------------------------------------------------------------------------------
3. ITEMS REQUIRING MANUAL CONFIRMATION BY THE STUDENT TEAM
--------------------------------------------------------------------------------
1. Chapter 11 (Division of Work - Table 11.1):
   In strict compliance with academic integrity guidelines, individual team member
   contributions for Sabeeh Ahsan (22803006), Harleen Kaur (22803009), Tanmay Butta
   (22803014), and Aryan Khanna (22803028) are marked as "To be documented/confirmed
   by team member prior to viva" in Table 11.1. Please fill in each student's specific
   role before printing/submitting if required by your instructor.
2. Unexecuted Ultra-Large Synthetic Sizes (n = 5,000 and n = 10,000) & flat300_28:
   As documented transparently in Chapter 4 (Table 4.2) and Chapter 5, the generator
   functions support arbitrary n, while the automated benchmark suite was capped at
   n = 1,000 (and n = 2,000 for heap scaling) so that all multi-seed and ablation
   experiments complete reproducibly within a few minutes. Additionally, flat300_28
   is hosted in binary .col.b format on the CMU archive and was substituted with the
   standard ASCII huck.col instance alongside the other 7 ASCII DIMACS benchmarks.
================================================================================
