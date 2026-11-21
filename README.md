# Deep Dive in Graph Coloring Algorithms (`gcol`)

**Experimental Analysis and Optimization of Greedy Graph Coloring Algorithms**  
*Advanced Algorithms Lab [17M15CS111] — Department of Computer Science and Engineering, Jaypee Institute of Information Technology (JIIT), Sector 62, Noida*

---

## Overview

The **Graph Vertex Coloring Problem (GCP)** assigns discrete color labels to the vertices of a simple undirected graph $G = (V, E)$ with $n = |V|$ and $m = |E|$ such that no two adjacent vertices share the same color. Computing the minimum number of colors—the chromatic number $\chi(G)$—is NP-hard, and even approximating $\chi(G)$ within $n^{1-\varepsilon}$ is NP-hard unless $\text{P} = \text{NP}$.

This repository provides a complete Python framework (`gcol`), an automated multi-seed benchmarking suite, an exact Branch-and-Bound verifier, and an interactive zero-dependency Web UI (`app.py` + `web/index.html`) comparing four constructive greedy vertex coloring algorithms:

1. **Basic Greedy (First-Fit) Coloring** — Sequential coloring along natural/seed-permuted vertex order in $\mathcal{O}(n + m)$ time.
2. **Welsh-Powell Algorithm** — Static non-increasing degree ordering ($\mathcal{O}(n \log n + m)$ time) in both First-Fit and classical color-class sweep formulations.
3. **Standard DSATUR (Brélaz, 1979)** — Dynamic maximum saturation degree ordering (`sat(v)`, `udeg(v)`) using a lazy-deletion binary priority queue in $\mathcal{O}((n + m) \log n)$ time (verified against a naive $\mathcal{O}(n^2 + m)$ implementation).
4. **Improved DSATUR** — Integrates three polynomial-time enhancements inspired by Schidler & Szeider (2023) and Sewell (1996):
   - **Multi-Start Greedy Maximal Clique Lower Bound ($\omega_g \le \omega(G) \le \chi(G)$)** & clique pre-coloring.
   - **Iterative Graph Reductions**: Low-degree LB-core peeling ($\deg(v) < \text{LB}$) onto a LIFO reconstruction stack and pivot-accelerated non-adjacent vertex domination removal ($u \not\sim v, N(u) \subseteq N(v)$).
   - **Sewell's Maximum-Constraint Tie-Breaking**: Resolves equal `(sat(v), udeg(v))` ties by maximizing shared available colors across uncolored neighbors.

---

## Repository Structure

```text
├── gcol/                           # Core Python Graph Coloring Package
│   ├── graph.py                    # Slot-based undirected Graph class & induced subgraph extraction
│   ├── coloring.py                 # First-Fit primitives, tie-break ranks & properness verifier
│   ├── bounds.py                   # Multi-start greedy clique LB & iterative degree/domination reductions
│   ├── dimacs.py                   # DIMACS (.col) benchmark parser
│   ├── generators.py               # Synthetic graph generators (ER, BA, RGG, Cycle, Complete, Crown)
│   └── algorithms/
│       ├── greedy.py               # Algorithm 1: Basic Greedy (First-Fit)
│       ├── welsh_powell.py         # Algorithm 2: Welsh-Powell (First-Fit & Classical Sweep)
│       ├── dsatur.py               # Algorithm 3: Standard DSATUR (Lazy Heap & Naive O(n^2) Verifier)
│       ├── improved_dsatur.py      # Algorithm 4: Improved DSATUR (Clique LB + Reductions + Sewell Rule)
│       └── exact.py                # Exact DSATUR-based Branch-and-Bound Chromatic Number Solver
├── data/                           # 8 DIMACS Benchmark Instances (myciel3, myciel5, queen5_5, queen8_8, jean, anna, huck, le450_15a)
├── web/
│   └── index.html                  # Single-page HTML5 Canvas & Live Algorithmic Comparison Workbench
├── app.py                          # Zero-dependency Python HTTP REST Backend (/api/color, /api/datasets)
├── run_experiments.py              # Main multi-seed experimental benchmark runner
├── generate_report_data.py         # Generates CSV summaries, ablation tables & exact B&B verification
├── generate_report_figures.py      # Generates 18 high-DPI architecture diagrams, flowcharts & empirical plots
├── build_final_report.py           # Automated builder for the final academic research project report
├── Experimental_Results/           # Exported CSV experimental tables & summary metrics
├── Figures/                        # High-resolution architectural flowcharts, plots & Web UI screenshots
├── tests/
│   └── test_algorithms.py          # Automated Pytest verification suite
├── .env.example                    # Safe environment variable template
├── requirements.txt                # Python package dependencies
└── LICENSE                         # MIT License
```

---

## Quick Start & Execution (PowerShell / Bash)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Launch the Interactive Web Application
```powershell
python app.py
```
Open **`http://127.0.0.1:8000`** in your browser to configure any DIMACS or synthetic graph, run all four algorithms side-by-side in real time, and inspect the interactive colored graph on the HTML5 Canvas.

### 3. Run the Full Experimental Benchmark Suite
```powershell
python run_experiments.py
```

### 4. Run Automated Unit Tests
```powershell
pytest -v
```

---

## Key Empirical Highlights

- **DIMACS Benchmarks**: On real-world character co-appearance networks (`anna`, `jean`, `huck`), **Improved DSATUR** achieves exact chromatic optimality ($k = \chi(G)$) while removing **100% of vertices** during LB-core preprocessing prior to DSATUR, cutting peak memory usage by $6\times\text{–}8\times$. On `queen8_8` ($\chi = 9$), Improved DSATUR achieves the lowest mean coloring ($11.00 \pm 0.47$, minimum $10$ colors), and on `le450_15a` ($\chi = 15$) reduces colors by **24.22%** over Basic Greedy.
- **Synthetic Topologies**: On Barabási–Albert scale-free networks (`BA(500, 2)`), dynamic saturation ordering reduces color usage by **51.87%** over Basic Greedy. On 2-chromatic even cycles (`Cycle(500)`) and adversarial bipartite `Crown` graphs, DSATUR and Improved DSATUR consistently achieve exact 2-colorings ($k = 2$).
- **Priority Queue Speedup**: Lazy-Heap DSATUR ($\mathcal{O}((n + m) \log n)$) achieves up to a **$3.44\times$ speedup** over Naive linear-scan DSATUR ($\mathcal{O}(n^2 + m)$) at $n = 2000$.

---

## Team Members

| Student Name | Roll Number |
|---|---|
| **Sabeeh Ahsan** | 22803006 |
| **Harleen Kaur** | 22803009 |
| **Tanmay Butta** | 22803014 |
| **Aryan Khanna** | 22803028 |

**Submitted To:** Dr. Taj Alam and Deepti Singh, Assistant Professors, Department of CSE, JIIT Noida.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
