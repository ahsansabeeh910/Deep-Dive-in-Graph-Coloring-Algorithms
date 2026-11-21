"""Comprehensive evaluation, analysis, and diagram/plot generation script for the Final Report."""

import os
import time
import tracemalloc
import shutil
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

from gcol.graph import Graph
from gcol.dimacs import load_dimacs
from gcol.coloring import num_colors, assert_proper
from gcol.bounds import greedy_clique, max_clique
from gcol.algorithms import (
    greedy_coloring,
    welsh_powell,
    welsh_powell_first_fit,
    dsatur,
    dsatur_naive,
    improved_dsatur,
    exact_coloring,
    chromatic_number
)
from gcol.generators import (
    erdos_renyi,
    barabasi_albert,
    random_geometric,
    cycle_graph,
    complete_graph,
    crown_graph
)

os.makedirs("Experimental_Results", exist_ok=True)
os.makedirs("Figures", exist_ok=True)

# Copy existing results to Experimental_Results and Figures
if os.path.exists("results/raw_results.csv"):
    shutil.copy("results/raw_results.csv", "Experimental_Results/baseline_raw_results.csv")
if os.path.exists("results/summary_results.csv"):
    shutil.copy("results/summary_results.csv", "Experimental_Results/baseline_summary_results.csv")

ALGORITHMS = {
    "Basic Greedy": greedy_coloring,
    "Welsh-Powell": welsh_powell_first_fit,
    "DSATUR": dsatur,
    "Improved DSATUR": improved_dsatur
}

KNOWN_CHI_DIMACS = {
    "myciel3": 4,
    "myciel5": 6,
    "queen5_5": 5,
    "queen8_8": 9,
    "jean": 10,
    "anna": 11,
    "huck": 11,
    "le450_15a": 15
}

def measure_run(algo_func, G, seed, **kwargs):
    tracemalloc.start()
    t0 = time.perf_counter()
    colors = algo_func(G, seed=seed, **kwargs)
    dt = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert_proper(G, colors)
    return num_colors(colors), dt, peak / (1024 * 1024)

def compute_graph_eda(G: Graph, family: str, params_str: str, known_chi=None):
    degs = G.degrees()
    nxG = G.to_networkx()
    avg_clust = nx.average_clustering(nxG) if G.n <= 1500 else 0.0
    clique_g = greedy_clique(G)
    omega_lb = len(clique_g)
    exact_chi = known_chi
    if exact_chi is None and G.n <= 50:
        res = exact_coloring(G, time_limit=5.0)
        if res.optimal:
            exact_chi = res.chi
    return {
        "Family": family,
        "Graph": G.name,
        "Parameters": params_str,
        "n": G.n,
        "m": G.m,
        "Density": round(G.density(), 4),
        "Min_Degree": int(min(degs)) if degs else 0,
        "Avg_Degree": round(float(np.mean(degs)), 2) if degs else 0.0,
        "Std_Degree": round(float(np.std(degs)), 2) if degs else 0.0,
        "Max_Degree": int(max(degs)) if degs else 0,
        "Avg_Clustering": round(avg_clust, 4),
        "Clique_LB_omega": omega_lb,
        "Known_or_Exact_Chi": exact_chi if exact_chi is not None else "Unknown"
    }

print("1. Computing EDA and running comprehensive DIMACS + Synthetic benchmarks...")
eda_rows = []
all_runs = []
diag_rows = []

# --- A. DIMACS Instances ---
dimacs_list = ["myciel3", "myciel5", "queen5_5", "queen8_8", "jean", "anna", "huck", "le450_15a"]
for name in dimacs_list:
    path = f"data/{name}.col"
    if not os.path.exists(path):
        continue
    G = load_dimacs(path)
    chi = KNOWN_CHI_DIMACS.get(name)
    eda_info = compute_graph_eda(G, "DIMACS", "Standard Benchmark", known_chi=chi)
    eda_rows.append(eda_info)
    omega = eda_info["Clique_LB_omega"]

    # Record Improved DSATUR diagnostics for seed=0
    info_d = {}
    c_diag = improved_dsatur(G, seed=0, info=info_d)
    diag_rows.append({
        "Graph": G.name, "Family": "DIMACS", "n": G.n, "m": G.m,
        "Clique_LB": info_d.get("lb", 0),
        "Removed_LowDeg": info_d.get("removed_low_degree", 0),
        "Removed_Dominated": info_d.get("removed_dominated", 0),
        "n_Reduced": info_d.get("n_reduced", G.n),
        "m_Reduced": info_d.get("m_reduced", G.m),
        "Reduction_Pct": round(100.0 * (G.n - info_d.get("n_reduced", G.n)) / G.n, 2),
        "Ties_Examined": info_d.get("ties_examined", 0),
        "Ties_Changed": info_d.get("ties_changed", 0),
        "Colors_Used": num_colors(c_diag)
    })

    for algo_name, algo_fn in ALGORITHMS.items():
        for seed in range(10):
            k, dt, mem = measure_run(algo_fn, G, seed)
            all_runs.append({
                "Category": "DIMACS", "Family": "DIMACS", "Graph": G.name,
                "n": G.n, "m": G.m, "Density": G.density(),
                "Instance": 0, "Seed": seed, "Algorithm": algo_name,
                "colors": k, "time_s": dt, "memory_mb": mem,
                "chi": chi, "omega_lb": omega,
                "approx_ratio_chi": k / chi if chi else np.nan,
                "approx_ratio_omega": k / omega if omega else np.nan
            })

# --- B. Synthetic Graph Families ---
synth_specs = [
    # Erdos-Renyi varying n (p=0.1)
    ("Erdos-Renyi", "ER(n=100,p=0.1)", "n=100, p=0.1", lambda s: erdos_renyi(100, 0.1, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=500,p=0.1)", "n=500, p=0.1", lambda s: erdos_renyi(500, 0.1, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=1000,p=0.1)", "n=1000, p=0.1", lambda s: erdos_renyi(1000, 0.1, seed=s), None, 3),
    # Erdos-Renyi varying density p (n=100 and n=500)
    ("Erdos-Renyi", "ER(n=100,p=0.3)", "n=100, p=0.3", lambda s: erdos_renyi(100, 0.3, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=100,p=0.5)", "n=100, p=0.5", lambda s: erdos_renyi(100, 0.5, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=100,p=0.7)", "n=100, p=0.7", lambda s: erdos_renyi(100, 0.7, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=100,p=0.9)", "n=100, p=0.9", lambda s: erdos_renyi(100, 0.9, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=500,p=0.3)", "n=500, p=0.3", lambda s: erdos_renyi(500, 0.3, seed=s), None, 3),
    ("Erdos-Renyi", "ER(n=500,p=0.5)", "n=500, p=0.5", lambda s: erdos_renyi(500, 0.5, seed=s), None, 3),
    # Barabasi-Albert varying n and m
    ("Barabasi-Albert", "BA(n=100,m=2)", "n=100, m=2", lambda s: barabasi_albert(100, 2, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=100,m=5)", "n=100, m=5", lambda s: barabasi_albert(100, 5, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=100,m=10)", "n=100, m=10", lambda s: barabasi_albert(100, 10, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=500,m=2)", "n=500, m=2", lambda s: barabasi_albert(500, 2, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=500,m=5)", "n=500, m=5", lambda s: barabasi_albert(500, 5, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=500,m=10)", "n=500, m=10", lambda s: barabasi_albert(500, 10, seed=s), None, 3),
    ("Barabasi-Albert", "BA(n=1000,m=5)", "n=1000, m=5", lambda s: barabasi_albert(1000, 5, seed=s), None, 3),
    # Random Geometric
    ("Random Geometric", "RGG(n=100,r=0.1)", "n=100, r=0.1", lambda s: random_geometric(100, 0.1, seed=s), None, 3),
    ("Random Geometric", "RGG(n=100,r=0.2)", "n=100, r=0.2", lambda s: random_geometric(100, 0.2, seed=s), None, 3),
    ("Random Geometric", "RGG(n=100,r=0.3)", "n=100, r=0.3", lambda s: random_geometric(100, 0.3, seed=s), None, 3),
    ("Random Geometric", "RGG(n=500,r=0.1)", "n=500, r=0.1", lambda s: random_geometric(500, 0.1, seed=s), None, 3),
    ("Random Geometric", "RGG(n=500,r=0.2)", "n=500, r=0.2", lambda s: random_geometric(500, 0.2, seed=s), None, 3),
    ("Random Geometric", "RGG(n=1000,r=0.1)", "n=1000, r=0.1", lambda s: random_geometric(1000, 0.1, seed=s), None, 3),
    # Cycle Graphs
    ("Cycle", "Cycle(50)", "n=50 (even)", lambda s: cycle_graph(50), 2, 1),
    ("Cycle", "Cycle(51)", "n=51 (odd)", lambda s: cycle_graph(51), 3, 1),
    ("Cycle", "Cycle(100)", "n=100 (even)", lambda s: cycle_graph(100), 2, 1),
    ("Cycle", "Cycle(500)", "n=500 (even)", lambda s: cycle_graph(500), 2, 1),
    # Complete Graphs
    ("Complete", "Complete(10)", "n=10", lambda s: complete_graph(10), 10, 1),
    ("Complete", "Complete(20)", "n=20", lambda s: complete_graph(20), 20, 1),
    ("Complete", "Complete(50)", "n=50", lambda s: complete_graph(50), 50, 1),
    ("Complete", "Complete(100)", "n=100", lambda s: complete_graph(100), 100, 1),
    # Crown Graph (bipartite adversarial)
    ("Crown", "Crown(25)", "2n=50 (bipartite)", lambda s: crown_graph(25), 2, 1),
]

for family, gname, pstr, gen_fn, known_chi, n_inst in synth_specs:
    print(f"  Running {gname}...")
    for inst in range(n_inst):
        G = gen_fn(100 + inst)
        G.name = gname
        if inst == 0:
            eda_info = compute_graph_eda(G, family, pstr, known_chi=known_chi)
            eda_rows.append(eda_info)
            info_d = {}
            c_diag = improved_dsatur(G, seed=0, info=info_d)
            diag_rows.append({
                "Graph": G.name, "Family": family, "n": G.n, "m": G.m,
                "Clique_LB": info_d.get("lb", 0),
                "Removed_LowDeg": info_d.get("removed_low_degree", 0),
                "Removed_Dominated": info_d.get("removed_dominated", 0),
                "n_Reduced": info_d.get("n_reduced", G.n),
                "m_Reduced": info_d.get("m_reduced", G.m),
                "Reduction_Pct": round(100.0 * (G.n - info_d.get("n_reduced", G.n)) / G.n, 2),
                "Ties_Examined": info_d.get("ties_examined", 0),
                "Ties_Changed": info_d.get("ties_changed", 0),
                "Colors_Used": num_colors(c_diag)
            })
        omega = len(greedy_clique(G))
        chi_val = known_chi if known_chi is not None else (eda_info["Known_or_Exact_Chi"] if isinstance(eda_info["Known_or_Exact_Chi"], int) else None)
        for algo_name, algo_fn in ALGORITHMS.items():
            for seed in range(10):
                k, dt, mem = measure_run(algo_fn, G, seed)
                all_runs.append({
                    "Category": "Synthetic", "Family": family, "Graph": gname,
                    "n": G.n, "m": G.m, "Density": G.density(),
                    "Instance": inst, "Seed": seed, "Algorithm": algo_name,
                    "colors": k, "time_s": dt, "memory_mb": mem,
                    "chi": chi_val, "omega_lb": omega,
                    "approx_ratio_chi": k / chi_val if chi_val else np.nan,
                    "approx_ratio_omega": k / omega if omega else np.nan
                })

df_eda = pd.DataFrame(eda_rows)
df_eda.to_csv("Experimental_Results/dataset_eda_summary.csv", index=False)

df_diag = pd.DataFrame(diag_rows)
df_diag.to_csv("Experimental_Results/improved_dsatur_diagnostics.csv", index=False)

df_runs = pd.DataFrame(all_runs)
df_runs.to_csv("Experimental_Results/comprehensive_raw_results.csv", index=False)

# Aggregate summary
agg = df_runs.groupby(["Category", "Family", "Graph", "n", "Algorithm"]).agg(
    m_mean=("m", "mean"),
    density_mean=("Density", "mean"),
    colors_mean=("colors", "mean"),
    colors_std=("colors", "std"),
    colors_min=("colors", "min"),
    colors_max=("colors", "max"),
    time_ms_mean=("time_s", lambda x: np.mean(x) * 1000.0),
    time_ms_std=("time_s", lambda x: np.std(x) * 1000.0),
    memory_kb_mean=("memory_mb", lambda x: np.mean(x) * 1024.0),
    chi=("chi", "first"),
    omega_lb=("omega_lb", "mean"),
    approx_chi_mean=("approx_ratio_chi", "mean"),
    approx_omega_mean=("approx_ratio_omega", "mean"),
).reset_index()

# Compute relative improvement over Basic Greedy for each Graph
greedy_means = agg[agg["Algorithm"] == "Basic Greedy"].set_index("Graph")["colors_mean"].to_dict()
agg["rel_improv_pct"] = agg.apply(
    lambda r: round(100.0 * (greedy_means[r["Graph"]] - r["colors_mean"]) / greedy_means[r["Graph"]], 2)
    if r["Graph"] in greedy_means and greedy_means[r["Graph"]] > 0 else 0.0,
    axis=1
)
agg.to_csv("Experimental_Results/comprehensive_summary_results.csv", index=False)

# --- C. Exact Chromatic Number Evaluation on Small Graphs (n <= 50) ---
print("2. Running Exact Solver on small graphs...")
small_graphs = [
    load_dimacs("data/myciel3.col"),
    load_dimacs("data/myciel5.col"),
    load_dimacs("data/queen5_5.col"),
    cycle_graph(50),
    cycle_graph(51),
    complete_graph(10),
    complete_graph(20),
    crown_graph(20),
    erdos_renyi(30, 0.2, seed=42),
    erdos_renyi(30, 0.5, seed=42),
    barabasi_albert(35, 3, seed=42),
    random_geometric(35, 0.25, seed=42)
]
exact_rows = []
for G in small_graphs:
    ex = exact_coloring(G, time_limit=10.0)
    c_g = num_colors(greedy_coloring(G, seed=0))
    c_wp = num_colors(welsh_powell_first_fit(G, seed=0))
    c_ds = num_colors(dsatur(G, seed=0))
    c_ids = num_colors(improved_dsatur(G, seed=0))
    exact_rows.append({
        "Graph": G.name, "n": G.n, "m": G.m,
        "Clique_LB": ex.lower_bound,
        "Exact_or_UB_Chi": ex.chi,
        "Optimal_Proven": ex.optimal,
        "BB_Nodes": ex.nodes,
        "Exact_Time_ms": round(ex.time * 1000.0, 3),
        "Greedy_k": c_g, "WP_k": c_wp, "DSATUR_k": c_ds, "ImpDSATUR_k": c_ids,
        "ImpDSATUR_Approx_Ratio": round(c_ids / ex.chi, 4)
    })
df_exact = pd.DataFrame(exact_rows)
df_exact.to_csv("Experimental_Results/exact_solver_results.csv", index=False)

# --- D. Ablation Study of Improved DSATUR ---
print("3. Running Ablation Study on Improved DSATUR...")
ablation_configs = [
    ("Standard DSATUR (Baseline)", False, False, False),
    ("+ Sewell Tie-Break Only", True, False, False),
    ("+ Clique Pre-color Only", False, True, False),
    ("+ Graph Reduction Only", False, False, True),
    ("+ Tie-Break & Clique", True, True, False),
    ("Full Improved DSATUR (All 3)", True, True, True),
]
ablation_targets = [
    load_dimacs("data/queen8_8.col"),
    load_dimacs("data/le450_15a.col"),
    load_dimacs("data/anna.col"),
    erdos_renyi(500, 0.1, seed=100),
    barabasi_albert(500, 5, seed=100),
    random_geometric(500, 0.1, seed=100),
]
ablation_rows = []
for G in ablation_targets:
    for cfg_name, tb, clq, red in ablation_configs:
        ks, ts = [], []
        for s in range(10):
            t0 = time.perf_counter()
            c = improved_dsatur(G, seed=s, use_tiebreak=tb, use_clique=clq, use_reduction=red)
            dt = (time.perf_counter() - t0) * 1000.0
            ks.append(num_colors(c))
            ts.append(dt)
        ablation_rows.append({
            "Graph": G.name, "n": G.n, "m": G.m,
            "Variant": cfg_name,
            "use_tiebreak": tb, "use_clique": clq, "use_reduction": red,
            "colors_mean": round(float(np.mean(ks)), 2),
            "colors_std": round(float(np.std(ks)), 2),
            "colors_min": int(min(ks)),
            "time_ms_mean": round(float(np.mean(ts)), 3)
        })
df_ablation = pd.DataFrame(ablation_rows)
df_ablation.to_csv("Experimental_Results/ablation_study_results.csv", index=False)

# --- E. Priority Queue vs Naive DSATUR Scaling ---
print("4. Running Heap vs Naive DSATUR Scaling...")
pq_rows = []
for n_val in [100, 250, 500, 1000, 2000]:
    G = erdos_renyi(n_val, 0.1, seed=42)
    t0 = time.perf_counter()
    c1 = dsatur(G, seed=0)
    t_heap = (time.perf_counter() - t0) * 1000.0
    t0 = time.perf_counter()
    c2 = dsatur_naive(G, seed=0)
    t_naive = (time.perf_counter() - t0) * 1000.0
    assert c1 == c2
    pq_rows.append({
        "n": n_val, "m": G.m, "colors": num_colors(c1),
        "Heap_DSATUR_ms": round(t_heap, 3),
        "Naive_DSATUR_ms": round(t_naive, 3),
        "Speedup_Ratio": round(t_naive / max(t_heap, 1e-6), 2)
    })
df_pq = pd.DataFrame(pq_rows)
df_pq.to_csv("Experimental_Results/dsatur_heap_vs_naive.csv", index=False)

print("All CSVs saved successfully!")
