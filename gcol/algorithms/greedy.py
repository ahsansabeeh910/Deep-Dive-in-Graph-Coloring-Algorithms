"""Algorithm 1 - Basic Greedy (first-fit) colouring.

Vertices are visited in a fixed order and each one receives the smallest
colour not already used by a coloured neighbour.

Complexity
----------
Time  : O(n + m) - every vertex is visited once and every edge is inspected
        twice (once from each endpoint); the inner ``while`` loop runs at most
        deg(v) + 1 times for vertex v.
Space : O(n) working memory besides the graph.

Quality: no useful guarantee. A bad order can force n/2 colours on a bipartite
graph (see :func:`gcol.generators.crown_graph`), although first-fit never uses
more than Delta + 1 colours.
"""

from __future__ import annotations

from typing import Sequence

from ..coloring import UNCOLORED, input_order
from ..graph import Graph


def greedy_coloring(G: Graph, seed: int | None = None, order: Sequence[int] | None = None) -> list[int]:
    """Colour ``G`` greedily.

    Parameters
    ----------
    G:
        Graph to colour.
    seed:
        Selects the input order (``None`` = natural order ``0..n-1``,
        otherwise a random permutation). Ignored if ``order`` is given.
    order:
        Explicit vertex order to use.
    """
    adj = G.adj
    colors = [UNCOLORED] * G.n
    if order is None:
        order = input_order(G.n, seed)
    for v in order:
        used = {colors[u] for u in adj[v]}
        c = 0
        while c in used:
            c += 1
        colors[v] = c
    return colors
