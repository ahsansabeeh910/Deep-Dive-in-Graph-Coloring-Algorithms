"""Generate all flowcharts, architecture diagrams, and experimental visualizations into Figures/."""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

from gcol.dimacs import load_dimacs
from gcol.generators import erdos_renyi, barabasi_albert, random_geometric

os.makedirs("Figures", exist_ok=True)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 10

# Helper for clean academic flowchart drawing
def create_flowchart_canvas(figsize=(8.0, 4.4), title=""):
    fig, ax = plt.subplots(figsize=figsize, dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    if title:
        ax.text(50, 96.5, title, ha="center", va="center", fontsize=13.5, fontweight="bold", color="#1F4E79")
    return fig, ax

def draw_box(ax, x, y, w, h, text, bg="#E8EEF5", edge="#1F4E79", text_color="#000000", fontsize=11.0, bold=False, boxstyle="round,pad=0.6,rounding_size=1.5"):
    patch = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle=boxstyle,
                           facecolor=bg, edgecolor=edge, linewidth=1.8)
    ax.add_patch(patch)
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=text_color, fontweight=weight, multialignment="center")

def draw_arrow(ax, x1, y1, x2, y2, label="", rad=0.0):
    conn = f"arc3,rad={rad}"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.45", lw=1.7, color="#2C3E50", connectionstyle=conn))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 1.5, my, label, fontsize=10.0, color="#1F4E79", fontweight="bold", ha="left", va="center")

print("Generating 8 Flowchart & Architecture Diagrams...")

# 1. Overall Project Architecture
fig, ax = create_flowchart_canvas((9.2, 5.4), "Overall System Architecture of the Graph Coloring Framework (gcol)")
draw_box(ax, 22, 82, 38, 12, "Data Acquisition Layer\n• DIMACS .col Parser (dimacs.py)\n• NetworkX Generators (generators.py)", bg="#D9E2F3", bold=True, fontsize=10.5)
draw_box(ax, 76, 82, 42, 12, "Core Graph Representation (graph.py)\n• Custom Adjacency-Set Graph Class\n• 0..n-1 Indexing, O(1) Adjacency Check", bg="#D9E2F3", bold=True, fontsize=10.5)
draw_arrow(ax, 41, 82, 55, 82, "Constructs")

draw_box(ax, 50, 60, 90, 13, "Preprocessing & Lower-Bound Module (bounds.py, improved_dsatur.py)\n• Multi-Start Greedy Maximal Clique (ω_LB) & Exact Clique (n ≤ 120)\n• LB-Core Low-Degree Peeling (deg(v) < LB) & Non-Adjacent Domination (N(u) ⊆ N(v))", bg="#FFF2CC", edge="#B27D00", bold=True, fontsize=10.5)
draw_arrow(ax, 76, 76, 55, 66.5)

draw_box(ax, 13, 36, 22, 15, "Basic Greedy\n(greedy.py)\n• Seed Order\n• First-Fit\n• O(n + m)", bg="#E2EFDA", edge="#375623", fontsize=10.0)
draw_box(ax, 37, 36, 22, 15, "Welsh-Powell\n(welsh_powell.py)\n• Degree Sort\n• First-Fit/Sweep\n• O(n log n + m)", bg="#E2EFDA", edge="#375623", fontsize=10.0)
draw_box(ax, 61, 36, 22, 15, "Std DSATUR\n(dsatur.py)\n• Lazy Heap\n• Max (sat, udeg)\n• O((n+m)log n)", bg="#E2EFDA", edge="#375623", fontsize=10.0)
draw_box(ax, 86, 36, 24, 15, "Improved DSATUR\n(improved_dsatur.py)\n• Clique Seed\n• Reduce + Sewell\n• O((n+m)log n+R)", bg="#FCE4D6", edge="#C65911", bold=True, fontsize=10.0)

for x_pos in [13, 37, 61, 86]:
    draw_arrow(ax, 50, 53.5, x_pos, 43.5)

draw_box(ax, 50, 12, 92, 12, "Verification, Web Workbench & Analytics Engine (coloring.py, exact.py, app.py)\n• Properness Check (assert_proper)  • Exact B&B Solver (exact.py)  • Web UI + CSV/Plots", bg="#EDEDED", edge="#404040", bold=True, fontsize=10.5)
for x_pos in [13, 37, 61, 86]:
    draw_arrow(ax, x_pos, 28.5, 50, 18)

fig.tight_layout()
fig.savefig("Figures/diag1_architecture.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 2. Complete Experimental Workflow
fig, ax = create_flowchart_canvas((8.6, 4.8), "End-to-End Experimental Workflow and Benchmarking Pipeline")
steps = [
    (17, 80, "1. Dataset Init\nLoad DIMACS (.col) &\nSynthetic Graphs"),
    (50, 80, "2. Structural EDA\nCompute n, m, ρ, Δ,\nClique ω_g, χ(G)"),
    (83, 80, "3. Seed Loop\nGenerate 10 Seeds\n(0..9) make_rank()"),
    (83, 48, "4. Run Algorithms\nGreedy, Welsh-Powell,\nDSATUR, ImpDSATUR"),
    (50, 48, "5. Profiling\ntime.perf_counter() &\ntracemalloc Memory"),
    (17, 48, "6. Verification\nassert_proper(G, c)\n0 Edge Conflicts"),
    (50, 15, "7. Statistical Aggregation & Visualization\nCompute Mean, SD, Min k, Approx Ratio (k/χ, k/ω), Relative Gain (%)\nExport CSV Tables (Experimental_Results/) & High-DPI Plots (Figures/)")
]
for i, (x, y, txt) in enumerate(steps):
    w = 29 if i < 6 else 88
    bg = "#D9E2F3" if i < 3 else ("#E2EFDA" if i < 6 else "#FFF2CC")
    draw_box(ax, x, y, w, 16, txt, bg=bg, bold=(i==6), fontsize=10.5)
draw_arrow(ax, 31.5, 80, 35.5, 80)
draw_arrow(ax, 64.5, 80, 68.5, 80)
draw_arrow(ax, 83, 72, 83, 56)
draw_arrow(ax, 68.5, 48, 64.5, 48)
draw_arrow(ax, 35.5, 48, 31.5, 48)
draw_arrow(ax, 17, 40, 40, 23)
fig.tight_layout()
fig.savefig("Figures/diag2_experimental_workflow.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 3. Graph Generation Pipeline
fig, ax = create_flowchart_canvas((8.4, 4.6), "Synthetic and DIMACS Graph Generation & Ingestion Pipeline")
draw_box(ax, 24, 78, 42, 16, "NetworkX Graph Generators\n• erdos_renyi(n, p), barabasi_albert(n, m)\n• random_geometric(n, r)\n• cycle_graph(n), complete_graph(n)", bg="#D9E2F3", fontsize=10.5)
draw_box(ax, 76, 78, 42, 16, "DIMACS Benchmark Files (.col)\n• Header: 'p edge n m'\n• Edges: 'e u v' (1-indexed)\n• 8 Instances: myciel, queen, jean, anna..", bg="#FCE4D6", fontsize=10.5)
draw_box(ax, 24, 46, 42, 13, "Graph.from_networkx(nxG)\nRemaps arbitrary node labels\nto contiguous integers 0..n-1", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 76, 46, 42, 13, "load_dimacs(filepath)\nShifts 1-indexed vertices (u-1, v-1)\nFilters comments ('c')", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 50, 15, 84, 15, "Unified Custom Graph Object (gcol.graph.Graph)\n• __slots__ = ('n', 'adj', 'name')  • adj: list[set[int]]\n• Eliminates NetworkX dictionary overhead during algorithm timing", bg="#FFF2CC", bold=True, fontsize=10.8)
draw_arrow(ax, 24, 70, 24, 52.5)
draw_arrow(ax, 76, 70, 76, 52.5)
draw_arrow(ax, 24, 39.5, 42, 22.5)
draw_arrow(ax, 76, 39.5, 58, 22.5)
fig.tight_layout()
fig.savefig("Figures/diag3_graph_pipeline.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 4. Basic Greedy Workflow
fig, ax = create_flowchart_canvas((7.5, 4.5), "Basic Greedy (First-Fit) Coloring Workflow")
draw_box(ax, 50, 84, 78, 11, "Input: Graph G(V, E), Seed s\nGenerate vertex sequence π = input_order(n, seed)", bg="#D9E2F3", bold=True, fontsize=11.5)
draw_box(ax, 50, 66, 78, 11, "Initialize colors[0..n-1] = UNCOLORED (-1)\nIterate next vertex v in order π", bg="#E8EEF5", fontsize=11.0)
draw_box(ax, 50, 46, 82, 12, "Collect Neighbor Color Set:\nused = { colors[u]  for u in G.adj[v] }", bg="#FFF2CC", fontsize=11.0)
draw_box(ax, 50, 27, 82, 12, "First-Fit Color Selection:\nFind smallest c ≥ 0 such that c ∉ used; Assign colors[v] = c", bg="#E2EFDA", fontsize=11.0)
draw_box(ax, 50, 9, 72, 10, "All vertices processed? Return colors[0..n-1]", bg="#D9E2F3", bold=True, fontsize=11.5)
draw_arrow(ax, 50, 78.5, 50, 71.5)
draw_arrow(ax, 50, 60.5, 50, 52)
draw_arrow(ax, 50, 40, 50, 33)
draw_arrow(ax, 50, 21, 50, 14)
fig.tight_layout()
fig.savefig("Figures/diag4_basic_greedy.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 5. Welsh-Powell Workflow
fig, ax = create_flowchart_canvas((7.8, 4.5), "Welsh-Powell Degree-Ordered Coloring Workflow")
draw_box(ax, 50, 84, 80, 11, "Input: Graph G(V, E), Seed s\nCompute tie-break rank = make_rank(n, seed)", bg="#D9E2F3", bold=True, fontsize=11.5)
draw_box(ax, 50, 65, 86, 12, "Static Degree Sorting (degree_order):\nSort vertices v ∈ V by key (-len(G.adj[v]), rank[v])", bg="#FFF2CC", bold=True, fontsize=11.0)
draw_box(ax, 25, 38, 45, 17, "First-Fit Formulation\n(welsh_powell_first_fit)\n• greedy_coloring(G, order=π)\n• Time: O(n log n + m)", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 75, 38, 45, 17, "Classical Sweep Formulation\n(welsh_powell)\n• Build color class c iteratively\n• Time: O(n log n + k·n + m)", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 50, 11, 80, 11, "Output: Identical Proper Coloring c: V → {0..k-1}\n(Equivalence verified by automated unit test suite)", bg="#D9E2F3", bold=True, fontsize=11.0)
draw_arrow(ax, 50, 78.5, 50, 71)
draw_arrow(ax, 40, 59, 25, 46.5)
draw_arrow(ax, 60, 59, 75, 46.5)
draw_arrow(ax, 25, 29.5, 42, 16.5)
draw_arrow(ax, 75, 29.5, 58, 16.5)
fig.tight_layout()
fig.savefig("Figures/diag5_welsh_powell.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 6. DSATUR Workflow
fig, ax = create_flowchart_canvas((8.0, 4.8), "Standard DSATUR Dynamic Workflow with Lazy Binary Heap")
draw_box(ax, 50, 85, 90, 11, "Initialize: colors[v] = -1, nbr_colors[v] = set(), udeg[v] = deg(v)\nPush (-sat(v), -udeg(v), rank[v], v) for all v ∈ V into Min-Heap", bg="#D9E2F3", bold=True, fontsize=11.0)
draw_box(ax, 50, 66, 90, 13, "Lazy Heap Extraction (pop_valid): Pop (-negsat, -negdeg, r, v)\n• If v colored or -negsat ≠ |nbr_colors[v]|: discard stale entry\n• If -negdeg ≠ udeg[v]: re-push (negsat, -udeg[v], r, v)", bg="#FFF2CC", fontsize=10.5)
draw_box(ax, 50, 45, 86, 11, "Assign Smallest Feasible Color:\nc = min { k ≥ 0 : k ∉ nbr_colors[v] }  →  colors[v] = c", bg="#E2EFDA", bold=True, fontsize=11.0)
draw_box(ax, 50, 26, 90, 12, "Update Uncolored Neighbors u ∈ G.adj[v]: Decrement udeg[u] -= 1\nIf c ∉ nbr_colors[u]: add c to nbr_colors[u] & push updated tuple", bg="#FCE4D6", fontsize=10.5)
draw_box(ax, 50, 9, 76, 9, "Repeat until remaining == 0  →  Return colors[0..n-1]", bg="#D9E2F3", bold=True, fontsize=11.0)
draw_arrow(ax, 50, 79.5, 50, 72.5)
draw_arrow(ax, 50, 59.5, 50, 50.5)
draw_arrow(ax, 50, 39.5, 50, 32)
draw_arrow(ax, 50, 20, 50, 13.5)
fig.tight_layout()
fig.savefig("Figures/diag6_dsatur.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 7. Improved DSATUR Workflow
fig, ax = create_flowchart_canvas((8.5, 5.2), "Improved DSATUR Five-Stage Pipeline (Preprocessing & Sewell Rule)")
draw_box(ax, 50, 86, 92, 10.5, "Stage 1: Multi-Start Greedy Maximal Clique (greedy_clique)\nFind clique Q from top-20 degree starts  →  Lower Bound LB = |Q| ≤ ω(G) ≤ χ(G)", bg="#D9E2F3", bold=True, fontsize=10.5)
draw_box(ax, 50, 69, 92, 12.5, "Stage 2: Iterative Graph Reduction (reduce_graph, up to 10 rounds)\n• Low-Degree Peeling: Remove v if deg(v) < LB; push v to stack\n• Non-Adjacent Domination: If (u, v) not in E and N(u) ⊆ N(v) (via pivot), remove u", bg="#FFF2CC", bold=True, fontsize=10.3)
draw_box(ax, 50, 51, 92, 10.5, "Stage 3: Subgraph Extraction & Clique Seeding\nBuild reduced subgraph H = G[kept]  •  Pre-color clique Q_H with colors 0..|Q|-1", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 50, 33, 92, 12.5, "Stage 4: DSATUR Engine with Sewell Tie-Breaking on H\nSelect max sat(v), max udeg(v); break ties (up to 8) by max Σ_{u∈N_uncol(v)} |A(v)∩A(u)|", bg="#FCE4D6", bold=True, fontsize=10.3)
draw_box(ax, 50, 14, 92, 10.5, "Stage 5: Solution Reconstruction & Reverse Stack Re-insertion\nMap H colors to G; pop removed v in reverse order and assign first_fit(adj[v], colors)", bg="#D9E2F3", bold=True, fontsize=10.5)
draw_arrow(ax, 50, 80.5, 50, 75.3)
draw_arrow(ax, 50, 62.7, 50, 56.3)
draw_arrow(ax, 50, 45.7, 50, 39.3)
draw_arrow(ax, 50, 26.7, 50, 19.3)
fig.tight_layout()
fig.savefig("Figures/diag7_improved_dsatur.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 8. Comparative Evaluation Pipeline
fig, ax = create_flowchart_canvas((8.2, 4.6), "Comparative Evaluation Metrics and Analysis Pipeline")
draw_box(ax, 50, 83, 88, 11, "Experimental Runs Matrix\n8 DIMACS Benchmarks + 31 Synthetic Configurations × 4 Algorithms × 10 Seeds", bg="#D9E2F3", bold=True, fontsize=11.0)
draw_box(ax, 17, 52, 30, 19, "Solution Quality\n• Colors Used (k)\n• Min & Mean ± SD\n• Relative Gain (%)\n  vs Basic Greedy", bg="#E2EFDA", fontsize=10.5)
draw_box(ax, 50, 52, 32, 19, "Optimality Gap\n• Exact Ratio: k / χ(G)\n  (Exact B&B / Known)\n• Clique Ratio: k / ω_LB\n  (via greedy_clique)", bg="#FFF2CC", fontsize=10.5)
draw_box(ax, 83, 52, 30, 19, "Computational Cost\n• Execution Time (ms)\n• Peak Memory (KB)\n• Reduction Shrinkage\n• Ablation Impact", bg="#FCE4D6", fontsize=10.5)
draw_box(ax, 50, 16, 88, 12, "Research Question Synthesis\nRQ1: Ordering Impact  |  RQ2: Preprocessing & Tie-Breaking  |  RQ3: Quality-Time-Memory", bg="#EDEDED", bold=True, fontsize=10.8)
draw_arrow(ax, 38, 77.5, 17, 61.5)
draw_arrow(ax, 50, 77.5, 50, 61.5)
draw_arrow(ax, 62, 77.5, 83, 61.5)
draw_arrow(ax, 17, 42.5, 40, 22)
draw_arrow(ax, 50, 42.5, 50, 22)
draw_arrow(ax, 83, 42.5, 60, 22)
fig.tight_layout()
fig.savefig("Figures/diag8_evaluation_pipeline.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Generating 10 Experimental Data Plots...")
sns.set_theme(style="whitegrid", font="serif")
PALETTE = {
    "Basic Greedy": "#7F8C8D",
    "Welsh-Powell": "#2980B9",
    "DSATUR": "#27AE60",
    "Improved DSATUR": "#C0392B"
}

df_runs = pd.read_csv("Experimental_Results/comprehensive_raw_results.csv")
df_agg = pd.read_csv("Experimental_Results/comprehensive_summary_results.csv")
df_eda = pd.read_csv("Experimental_Results/dataset_eda_summary.csv")
df_abl = pd.read_csv("Experimental_Results/ablation_study_results.csv")
df_pq = pd.read_csv("Experimental_Results/dsatur_heap_vs_naive.csv")

# Plot 1: DIMACS Benchmark Colors Comparison
plt.figure(figsize=(11, 5.5))
dim_df = df_runs[df_runs["Category"] == "DIMACS"]
order_dim = ["myciel3", "queen5_5", "myciel5", "queen8_8", "huck", "jean", "anna", "le450_15a"]
ax = sns.barplot(data=dim_df, x="Graph", y="colors", hue="Algorithm", order=order_dim, palette=PALETTE, errorbar="sd", capsize=0.08)
# Plot known chromatic numbers as black stars/markers
chi_map = {"myciel3": 4, "queen5_5": 5, "myciel5": 6, "queen8_8": 9, "huck": 11, "jean": 10, "anna": 11, "le450_15a": 15}
for idx, g in enumerate(order_dim):
    plt.scatter(idx, chi_map[g], color="gold", edgecolor="black", s=90, zorder=10, marker="*", label="Known χ(G)" if idx == 0 else "")
plt.title("Figure 8.1: Number of Colors Used Across DIMACS Benchmark Instances (Mean ± SD, 10 Seeds)", fontsize=12, fontweight="bold")
plt.xlabel("DIMACS Benchmark Instance", fontsize=11)
plt.ylabel("Number of Colors (k)", fontsize=11)
plt.legend(frameon=True, title="Algorithm / Bound")
plt.tight_layout()
plt.savefig("Figures/fig1_dimacs_colors.png", dpi=300)
plt.close()

# Plot 2: DIMACS Execution Time Comparison
plt.figure(figsize=(11, 5.2))
ax = sns.barplot(data=dim_df, x="Graph", y="time_s", hue="Algorithm", order=order_dim, palette=PALETTE, errorbar="sd")
plt.yscale("log")
plt.title("Figure 8.2: Execution Time on DIMACS Benchmark Instances (Log Scale, Seconds)", fontsize=12, fontweight="bold")
plt.xlabel("DIMACS Benchmark Instance", fontsize=11)
plt.ylabel("Execution Time (seconds, log scale)", fontsize=11)
plt.legend(frameon=True, title="Algorithm")
plt.tight_layout()
plt.savefig("Figures/fig2_dimacs_time.png", dpi=300)
plt.close()

# Plot 3: Number of Colors vs Number of Vertices (Scalability on ER and BA)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
er_scale = df_runs[df_runs["Graph"].isin(["ER(n=100,p=0.1)", "ER(n=500,p=0.1)", "ER(n=1000,p=0.1)"])]
sns.lineplot(data=er_scale, x="n", y="colors", hue="Algorithm", style="Algorithm", markers=True, dashes=False, palette=PALETTE, ax=axes[0], linewidth=2.2, markersize=8)
axes[0].set_title("(a) Erdős–Rényi G(n, p=0.1)", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Number of Vertices (n)")
axes[0].set_ylabel("Mean Colors Used (k)")
axes[0].set_xticks([100, 500, 1000])

ba_scale = df_runs[df_runs["Graph"].isin(["BA(n=100,m=5)", "BA(n=500,m=5)", "BA(n=1000,m=5)"])]
sns.lineplot(data=ba_scale, x="n", y="colors", hue="Algorithm", style="Algorithm", markers=True, dashes=False, palette=PALETTE, ax=axes[1], linewidth=2.2, markersize=8)
axes[1].set_title("(b) Barabási–Albert BA(n, m=5)", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Number of Vertices (n)")
axes[1].set_ylabel("Mean Colors Used (k)")
axes[1].set_xticks([100, 500, 1000])

fig.suptitle("Figure 8.3: Number of Colors Used vs. Graph Size (n) Across Random and Scale-Free Topologies", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig("Figures/fig3_colors_vs_n.png", dpi=300)
plt.close(fig)

# Plot 4: Execution Time vs Number of Vertices + Heap vs Naive DSATUR
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
sns.lineplot(data=er_scale, x="n", y="time_s", hue="Algorithm", style="Algorithm", markers=True, dashes=False, palette=PALETTE, ax=axes[0], linewidth=2.2, markersize=8)
axes[0].set_yscale("log")
axes[0].set_title("(a) All 4 Algorithms on ER(n, p=0.1) [Log Scale]", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Number of Vertices (n)")
axes[0].set_ylabel("Execution Time (seconds, log scale)")
axes[0].set_xticks([100, 500, 1000])

axes[1].plot(df_pq["n"], df_pq["Heap_DSATUR_ms"], marker="o", lw=2.2, color="#27AE60", label="Heap DSATUR O((n+m) log n)")
axes[1].plot(df_pq["n"], df_pq["Naive_DSATUR_ms"], marker="s", lw=2.2, color="#E67E22", linestyle="--", label="Naive DSATUR O(n² + m)")
axes[1].set_title("(b) Heap vs. Naive DSATUR Scaling on ER(n, p=0.1)", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Number of Vertices (n)")
axes[1].set_ylabel("Execution Time (milliseconds)")
axes[1].legend(frameon=True)

fig.suptitle("Figure 8.4: Execution Time Scalability with Graph Size (n) and Priority Queue Verification", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig("Figures/fig4_time_vs_n.png", dpi=300)
plt.close(fig)

# Plot 5: Performance vs Graph Density on Erdos-Renyi
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
er_dens100 = df_runs[df_runs["Graph"].isin(["ER(n=100,p=0.1)", "ER(n=100,p=0.3)", "ER(n=100,p=0.5)", "ER(n=100,p=0.7)", "ER(n=100,p=0.9)"])].copy()
er_dens100["p"] = er_dens100["Graph"].str.extract(r"p=([0-9.]+)").astype(float)
sns.lineplot(data=er_dens100, x="p", y="colors", hue="Algorithm", style="Algorithm", markers=True, dashes=False, palette=PALETTE, ax=axes[0], linewidth=2.2, markersize=8)
axes[0].set_title("(a) Colors Used vs. Edge Probability p (n = 100)", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Edge Probability / Density (p)")
axes[0].set_ylabel("Mean Colors Used (k)")

er_dens500 = df_runs[df_runs["Graph"].isin(["ER(n=500,p=0.1)", "ER(n=500,p=0.3)", "ER(n=500,p=0.5)"])].copy()
er_dens500["p"] = er_dens500["Graph"].str.extract(r"p=([0-9.]+)").astype(float)
sns.barplot(data=er_dens500, x="p", y="colors", hue="Algorithm", palette=PALETTE, ax=axes[1], errorbar="sd")
axes[1].set_title("(b) Colors Used vs. Edge Probability p (n = 500)", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Edge Probability / Density (p)")
axes[1].set_ylabel("Mean Colors Used (k)")

fig.suptitle("Figure 8.5: Impact of Graph Density (p) on Coloring Quality in Erdős–Rényi Graphs", fontsize=12, fontweight="bold")
fig.tight_layout()
fig.savefig("Figures/fig5_density_impact.png", dpi=300)
plt.close(fig)

# Plot 6: Algorithm Comparison Across Diverse Synthetic Graph Families (n=500 & Adversarial)
plt.figure(figsize=(11.5, 5.5))
fam_targets = ["ER(n=500,p=0.1)", "BA(n=500,m=5)", "RGG(n=500,r=0.1)", "Cycle(500)", "Complete(50)", "Crown(25)"]
fam_df = df_runs[df_runs["Graph"].isin(fam_targets)]
sns.barplot(data=fam_df, x="Graph", y="colors", hue="Algorithm", order=fam_targets, palette=PALETTE, errorbar="sd")
plt.title("Figure 8.6: Comparative Coloring Quality Across Synthetic Graph Topologies", fontsize=12, fontweight="bold")
plt.xlabel("Synthetic Graph Configuration", fontsize=11)
plt.ylabel("Number of Colors Used (k)", fontsize=11)
plt.xticks(rotation=15)
plt.legend(frameon=True, title="Algorithm")
plt.tight_layout()
plt.savefig("Figures/fig6_synthetic_families.png", dpi=300)
plt.close()

# Plot 7: Peak Memory Usage Comparison
plt.figure(figsize=(11, 5.2))
mem_targets = ["anna", "queen8_8", "le450_15a", "ER(n=500,p=0.1)", "ER(n=500,p=0.5)", "BA(n=500,m=5)", "RGG(n=500,r=0.1)"]
mem_df = df_runs[df_runs["Graph"].isin(mem_targets)].copy()
mem_df["memory_kb"] = mem_df["memory_mb"] * 1024.0
sns.barplot(data=mem_df, x="Graph", y="memory_kb", hue="Algorithm", order=mem_targets, palette=PALETTE, errorbar="sd")
plt.yscale("log")
plt.title("Figure 8.7: Peak Memory Consumption (tracemalloc, KB, Log Scale) Across Benchmark Instances", fontsize=12, fontweight="bold")
plt.xlabel("Graph Instance", fontsize=11)
plt.ylabel("Peak Traced Memory (KB, log scale)", fontsize=11)
plt.xticks(rotation=15)
plt.legend(frameon=True, title="Algorithm")
plt.tight_layout()
plt.savefig("Figures/fig7_memory_usage.png", dpi=300)
plt.close()

# Plot 8: Approximation Ratio Comparison (k / chi(G)) on Graphs with Known Chromatic Number
plt.figure(figsize=(11.5, 5.2))
ap_targets = ["myciel3", "myciel5", "queen5_5", "queen8_8", "jean", "anna", "huck", "le450_15a", "Cycle(51)", "Crown(25)"]
ap_df = df_runs[df_runs["Graph"].isin(ap_targets)].copy()
sns.barplot(data=ap_df, x="Graph", y="approx_ratio_chi", hue="Algorithm", order=ap_targets, palette=PALETTE, errorbar="sd")
plt.axhline(1.0, color="black", linestyle="--", linewidth=1.3, label="Optimal Ratio (1.0)")
plt.ylim(0.8, 2.3)
plt.title("Figure 8.8: Empirical Approximation Ratio k / χ(G) Across Instances with Known Chromatic Number", fontsize=12, fontweight="bold")
plt.xlabel("Graph Instance", fontsize=11)
plt.ylabel("Approximation Ratio (k / χ(G))", fontsize=11)
plt.xticks(rotation=20)
plt.legend(frameon=True, title="Algorithm", loc="upper right")
plt.tight_layout()
plt.savefig("Figures/fig8_approximation_ratio.png", dpi=300)
plt.close()

# Plot 9: Exploratory Data Analysis — Degree Distributions & Density Comparison
fig, axes = plt.subplots(2, 2, figsize=(12, 8.2))
G_er = erdos_renyi(500, 0.1, seed=100)
G_ba = barabasi_albert(500, 5, seed=100)
G_rgg = random_geometric(500, 0.1, seed=100)
G_le = load_dimacs("data/le450_15a.col")

sns.histplot(G_er.degrees(), kde=True, color="#2980B9", ax=axes[0, 0], bins=18)
axes[0, 0].set_title("(a) Erdős–Rényi ER(500, 0.1) — Binomial", fontsize=10, fontweight="bold")
axes[0, 0].set_xlabel("Vertex Degree")
axes[0, 0].set_ylabel("Vertex Count")

sns.histplot(G_ba.degrees(), kde=False, color="#C0392B", ax=axes[0, 1], bins=25)
axes[0, 1].set_yscale("log")
axes[0, 1].set_title("(b) Barabási–Albert BA(500, 5) — Scale-Free (Log Y)", fontsize=10, fontweight="bold")
axes[0, 1].set_xlabel("Vertex Degree")
axes[0, 1].set_ylabel("Vertex Count (log scale)")

sns.histplot(G_rgg.degrees(), kde=True, color="#27AE60", ax=axes[1, 0], bins=18)
axes[1, 0].set_title("(c) Random Geometric RGG(500, 0.1) — Spatial", fontsize=10, fontweight="bold")
axes[1, 0].set_xlabel("Vertex Degree")
axes[1, 0].set_ylabel("Vertex Count")

sns.histplot(G_le.degrees(), kde=True, color="#8E44AD", ax=axes[1, 1], bins=20)
axes[1, 1].set_title("(d) DIMACS le450_15a (n=450, m=8168)", fontsize=10, fontweight="bold")
axes[1, 1].set_xlabel("Vertex Degree")
axes[1, 1].set_ylabel("Vertex Count")

fig.suptitle("Figure 8.9: Exploratory Data Analysis — Vertex Degree Distributions Across Graph Families", fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("Figures/fig9_eda_degree_distributions.png", dpi=300)
plt.close(fig)

# Plot 10: Ablation Study & Graph Reduction Analysis
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4))
abl_sub = df_abl[df_abl["Graph"].isin(["queen8_8", "le450_15a", "ER(n=500,p=0.1)"])]
sns.barplot(data=abl_sub, x="Graph", y="colors_mean", hue="Variant", ax=axes[0], palette="viridis")
axes[0].set_title("(a) Ablation of Improved DSATUR (Mean Colors)", fontsize=10.5, fontweight="bold")
axes[0].set_xlabel("Graph Instance")
axes[0].set_ylabel("Mean Colors Used (10 Seeds)")
axes[0].set_ylim(8, 20)
axes[0].legend(frameon=True, fontsize=8, title="Configuration")

df_diag = pd.read_csv("Experimental_Results/improved_dsatur_diagnostics.csv")
red_sub = df_diag[df_diag["Reduction_Pct"] > 0].sort_values("Reduction_Pct", ascending=False)
sns.barplot(data=red_sub, x="Reduction_Pct", y="Graph", color="#C0392B", ax=axes[1])
axes[1].set_title("(b) Vertices Removed by Reductions (%)", fontsize=10.5, fontweight="bold")
axes[1].set_xlabel("Vertices Removed Prior to DSATUR (%)")
axes[1].set_ylabel("Graph Instance")

fig.suptitle("Figure 8.10: Ablation Analysis and Vertex Reduction Effectiveness in Improved DSATUR", fontsize=12, fontweight="bold")
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("Figures/fig10_ablation_and_reduction.png", dpi=300)
plt.close(fig)

print("All 18 figures generated successfully in Figures/!")
