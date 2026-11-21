"""Exact chromatic number by DSATUR-based branch and bound (Brelaz, 1979).

Used only to obtain the *true* chromatic number of small graphs so that the
approximation ratio  colours_used / chi(G)  of the heuristics can be measured.

Search
------
* Upper bound: best of DSATUR and Improved DSATUR.
* Lower bound: a maximum clique (exact for small graphs, greedy otherwise).
  The clique is pre-coloured 0..q-1 at the root, which also removes colour
  symmetry for those vertices.
* Branching: the uncoloured vertex of maximum saturation (ties: uncoloured
  degree) is tried with every feasible used colour, then with one new colour
  if that still beats the incumbent.
* Pruning: a partial colouring with k >= best colours is abandoned; the
  search stops immediately when best == lower bound.

Worst-case time is exponential; a time limit returns the best colouring
found together with ``optimal=False``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from ..bounds import greedy_clique, max_clique
from ..coloring import UNCOLORED, num_colors
from ..graph import Graph
from .dsatur import dsatur
from .improved_dsatur import improved_dsatur


class _Timeout(Exception):
    pass


@dataclass
class ExactResult:
    colors: list[int]
    chi: int                 # best number of colours found (= chi if optimal)
    lower_bound: int
    optimal: bool
    nodes: int = 0
    time: float = 0.0
    info: dict = field(default_factory=dict)


def exact_coloring(G: Graph, time_limit: float = 30.0, exact_clique_limit: int = 120) -> ExactResult:
    t0 = perf_counter()
    n = G.n
    adj = G.adj
    if n == 0:
        return ExactResult([], 0, 0, True)

    # upper bound
    best_colors = dsatur(G)
    alt = improved_dsatur(G)
    if num_colors(alt) < num_colors(best_colors):
        best_colors = alt
    best_k = num_colors(best_colors)

    # lower bound
    clique = max_clique(G) if n <= exact_clique_limit else greedy_clique(G)
    lb = max(len(clique), 1)
    if best_k == lb:
        return ExactResult(best_colors, best_k, lb, True, 0, perf_counter() - t0)

    colors = [UNCOLORED] * n
    cnt = [[0] * best_k for _ in range(n)]  # cnt[v][c] = #neighbours of v with colour c
    sat = [0] * n
    udeg = [len(a) for a in adj]

    def assign(v: int, c: int) -> None:
        colors[v] = c
        for u in adj[v]:
            row = cnt[u]
            if row[c] == 0:
                sat[u] += 1
            row[c] += 1
            udeg[u] -= 1

    def unassign(v: int, c: int) -> None:
        colors[v] = UNCOLORED
        for u in adj[v]:
            row = cnt[u]
            row[c] -= 1
            if row[c] == 0:
                sat[u] -= 1
            udeg[u] += 1

    for i, v in enumerate(clique):
        assign(v, i)
    state = {"best_k": best_k, "best": best_colors, "nodes": 0}
    deadline = t0 + time_limit

    def select() -> int:
        bv, bs, bd = -1, -1, -1
        for v in range(n):
            if colors[v] == UNCOLORED:
                s = sat[v]
                if s > bs or (s == bs and udeg[v] > bd):
                    bv, bs, bd = v, s, udeg[v]
        return bv

    def search(ncolored: int, k: int) -> bool:
        """Returns True when an optimal (== lb) colouring has been found."""
        state["nodes"] += 1
        if (state["nodes"] & 1023) == 0 and perf_counter() > deadline:
            raise _Timeout
        if k >= state["best_k"]:
            return False
        if ncolored == n:
            state["best_k"] = k
            state["best"] = colors[:]
            return k == lb
        v = select()
        row = cnt[v]
        for c in range(k):
            if row[c] == 0:
                assign(v, c)
                done = search(ncolored + 1, k)
                unassign(v, c)
                if done:
                    return True
                if k >= state["best_k"]:
                    return False
        if k + 1 < state["best_k"]:
            assign(v, k)
            done = search(ncolored + 1, k + 1)
            unassign(v, k)
            if done:
                return True
        return False

    optimal = True
    try:
        search(len(clique), len(clique))
    except _Timeout:
        optimal = state["best_k"] == lb
    return ExactResult(state["best"], state["best_k"], lb, optimal, state["nodes"], perf_counter() - t0)


def chromatic_number(G: Graph, time_limit: float = 30.0) -> int | None:
    """chi(G), or ``None`` if it could not be proven within ``time_limit``."""
    r = exact_coloring(G, time_limit)
    return r.chi if r.optimal else None
