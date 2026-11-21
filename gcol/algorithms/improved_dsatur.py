"""Algorithm 4 - Improved DSATUR.

Standard DSATUR plus three enhancements, each of which can be switched off
independently for the ablation study:

1. **Enhanced tie-breaking** (``use_tiebreak``)
   Standard DSATUR picks max saturation, then max uncoloured degree, then an
   arbitrary vertex. Here the remaining ties are resolved with *Sewell's
   rule* (Sewell 1996; used in the PASS algorithm of San Segundo 2012): pick
   the tied vertex v maximising

       sum over uncoloured neighbours u of |A(v) & A(u)|

   where A(x) is the set of colours (among those already used) still
   available to x. Colouring such a vertex removes the most options from its
   neighbourhood, i.e. it is the most *constraining* choice, which tends to
   expose conflicts early.

   Note: the synopsis listed "smallest available colour set" as a tertiary
   criterion. Vertices tied on saturation always have available sets of the
   same size, so that criterion can never separate them; Sewell's rule is the
   well-defined criterion from the literature that we implement instead.

2. **Clique pre-colouring** (``use_clique``)
   A large clique Q is found with a greedy heuristic and its vertices are
   fixed to colours 0..|Q|-1 before DSATUR starts. |Q| is a lower bound on
   chi(G), so this costs nothing in quality and seeds DSATUR with the most
   constrained part of the graph.

3. **Graph reduction** (``use_reduction``), inspired by the preprocessing of
   Schidler & Szeider (2023) and reduction-based colouring (RECOL):

   * *Low-degree removal*: a vertex with current degree < LB (= |Q|) can
     always be coloured afterwards with one of the first LB colours, so it
     is removed. This is applied repeatedly (it is the "LB-core" peeling).
   * *Domination removal*: if u and v are **non-adjacent** and
     N(u) is a subset of N(v), then u can always take v's colour, so u is
     removed. (Adjacent vertices can never share a colour, which is why the
     rule uses open neighbourhoods and requires non-adjacency.)

   Removed vertices are re-inserted in reverse order of removal with
   first-fit. Correctness: when u is re-inserted, exactly the vertices that
   were present when u was removed are coloured. A low-degree vertex sees
   < LB coloured neighbours, so it gets a colour < LB; a dominated vertex's
   coloured neighbours all neighbour its dominator v and so avoid c(v), hence
   first-fit returns a colour <= c(v). Therefore reductions never add colours
   beyond max(k, LB), where k is the number of colours used on the reduced graph.

Complexity
----------
clique heuristic      O(s * omega * |cand| * min-intersection), s = number of starts
low-degree peeling    O(n + m)
domination pass       O(sum_u deg(pivot(u)) * deg(u)) <= O(m * Delta), capped by a work budget
DSATUR + Sewell rule  O((n + m) log n + T), T = cost of scoring tied vertices
                      (at most ``max_ties`` vertices per step, each O(deg * k))
Overall               O((n + m) log n + R), R = preprocessing cost.  Space O(n + m).
"""

from __future__ import annotations

from time import perf_counter

from ..bounds import greedy_clique
from ..coloring import UNCOLORED, first_fit, make_rank
from ..graph import Graph
from .dsatur import dsatur_engine


def reduce_graph(G: Graph, lb: int, rank: list[int], *, use_domination: bool = True,
                 domination_budget: int = 2_000_000, max_rounds: int = 10) -> tuple[list[bool], list[int], dict]:
    """Apply low-degree and domination reductions until no rule fires.

    Returns ``(alive, stack, stats)`` where ``alive[v]`` says whether v is in
    the reduced graph and ``stack`` lists removed vertices in removal order.
    """
    n = G.n
    adj = G.adj
    alive = [True] * n
    deg = [len(a) for a in adj]
    stack: list[int] = []
    stats = {"removed_low_degree": 0, "removed_dominated": 0,
             "domination_work": 0, "domination_skipped": False, "rounds": 0}

    queue = [v for v in range(n) if deg[v] < lb]

    def peel() -> None:
        while queue:
            v = queue.pop()
            if not alive[v]:
                continue
            alive[v] = False
            stack.append(v)
            stats["removed_low_degree"] += 1
            for w in adj[v]:
                if alive[w]:
                    deg[w] -= 1
                    if deg[w] == lb - 1:  # just crossed the threshold
                        queue.append(w)

    order = sorted(range(n), key=rank.__getitem__)
    work = 0
    for _ in range(max_rounds):
        stats["rounds"] += 1
        peel()
        if not use_domination or stats["domination_skipped"]:
            break
        removed_this_round = 0
        for u in order:
            if not alive[u]:
                continue
            nbrs = [w for w in adj[u] if alive[w]]
            if not nbrs:
                continue
            # A dominator v must be adjacent to every neighbour of u, in
            # particular to the neighbour of minimum degree ("pivot").
            pivot = min(nbrs, key=deg.__getitem__)
            work += deg[pivot]
            if work > domination_budget:
                stats["domination_skipped"] = True
                break
            du = deg[u]
            adj_u = adj[u]
            for v in adj[pivot]:
                if v == u or not alive[v] or deg[v] < du or v in adj_u:
                    continue
                if adj[v].issuperset(nbrs):
                    alive[u] = False
                    stack.append(u)
                    stats["removed_dominated"] += 1
                    removed_this_round += 1
                    for w in nbrs:
                        deg[w] -= 1
                        if deg[w] == lb - 1:
                            queue.append(w)
                    break
        stats["domination_work"] = work
        if removed_this_round == 0 and not queue:
            break
    peel()
    return alive, stack, stats


def improved_dsatur(G: Graph, seed: int | None = None, *, use_tiebreak: bool = True,
                    use_clique: bool = True, use_reduction: bool = True,
                    max_ties: int = 8, domination_budget: int = 2_000_000,
                    info: dict | None = None) -> list[int]:
    """Improved DSATUR (see module docstring). Returns a proper colouring.

    If ``info`` is a dict it receives diagnostics: lower bound, reduced graph
    size, number of removed vertices per rule, tie-break counters and the time
    spent in each phase.
    """
    t_start = perf_counter()
    n = G.n
    rank = make_rank(n, seed)
    diag: dict = {"lb": 0, "n_reduced": n, "removed_low_degree": 0, "removed_dominated": 0}

    # 1) clique -> lower bound
    clique: list[int] = []
    if (use_clique or use_reduction) and n > 0:
        clique = greedy_clique(G, rank)
    lb = len(clique)
    diag["lb"] = lb
    t_clique = perf_counter()

    # 2) reductions
    stack: list[int] = []
    if use_reduction and n > 0:
        alive, stack, rstats = reduce_graph(G, lb, rank, domination_budget=domination_budget)
        diag.update(rstats)
        kept = [v for v in range(n) if alive[v]]
    else:
        kept = list(range(n))
    H, mapping = G.induced_subgraph(kept)
    diag["n_reduced"] = H.n
    diag["m_reduced"] = H.m
    t_reduce = perf_counter()

    # 3) clique pre-colouring on the reduced graph
    rank_h = [rank[old] for old in mapping]
    initial: dict[int, int] = {}
    if use_clique and H.n > 0:
        index = {old: new for new, old in enumerate(mapping)}
        if clique and all(v in index for v in clique):
            hq = [index[v] for v in clique]
        else:
            hq = greedy_clique(H, rank_h)
        hq.sort(key=rank_h.__getitem__)
        initial = {v: i for i, v in enumerate(hq)}
        diag["precolored"] = len(initial)

    # 4) DSATUR on the reduced graph
    tstats: dict = {}
    hcolors = dsatur_engine(H, rank_h, initial=initial, sewell_tiebreak=use_tiebreak,
                            max_ties=max_ties, stats=tstats)
    diag.update(tstats)
    t_color = perf_counter()

    # 5) map back and re-insert removed vertices (reverse removal order)
    colors = [UNCOLORED] * n
    for new, old in enumerate(mapping):
        colors[old] = hcolors[new]
    adj = G.adj
    for v in reversed(stack):
        colors[v] = first_fit(adj[v], colors)
    t_end = perf_counter()

    diag["k_reduced"] = len(set(hcolors))
    diag["time_clique"] = t_clique - t_start
    diag["time_reduce"] = t_reduce - t_clique
    diag["time_color"] = t_color - t_reduce
    diag["time_reinsert"] = t_end - t_color
    if info is not None:
        info.update(diag)
    return colors
