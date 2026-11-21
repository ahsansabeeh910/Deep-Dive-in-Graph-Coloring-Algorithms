"""Synthetic graph generators based on NetworkX."""

from __future__ import annotations

import networkx as nx

from .graph import Graph


def erdos_renyi(n: int, p: float, seed: int | None = None) -> Graph:
    """G(n, p) random graph."""
    G = nx.erdos_renyi_graph(n, p, seed=seed)
    return Graph.from_networkx(G, name=f"ER(n={n},p={p})")


def barabasi_albert(n: int, m: int, seed: int | None = None) -> Graph:
    """Scale-free random graph."""
    if m < 1 or m >= n:
        raise ValueError("m must be in [1, n)")
    G = nx.barabasi_albert_graph(n, m, seed=seed)
    return Graph.from_networkx(G, name=f"BA(n={n},m={m})")


def random_geometric(n: int, radius: float, seed: int | None = None) -> Graph:
    """Random geometric graph in the unit square."""
    G = nx.random_geometric_graph(n, radius, seed=seed)
    return Graph.from_networkx(G, name=f"RGG(n={n},r={radius})")


def cycle_graph(n: int) -> Graph:
    """Cycle graph C_n (chi=2 if even, chi=3 if odd)."""
    G = nx.cycle_graph(n)
    return Graph.from_networkx(G, name=f"Cycle({n})")


def complete_graph(n: int) -> Graph:
    """Complete graph K_n (chi=n)."""
    G = nx.complete_graph(n)
    return Graph.from_networkx(G, name=f"Complete({n})")


def crown_graph(n: int) -> Graph:
    """Bipartite graph with 2n vertices (chi=2) that defeats bad greedy orders."""
    G = nx.Graph()
    G.add_nodes_from(range(2 * n))
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i, n + j)
    return Graph.from_networkx(G, name=f"Crown({n})")
