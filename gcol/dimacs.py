"""Parser for DIMACS graph formats (.col)."""

from __future__ import annotations

import os

from .graph import Graph


def load_dimacs(filepath: str | os.PathLike) -> Graph:
    """Load a graph from a DIMACS .col file.
    
    Vertices are 1-indexed in the file and mapped to 0..n-1 in the Graph.
    """
    n, m = 0, 0
    edges: list[tuple[int, int]] = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            
            parts = line.split()
            if parts[0] == "p":
                # p edge n m
                n = int(parts[2])
                m = int(parts[3])
            elif parts[0] == "e":
                # e u v (1-indexed)
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                edges.append((u, v))
                
    name = os.path.basename(os.fspath(filepath))
    if name.endswith(".col"):
        name = name[:-4]
        
    return Graph(n, edges, name=name)
