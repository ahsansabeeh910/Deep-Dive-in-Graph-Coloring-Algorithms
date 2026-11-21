import os
import time
import tracemalloc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from gcol.graph import Graph
from gcol.dimacs import load_dimacs
from gcol.coloring import num_colors, assert_proper
from gcol.algorithms import (
    greedy_coloring,
    welsh_powell_first_fit,
    dsatur,
    improved_dsatur
)
from gcol.generators import (
    erdos_renyi,
    barabasi_albert,
    random_geometric
)

# Configuration
SEEDS = 10
SYNTHETIC_INSTANCES = 3

ALGORITHMS = {
    "Basic Greedy": greedy_coloring,
    "Welsh-Powell": welsh_powell_first_fit,
    "DSATUR": dsatur,
    "Improved DSATUR": improved_dsatur
}

def measure_algorithm(algo_func, G, seed):
    tracemalloc.start()
    start_time = time.perf_counter()
    
    colors = algo_func(G, seed=seed)
    
    end_time = time.perf_counter()
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    assert_proper(G, colors)
    k = num_colors(colors)
    
    return {
        "colors": k,
        "time_s": end_time - start_time,
        "memory_mb": peak_mem / (1024 * 1024)
    }

def run_experiments():
    results = []
    
    # 1. DIMACS Benchmarks
    dimacs_files = [
        "data/myciel3.col",
        "data/myciel5.col",
        "data/queen5_5.col",
        "data/queen8_8.col",
        "data/jean.col",
        "data/anna.col"
    ]
    
    print("--- Running DIMACS Benchmarks ---")
    for f in dimacs_files:
        if not os.path.exists(f):
            print(f"Skipping {f}, not found.")
            continue
        G = load_dimacs(f)
        print(f"Loaded {G.name}: n={G.n}, m={G.m}")
        
        for algo_name, algo_func in ALGORITHMS.items():
            for seed in range(SEEDS):
                res = measure_algorithm(algo_func, G, seed)
                results.append({
                    "Dataset": "DIMACS",
                    "Graph": G.name,
                    "n": G.n,
                    "m": G.m,
                    "Algorithm": algo_name,
                    "Seed": seed,
                    **res
                })
                
    # 2. Synthetic Graphs
    print("\n--- Running Synthetic Benchmarks ---")
    synthetic_configs = [
        ("ER(n=500,p=0.1)", lambda s: erdos_renyi(500, 0.1, seed=s)),
        ("ER(n=500,p=0.5)", lambda s: erdos_renyi(500, 0.5, seed=s)),
        ("BA(n=500,m=5)", lambda s: barabasi_albert(500, 5, seed=s)),
        ("RGG(n=500,r=0.1)", lambda s: random_geometric(500, 0.1, seed=s))
    ]
    
    for graph_name, gen_func in synthetic_configs:
        print(f"Generating {graph_name}...")
        for inst in range(SYNTHETIC_INSTANCES):
            G = gen_func(100 + inst) # Seed for graph generation
            for algo_name, algo_func in ALGORITHMS.items():
                for seed in range(SEEDS):
                    res = measure_algorithm(algo_func, G, seed)
                    results.append({
                        "Dataset": "Synthetic",
                        "Graph": graph_name,
                        "n": G.n,
                        "m": G.m,
                        "Algorithm": algo_name,
                        "Seed": seed,
                        **res
                    })

    df = pd.DataFrame(results)
    
    # Save raw results
    os.makedirs("results", exist_ok=True)
    df.to_csv("results/raw_results.csv", index=False)
    
    # Aggregation
    agg_df = df.groupby(["Dataset", "Graph", "Algorithm"]).agg({
        "colors": ["mean", "std", "min"],
        "time_s": "mean",
        "memory_mb": "mean"
    }).reset_index()
    
    # Flatten columns
    agg_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in agg_df.columns.values]
    agg_df.to_csv("results/summary_results.csv", index=False)
    
    print("\n--- Summary ---")
    print(agg_df.to_string())
    
    # Visualization
    sns.set_theme(style="whitegrid")
    
    # 1. Colors Plot
    plt.figure(figsize=(12, 6))
    dimacs_df = df[df["Dataset"] == "DIMACS"]
    if not dimacs_df.empty:
        sns.barplot(data=dimacs_df, x="Graph", y="colors", hue="Algorithm", errorbar="sd")
        plt.title("Colors Used - DIMACS Benchmarks")
        plt.ylabel("Number of Colors")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("results/plot_colors_dimacs.png", dpi=300)
    
    # 2. Time Plot
    plt.figure(figsize=(12, 6))
    if not dimacs_df.empty:
        sns.barplot(data=dimacs_df, x="Graph", y="time_s", hue="Algorithm", errorbar="sd")
        plt.title("Execution Time - DIMACS Benchmarks")
        plt.ylabel("Time (seconds)")
        plt.yscale("log")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("results/plot_time_dimacs.png", dpi=300)

    # 3. Colors Plot (Synthetic)
    plt.figure(figsize=(12, 6))
    synth_df = df[df["Dataset"] == "Synthetic"]
    if not synth_df.empty:
        sns.barplot(data=synth_df, x="Graph", y="colors", hue="Algorithm", errorbar="sd")
        plt.title("Colors Used - Synthetic Graphs")
        plt.ylabel("Number of Colors")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("results/plot_colors_synthetic.png", dpi=300)
        
    print("\nPlots saved in results/ directory.")

if __name__ == "__main__":
    run_experiments()
