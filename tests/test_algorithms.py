import pytest
from gcol.graph import Graph
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
from gcol.coloring import is_proper, num_colors
from gcol.generators import cycle_graph, complete_graph, crown_graph, erdos_renyi

ALGORITHMS = [
    greedy_coloring,
    welsh_powell,
    welsh_powell_first_fit,
    dsatur,
    dsatur_naive,
    improved_dsatur,
]

def test_complete_graph():
    G = complete_graph(5)
    for algo in ALGORITHMS:
        colors = algo(G)
        assert is_proper(G, colors)
        assert num_colors(colors) == 5

def test_cycle_graph():
    # C_5 chi = 3
    G = cycle_graph(5)
    for algo in ALGORITHMS:
        colors = algo(G)
        assert is_proper(G, colors)

def test_bipartite_crown():
    # Crown graph chi = 2
    G = crown_graph(3)
    for algo in ALGORITHMS:
        colors = algo(G)
        assert is_proper(G, colors)
        if algo not in (greedy_coloring, welsh_powell, welsh_powell_first_fit):
            # DSATUR variants should easily find 2 colors
            assert num_colors(colors) == 2

def test_dsatur_equivalences():
    G = erdos_renyi(30, 0.3, seed=42)
    # Both heap and naive should produce identical colourings (by same seed)
    c1 = dsatur(G, seed=10)
    c2 = dsatur_naive(G, seed=10)
    assert c1 == c2

def test_welsh_powell_equivalences():
    G = erdos_renyi(30, 0.3, seed=42)
    c1 = welsh_powell(G, seed=10)
    c2 = welsh_powell_first_fit(G, seed=10)
    assert c1 == c2

def test_exact_solver():
    G = cycle_graph(5)
    assert chromatic_number(G) == 3
    
    G = complete_graph(6)
    assert chromatic_number(G) == 6
    
    G = crown_graph(4)
    assert chromatic_number(G) == 2
