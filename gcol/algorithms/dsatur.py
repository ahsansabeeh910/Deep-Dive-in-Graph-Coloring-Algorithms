"""Algorithm 3 - DSATUR (Brelaz, 1979).

At every step DSATUR colours the uncoloured vertex with the largest
*saturation degree* - the number of distinct colours already present in its
neighbourhood - and gives it the smallest feasible colour. Ties are broken by
the largest degree in the subgraph induced by the uncoloured vertices, and
any remaining ties by input order (``rank``).

Two implementations are provided:

``dsatur``        Priority queue (binary heap) with lazy deletion.
                  Time O((n + m) log n), space O(n + m).
``dsatur_naive``  Linear scan for the next vertex at every step.
                  Time O(n^2 + m), space O(n + m).

Both produce *identical* colourings (checked in the tests), so the difference
between them is purely one of running time; the complexity experiment
measures it.

Heap invariant (why lazy deletion is correct)
---------------------------------------------
Each heap entry is ``(-sat, -udeg, rank, v)``. Saturation only *increases*
and the uncoloured degree only *decreases* while the algorithm runs.

* When ``sat(v)`` grows, a new entry is pushed; the old one now carries a
  stale ``sat`` and is discarded when popped.
* When only ``udeg(v)`` shrinks nothing is pushed. The existing entry then
  *over-estimates* v's priority, so it is popped no later than it should be;
  at that moment it is re-pushed with the correct key.

Hence every uncoloured vertex always has an entry whose key is at least as
good as its true key, and the first *valid* entry popped is a true maximum.
Each edge causes at most one push, so there are O(n + m) heap operations.
"""

from __future__ import annotations

from heapq import heapify, heappop, heappush
from typing import Mapping

from ..coloring import UNCOLORED, make_rank
from ..graph import Graph


def dsatur_engine(
    G: Graph,
    rank: list[int],
    *,
    initial: Mapping[int, int] | None = None,
    sewell_tiebreak: bool = False,
    max_ties: int = 8,
    trace: list | None = None,
    stats: dict | None = None,
) -> list[int]:
    """Heap-based DSATUR shared by :func:`dsatur` and Improved DSATUR.

    Parameters
    ----------
    rank:
        Final tie-breaker (smaller rank wins).
    initial:
        Optional pre-colouring ``{vertex: colour}`` applied before the main
        loop (Improved DSATUR uses it to fix a clique to colours 0..q-1).
    sewell_tiebreak:
        If True, vertices tied on (saturation, uncoloured degree) are
        compared with Sewell's rule before falling back to ``rank``
        (Improvement 1). At most ``max_ties`` tied vertices are examined.
    trace:
        If a list is given, one tuple ``(v, sat, udeg, colour)`` is appended
        per vertex in the order it is coloured (used by the demo).
    stats:
        If a dict is given, counters about tie-breaking are written to it.
    """
    n = G.n
    adj = G.adj
    colors = [UNCOLORED] * n
    nbr_colors: list[set[int]] = [set() for _ in range(n)]
    udeg = [len(a) for a in adj]
    k = 0  # number of colours used so far
    ties_seen = 0
    ties_changed = 0

    heap: list[tuple[int, int, int, int]] = []

    def assign(v: int, c: int, push: bool) -> None:
        colors[v] = c
        for u in adj[v]:
            if colors[u] == UNCOLORED:
                udeg[u] -= 1
                ncu = nbr_colors[u]
                if c not in ncu:
                    ncu.add(c)
                    if push:
                        heappush(heap, (-len(ncu), -udeg[u], rank[u], u))

    remaining = n
    if initial:
        for v, c in initial.items():
            if colors[v] != UNCOLORED:
                raise ValueError(f"vertex {v} pre-coloured twice")
            if c in nbr_colors[v]:
                raise ValueError(f"pre-colouring is not proper at vertex {v}")
            assign(v, c, push=False)
            if c >= k:
                k = c + 1
            remaining -= 1

    heap = [(-len(nbr_colors[v]), -udeg[v], rank[v], v) for v in range(n) if colors[v] == UNCOLORED]
    heapify(heap)

    def pop_valid() -> int:
        while heap:
            negsat, negdeg, r, v = heappop(heap)
            if colors[v] != UNCOLORED or -negsat != len(nbr_colors[v]):
                continue  # already coloured, or superseded by a newer entry
            if -negdeg != udeg[v]:
                heappush(heap, (negsat, -udeg[v], r, v))  # refresh stale degree
                continue
            return v
        return -1

    def sewell_score(v: int) -> int:
        # Sum over uncoloured neighbours u of |available(v) & available(u)|,
        # restricted to the k colours already in use.
        nv = nbr_colors[v]
        avail = {c for c in range(k) if c not in nv}
        la = len(avail)
        if la == 0:
            return 0
        score = 0
        for u in adj[v]:
            if colors[u] == UNCOLORED:
                score += la - len(nbr_colors[u] & avail)
        return score

    while remaining:
        v = pop_valid()
        if sewell_tiebreak:
            key = (len(nbr_colors[v]), udeg[v])
            tied = [v]
            while len(tied) < max_ties:
                w = pop_valid()
                if w == -1:
                    break
                if (len(nbr_colors[w]), udeg[w]) == key:
                    tied.append(w)
                else:
                    heappush(heap, (-len(nbr_colors[w]), -udeg[w], rank[w], w))
                    break
            if len(tied) > 1:
                ties_seen += 1
                best = max(tied, key=lambda w: (sewell_score(w), -rank[w]))
                if best != v:
                    ties_changed += 1
                for w in tied:
                    if w != best:
                        heappush(heap, (-len(nbr_colors[w]), -udeg[w], rank[w], w))
                v = best

        nv = nbr_colors[v]
        c = 0
        while c in nv:
            c += 1
        if trace is not None:
            trace.append((v, len(nv), udeg[v], c))
        assign(v, c, push=True)
        if c >= k:
            k = c + 1
        remaining -= 1

    if stats is not None:
        stats["ties_examined"] = ties_seen
        stats["ties_changed"] = ties_changed
    return colors


def dsatur(G: Graph, seed: int | None = None, trace: list | None = None) -> list[int]:
    """Standard DSATUR, heap implementation, O((n + m) log n)."""
    return dsatur_engine(G, make_rank(G.n, seed), trace=trace)


def dsatur_naive(G: Graph, seed: int | None = None) -> list[int]:
    """Standard DSATUR with a linear scan per step, O(n^2 + m).

    Uses exactly the same selection rule as :func:`dsatur`.
    """
    n = G.n
    adj = G.adj
    rank = make_rank(n, seed)
    colors = [UNCOLORED] * n
    nbr_colors: list[set[int]] = [set() for _ in range(n)]
    udeg = [len(a) for a in adj]
    uncolored = list(range(n))

    for _ in range(n):
        best_i = 0
        bv = uncolored[0]
        best_key = (len(nbr_colors[bv]), udeg[bv], -rank[bv])
        for i in range(1, len(uncolored)):
            w = uncolored[i]
            key = (len(nbr_colors[w]), udeg[w], -rank[w])
            if key > best_key:
                best_key = key
                best_i = i
        v = uncolored[best_i]
        uncolored[best_i] = uncolored[-1]  # O(1) removal
        uncolored.pop()

        nv = nbr_colors[v]
        c = 0
        while c in nv:
            c += 1
        colors[v] = c
        for u in adj[v]:
            if colors[u] == UNCOLORED:
                udeg[u] -= 1
                nbr_colors[u].add(c)
    return colors
