"""Lower bounds on the chromatic number.

Every clique Q satisfies |Q| <= omega(G) <= chi(G), so any clique
found is a valid lower bound. Finding a maximum clique is NP-hard, so
:func:`greedy_clique` uses a multi-start greedy heuristic; :func:`max_clique`
is exact (via NetworkX) and only meant for small graphs.
"""

from __future__ import annotations

from .graph import Graph


def greedy_clique(G: Graph, rank: list[int] | None = None, max_starts: int = 20,
                  exact_choice_limit: int = 64) -> list[int]:
    """Multi-start greedy clique heuristic.

    Starting from each of the ``max_starts`` highest-degree vertices, keep a
    candidate set (common neighbours of the clique so far) and repeatedly add
    the candidate with the most neighbours inside the candidate set (when the
    set is small) or the highest degree (when it is large).

    Pruning: starts are visited by non-increasing degree, so we stop as soon
    as deg(s) + 1 cannot beat the best clique; a single run stops when the
    clique plus all remaining candidates cannot beat it.

    Time: O(max_starts * omega * |cand| * min-intersection) in the worst case,
    in practice a small fraction of the colouring time.
    """
    n = G.n
    if n == 0:
        return []
    adj = G.adj
    if rank is None:
        rank = list(range(n))
    deg = [len(a) for a in adj]
    order = sorted(range(n), key=lambda v: (-deg[v], rank[v]))
    best = [order[0]]

    for s in order[:max_starts]:
        if deg[s] + 1 <= len(best):
            break
        clique = [s]
        cand = set(adj[s])
        while cand:
            if len(clique) + len(cand) <= len(best):
                break
            if len(cand) <= exact_choice_limit:
                u = max(cand, key=lambda w: (len(adj[w] & cand), deg[w], -rank[w]))
            else:
                u = max(cand, key=lambda w: (deg[w], -rank[w]))
            clique.append(u)
            cand &= adj[u]
        if len(clique) > len(best):
            best = clique
    return best


def max_clique(G: Graph) -> list[int]:
    """Exact maximum clique (exponential time - small graphs only)."""
    import networkx as nx

    if G.n == 0:
        return []
    clique, _ = nx.max_weight_clique(G.to_networkx(), weight=None)
    return list(clique)


def is_clique(G: Graph, vertices: list[int]) -> bool:
    vs = list(vertices)
    return all(vs[j] in G.adj[vs[i]] for i in range(len(vs)) for j in range(i + 1, len(vs)))
