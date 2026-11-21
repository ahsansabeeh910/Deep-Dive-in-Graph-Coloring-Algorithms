"""Lightweight undirected simple graph used by all coloring algorithms.

All algorithms in this project operate on :class:`Graph` rather than on a
NetworkX graph. Vertices are the integers ``0 .. n-1`` and adjacency is stored
as a list of Python ``set`` objects, which gives

* O(1) expected-time adjacency tests (``v in G.adj[u]``),
* O(deg(v)) neighbourhood iteration,
* O(n + m) memory.

Keeping the representation minimal means that the measured running times
reflect the algorithms themselves and not the overhead of a general-purpose
graph library.
"""

from __future__ import annotations

from typing import Iterable, Iterator, Sequence


class Graph:
    """Undirected simple graph on vertices ``0 .. n-1``.

    Self-loops are ignored and parallel edges are merged, so the stored graph
    is always simple.
    """

    __slots__ = ("n", "adj", "name")

    def __init__(self, n: int, edges: Iterable[tuple[int, int]] = (), name: str = "") -> None:
        if n < 0:
            raise ValueError("number of vertices must be non-negative")
        self.n: int = n
        self.adj: list[set[int]] = [set() for _ in range(n)]
        self.name: str = name
        for u, v in edges:
            self.add_edge(u, v)

    # ------------------------------------------------------------------ edits
    def add_edge(self, u: int, v: int) -> None:
        """Add the undirected edge ``{u, v}`` (self-loops are ignored)."""
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise ValueError(f"edge ({u}, {v}) out of range for n={self.n}")
        if u == v:
            return
        self.adj[u].add(v)
        self.adj[v].add(u)

    # ---------------------------------------------------------------- queries
    @property
    def m(self) -> int:
        """Number of edges."""
        return sum(len(a) for a in self.adj) // 2

    def degree(self, v: int) -> int:
        return len(self.adj[v])

    def degrees(self) -> list[int]:
        return [len(a) for a in self.adj]

    def max_degree(self) -> int:
        return max((len(a) for a in self.adj), default=0)

    def density(self) -> float:
        """Edge density 2m / (n(n-1)); 0 for graphs with fewer than 2 vertices."""
        if self.n < 2:
            return 0.0
        return 2.0 * self.m / (self.n * (self.n - 1))

    def has_edge(self, u: int, v: int) -> bool:
        return v in self.adj[u]

    def edges(self) -> Iterator[tuple[int, int]]:
        """Iterate over each edge exactly once as ``(u, v)`` with ``u < v``."""
        for u, nbrs in enumerate(self.adj):
            for v in nbrs:
                if u < v:
                    yield (u, v)

    # ------------------------------------------------------------ transforms
    def induced_subgraph(self, vertices: Sequence[int], name: str = "") -> tuple["Graph", list[int]]:
        """Return the subgraph induced by ``vertices`` relabelled to ``0..k-1``.

        Returns ``(H, mapping)`` where ``mapping[i]`` is the original label of
        vertex ``i`` of ``H``.
        """
        mapping = list(vertices)
        index = {old: new for new, old in enumerate(mapping)}
        H = Graph(len(mapping), name=name or f"{self.name}[sub]")
        for new, old in enumerate(mapping):
            H.adj[new] = {index[w] for w in self.adj[old] if w in index}
        return H, mapping

    def relabeled(self, perm: Sequence[int], name: str = "") -> "Graph":
        """Return a copy where vertex ``v`` becomes ``perm[v]``."""
        H = Graph(self.n, name=name or self.name)
        for v, nbrs in enumerate(self.adj):
            H.adj[perm[v]] = {perm[w] for w in nbrs}
        return H

    def copy(self) -> "Graph":
        H = Graph(self.n, name=self.name)
        H.adj = [set(a) for a in self.adj]
        return H

    # ----------------------------------------------------------- conversions
    @classmethod
    def from_networkx(cls, G, name: str = "") -> "Graph":
        """Build a :class:`Graph` from any NetworkX graph (labels are remapped)."""
        nodes = list(G.nodes())
        index = {v: i for i, v in enumerate(nodes)}
        H = cls(len(nodes), name=name or str(G.name or ""))
        for u, v in G.edges():
            H.add_edge(index[u], index[v])
        return H

    def to_networkx(self):
        import networkx as nx

        G = nx.Graph(name=self.name)
        G.add_nodes_from(range(self.n))
        G.add_edges_from(self.edges())
        return G

    @classmethod
    def from_edge_list(cls, n: int, edges: Iterable[tuple[int, int]], name: str = "") -> "Graph":
        return cls(n, edges, name=name)

    # ---------------------------------------------------------------- dunder
    def __len__(self) -> int:
        return self.n

    def __repr__(self) -> str:
        label = f" '{self.name}'" if self.name else ""
        return f"<Graph{label} n={self.n} m={self.m}>"
