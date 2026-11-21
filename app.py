"""Simple Web Backend & Frontend Server for Greedy Graph Coloring Algorithms.

Uses only Python's standard library (http.server) and the existing gcol package.
Run with:
    python app.py
Then open http://127.0.0.1:8000 in a web browser.
"""

from __future__ import annotations

import json
import math
import os
import time
import tracemalloc
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

import networkx as nx

from gcol.algorithms import (
    dsatur,
    exact_coloring,
    greedy_coloring,
    improved_dsatur,
    welsh_powell_first_fit,
)
from gcol.bounds import greedy_clique
from gcol.coloring import is_proper, make_rank, num_colors
from gcol.dimacs import load_dimacs

KNOWN_CHROMATIC = {
    "myciel3": 4,
    "myciel5": 6,
    "queen5_5": 5,
    "queen8_8": 9,
    "jean": 10,
    "anna": 11,
    "huck": 11,
    "le450_15a": 15,
}
from gcol.generators import (
    barabasi_albert,
    complete_graph,
    crown_graph,
    cycle_graph,
    erdos_renyi,
    random_geometric,
)
from gcol.graph import Graph

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
WEB_DIR = ROOT / "web"

ALGORITHMS = [
    ("Basic Greedy", greedy_coloring),
    ("Welsh-Powell", welsh_powell_first_fit),
    ("DSATUR", dsatur),
    ("Improved DSATUR", improved_dsatur),
]


def build_graph(params: dict) -> tuple[Graph, int | None]:
    """Build or load a Graph based on frontend request parameters."""
    gtype = params.get("graph_type", "erdos_renyi")
    n = max(3, min(int(params.get("n", 25)), 500))
    seed = int(params.get("seed", 0))
    known_chi: int | None = None

    if gtype == "dimacs":
        inst = params.get("dimacs_name", "myciel3")
        col_path = DATA_DIR / f"{inst}.col"
        if not col_path.exists():
            col_path = next(DATA_DIR.glob("*.col"))
        G = load_dimacs(col_path)
        known_chi = KNOWN_CHROMATIC.get(G.name)
    elif gtype == "erdos_renyi":
        p = max(0.02, min(float(params.get("param", 0.25)), 0.95))
        G = erdos_renyi(n, p, seed=seed)
    elif gtype == "barabasi_albert":
        m = max(1, min(int(float(params.get("param", 2))), n - 1))
        G = barabasi_albert(n, m, seed=seed)
    elif gtype == "random_geometric":
        r = max(0.05, min(float(params.get("param", 0.25)), 0.9))
        G = random_geometric(n, r, seed=seed)
    elif gtype == "cycle":
        G = cycle_graph(n)
        known_chi = 2 if n % 2 == 0 else 3
    elif gtype == "complete":
        n = min(n, 60)
        G = complete_graph(n)
        known_chi = n
    elif gtype == "crown":
        half = max(3, min(n // 2, 100))
        G = crown_graph(half)
        known_chi = 2
    else:
        G = erdos_renyi(n, 0.25, seed=seed)

    if known_chi is None and G.n <= 35:
        ex = exact_coloring(G, time_limit=1.0)
        if ex.optimal:
            known_chi = ex.chi

    return G, known_chi


def compute_layout(G: Graph) -> list[dict[str, float]]:
    """Compute 2D coordinates in [0.08, 0.92] for frontend canvas visualization."""
    if G.n > 150:
        return []
    nx_g = nx.Graph()
    nx_g.add_nodes_from(range(G.n))
    nx_g.add_edges_from(G.edges())
    if G.name.startswith("Cycle") or G.name.startswith("Complete") or G.name.startswith("Crown"):
        pos = nx.circular_layout(nx_g)
    else:
        pos = nx.spring_layout(nx_g, seed=42, iterations=40)

    xs = [float(pos[i][0]) for i in range(G.n)]
    ys = [float(pos[i][1]) for i in range(G.n)]
    min_x, max_x = min(xs, default=0.0), max(xs, default=1.0)
    min_y, max_y = min(ys, default=0.0), max(ys, default=1.0)
    span_x = (max_x - min_x) or 1.0
    span_y = (max_y - min_y) or 1.0

    coords = []
    for i in range(G.n):
        nx_val = 0.08 + 0.84 * ((xs[i] - min_x) / span_x)
        ny_val = 0.08 + 0.84 * ((ys[i] - min_y) / span_y)
        coords.append({"id": i, "x": round(nx_val, 4), "y": round(ny_val, 4), "degree": G.degree(i)})
    return coords


def run_comparison(params: dict) -> dict:
    """Run all 4 greedy algorithms on the requested graph and return JSON metrics + coloring."""
    G, known_chi = build_graph(params)
    seed = int(params.get("seed", 0))
    omega_lb = len(greedy_clique(G, make_rank(G.n, seed)))

    results = []
    colorings = {}
    base_k = None

    for name, fn in ALGORITHMS:
        tracemalloc.start()
        t0 = time.perf_counter()
        colors = fn(G, seed=seed)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        k = num_colors(colors)
        proper = is_proper(G, colors)
        if base_k is None:
            base_k = k
        gain_pct = ((base_k - k) / base_k * 100.0) if base_k else 0.0
        approx_ratio = (k / known_chi) if known_chi else (k / omega_lb if omega_lb else 1.0)

        results.append({
            "algorithm": name,
            "colors": k,
            "time_ms": round(elapsed_ms, 3),
            "memory_kb": round(peak_bytes / 1024.0, 2),
            "proper": proper,
            "approx_ratio": round(approx_ratio, 3),
            "gain_pct": round(gain_pct, 2),
        })
        colorings[name] = colors

    nodes = compute_layout(G)
    edges = [[u, v] for u, v in G.edges()] if G.n <= 150 else []

    return {
        "graph": {
            "name": G.name,
            "n": G.n,
            "m": G.m,
            "density": round(G.density(), 4),
            "max_degree": G.max_degree(),
            "avg_degree": round((2.0 * G.m / G.n) if G.n > 0 else 0.0, 2),
            "omega_lb": omega_lb,
            "known_chi": known_chi,
        },
        "results": results,
        "colorings": colorings if G.n <= 150 else {},
        "nodes": nodes,
        "edges": edges,
    }


class ColoringRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler serving the web UI and JSON API endpoints."""

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            html_path = WEB_DIR / "index.html"
            content = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif parsed.path == "/api/datasets":
            dimacs_files = sorted(p.stem for p in DATA_DIR.glob("*.col"))
            self._send_json({"dimacs": dimacs_files})
        else:
            self.send_error(404, "Not Found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/color":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            params = json.loads(raw)
            data = run_comparison(params)
            self._send_json(data)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, fmt: str, *args) -> None:
        return


def load_env_file() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())


def main(host: str | None = None, port: int | None = None) -> None:
    load_env_file()
    host = host or os.environ.get("APP_HOST", "127.0.0.1")
    port = port or int(os.environ.get("APP_PORT", "8000"))
    server = HTTPServer((host, port), ColoringRequestHandler)
    print(f"Graph Coloring Web Server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
