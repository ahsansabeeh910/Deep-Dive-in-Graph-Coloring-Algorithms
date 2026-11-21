"""Helpers shared by all coloring algorithms: validation, first-fit, tie ranks."""

from __future__ import annotations

import random
from typing import Iterable, Sequence

from .graph import Graph

UNCOLORED = -1


def make_rank(n: int, seed: int | None) -> list[int]:
    """Return a tie-breaking rank for every vertex.

    ``rank[v]`` is the position of ``v`` in the *input order*. With
    ``seed=None`` the input order is the natural order ``0..n-1``; otherwise it
    is a uniformly random permutation drawn from ``random.Random(seed)``.

    Every algorithm breaks its final ties by this rank (smaller first), so a
    seed acts like presenting the same graph with a different vertex
    numbering. This is how repeated runs of otherwise deterministic algorithms
    are made statistically meaningful.
    """
    if seed is None:
        return list(range(n))
    perm = list(range(n))
    random.Random(seed).shuffle(perm)
    rank = [0] * n
    for position, v in enumerate(perm):
        rank[v] = position
    return rank


def input_order(n: int, seed: int | None) -> list[int]:
    """Vertices sorted by :func:`make_rank` (the input order for this seed)."""
    rank = make_rank(n, seed)
    order = [0] * n
    for v, r in enumerate(rank):
        order[r] = v
    return order


def first_fit(neighbours: Iterable[int], colors: Sequence[int]) -> int:
    """Smallest colour (>= 0) not used by any already-coloured neighbour."""
    used = {colors[u] for u in neighbours}
    c = 0
    while c in used:
        c += 1
    return c


def num_colors(colors: Sequence[int]) -> int:
    """Number of distinct colours used (ignores uncoloured vertices)."""
    return len({c for c in colors if c != UNCOLORED})


def find_conflict(G: Graph, colors: Sequence[int]) -> tuple[int, int] | None:
    """Return an edge whose endpoints share a colour / a vertex left uncoloured."""
    if len(colors) != G.n:
        raise ValueError(f"expected {G.n} colours, got {len(colors)}")
    for v in range(G.n):
        if colors[v] == UNCOLORED or colors[v] < 0:
            return (v, v)
    for u, v in G.edges():
        if colors[u] == colors[v]:
            return (u, v)
    return None


def is_proper(G: Graph, colors: Sequence[int]) -> bool:
    """True iff every vertex is coloured and no edge is monochromatic."""
    return find_conflict(G, colors) is None


def assert_proper(G: Graph, colors: Sequence[int]) -> None:
    conflict = find_conflict(G, colors)
    if conflict is not None:
        u, v = conflict
        if u == v:
            raise AssertionError(f"vertex {u} is uncoloured")
        raise AssertionError(f"edge ({u}, {v}) is monochromatic (colour {colors[u]})")


def color_classes(colors: Sequence[int]) -> dict[int, list[int]]:
    classes: dict[int, list[int]] = {}
    for v, c in enumerate(colors):
        classes.setdefault(c, []).append(v)
    return classes
