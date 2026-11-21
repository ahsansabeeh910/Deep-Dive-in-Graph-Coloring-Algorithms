"""Algorithm 2 - Welsh-Powell colouring (Welsh & Powell, 1967).

The vertices are sorted by non-increasing degree. Colour classes are then
built one at a time: sweep the sorted list, giving the current colour to
every uncoloured vertex that has no neighbour of that colour yet; repeat with
the next colour until every vertex is coloured. This is the formulation in
the original paper.

The sweep produces exactly the same colouring as first-fit greedy applied to
the degree-sorted order (a vertex receives colour c in sweep c iff no earlier
vertex adjacent to it holds c), which is verified in the test-suite.

Complexity
----------
Sorting                : O(n log n)
Sweeps (this version)  : O(k * n + m) - each of the k sweeps scans the remaining
                         vertices, and each vertex's adjacency list is
                         processed once, when it is coloured.
First-fit formulation  : O(n log n + m), see ``welsh_powell_first_fit``.
Space                  : O(n).

Quality: uses at most max_i min(d(v_i) + 1, i) colours, where v_1, v_2, ...
is the degree-sorted order, and hence at most Delta + 1.
"""

from __future__ import annotations

from ..coloring import UNCOLORED, make_rank
from ..graph import Graph
from .greedy import greedy_coloring


def degree_order(G: Graph, seed: int | None = None) -> list[int]:
    """Vertices by non-increasing degree; equal degrees keep the input order."""
    rank = make_rank(G.n, seed)
    adj = G.adj
    return sorted(range(G.n), key=lambda v: (-len(adj[v]), rank[v]))


def welsh_powell(G: Graph, seed: int | None = None) -> list[int]:
    """Welsh-Powell colouring using the class-by-class sweep of the paper."""
    adj = G.adj
    colors = [UNCOLORED] * G.n
    remaining = degree_order(G, seed)
    c = 0
    while remaining:
        blocked: set[int] = set()  # vertices adjacent to some vertex of colour c
        deferred = []
        for v in remaining:
            if v in blocked:
                deferred.append(v)
            else:
                colors[v] = c
                blocked.update(adj[v])
        remaining = deferred
        c += 1
    return colors


def welsh_powell_first_fit(G: Graph, seed: int | None = None) -> list[int]:
    """Equivalent O(n log n + m) formulation: first-fit on the degree order."""
    return greedy_coloring(G, order=degree_order(G, seed))
