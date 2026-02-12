#!/usr/bin/env python3
"""Evaluator for Task 10: Graph Algorithms"""
import sys
import os
import importlib.util

TASK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', '..', 'tasks', 'task_10_graph_algorithms')


def load_solution():
    path = os.path.join(TASK_DIR, 'graph.py')
    if not os.path.exists(path):
        print("[FAIL] graph.py not found")
        sys.exit(1)
    spec = importlib.util.spec_from_file_location("graph", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


passed = failed = 0


def check(name, fn, validator):
    global passed, failed
    try:
        got = fn()
        ok, msg = validator(got)
        if ok:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}: {msg} (got {got!r})")
            failed += 1
    except NotImplementedError:
        print(f"[FAIL] {name}: not implemented")
        failed += 1
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")
        failed += 1


def fresh_graph(directed=False):
    """Load a fresh module and return a new Graph instance."""
    spec = importlib.util.spec_from_file_location(
        "graph_fresh", os.path.join(TASK_DIR, 'graph.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Graph(directed=directed)


def build_undirected():
    """Undirected graph: A-B-C, A-D-E-B"""
    g = fresh_graph(directed=False)
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('A', 'D')
    g.add_edge('D', 'E')
    g.add_edge('E', 'B')
    return g


def build_directed():
    """Directed graph: A->B->C, A->D, D->C"""
    g = fresh_graph(directed=True)
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('A', 'D')
    g.add_edge('D', 'C')
    return g


def build_weighted():
    """Weighted directed graph for Dijkstra.
       A->B(1), A->C(4), B->C(2), B->D(5), C->D(1)
       Shortest paths from A:  A=0, B=1, C=3, D=4
    """
    g = fresh_graph(directed=True)
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'C', 2)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 1)
    return g


def main():
    sol = load_solution()

    # ── add_edge / basic structure ────────────────────────────────────────────
    check(
        "add_edge creates vertices",
        lambda: (
            lambda g: ('A' in g.adjacency_list and 'B' in g.adjacency_list)
        )(build_directed()),
        lambda v: (v is True, "vertices not created")
    )

    check(
        "undirected add_edge creates both directions",
        lambda: (
            lambda g: (
                any(n == 'B' for n, _ in g.adjacency_list.get('A', []))
                and any(n == 'A' for n, _ in g.adjacency_list.get('B', []))
            )
        )(build_undirected()),
        lambda v: (v is True, "reverse edge missing in undirected graph")
    )

    # ── BFS ──────────────────────────────────────────────────────────────────
    check(
        "bfs visits all reachable nodes",
        lambda: set(build_undirected().bfs('A')),
        lambda v: (v == {'A', 'B', 'C', 'D', 'E'}, f"expected all 5 nodes, got {v}")
    )
    check(
        "bfs starts with start node",
        lambda: build_undirected().bfs('A')[0],
        lambda v: (v == 'A', f"first node should be A, got {v}")
    )
    check(
        "bfs level order (neighbours before their children)",
        lambda: (
            lambda order: (
                order.index('B') < order.index('C')
                and order.index('D') < order.index('E')
            )
        )(build_undirected().bfs('A')),
        lambda v: (v is True, "BFS level order violated")
    )

    # ── DFS ──────────────────────────────────────────────────────────────────
    check(
        "dfs visits all reachable nodes",
        lambda: set(build_undirected().dfs('A')),
        lambda v: (v == {'A', 'B', 'C', 'D', 'E'}, f"expected all 5 nodes, got {v}")
    )
    check(
        "dfs starts with start node",
        lambda: build_undirected().dfs('A')[0],
        lambda v: (v == 'A', f"first node should be A")
    )

    # ── shortest_path ─────────────────────────────────────────────────────────
    check(
        "shortest_path direct neighbour",
        lambda: build_undirected().shortest_path('A', 'B'),
        lambda v: (v == ['A', 'B'], f"expected ['A','B'], got {v}")
    )
    check(
        "shortest_path A->C length is 3",
        lambda: len(build_undirected().shortest_path('A', 'C') or []),
        lambda v: (v == 3, f"expected path length 3 (A,B,C), got {v}")
    )
    check(
        "shortest_path same node",
        lambda: build_undirected().shortest_path('A', 'A'),
        lambda v: (v == ['A'], f"expected ['A'], got {v}")
    )
    check(
        "shortest_path unreachable returns None",
        lambda: build_directed().shortest_path('C', 'A'),
        lambda v: (v is None, f"expected None for unreachable node, got {v}")
    )

    # ── dijkstra ──────────────────────────────────────────────────────────────
    check(
        "dijkstra distance to self is 0",
        lambda: build_weighted().dijkstra('A').get('A'),
        lambda v: (v == 0, f"expected 0, got {v}")
    )
    check(
        "dijkstra distance A->B is 1",
        lambda: build_weighted().dijkstra('A').get('B'),
        lambda v: (v == 1, f"expected 1, got {v}")
    )
    check(
        "dijkstra distance A->C is 3 (via B)",
        lambda: build_weighted().dijkstra('A').get('C'),
        lambda v: (v == 3, f"expected 3, got {v}")
    )
    check(
        "dijkstra distance A->D is 4 (via B->C)",
        lambda: build_weighted().dijkstra('A').get('D'),
        lambda v: (v == 4, f"expected 4, got {v}")
    )

    # ── has_cycle ─────────────────────────────────────────────────────────────
    check(
        "has_cycle detects cycle in undirected graph",
        lambda: build_undirected().has_cycle(),
        lambda v: (v is True, "should have a cycle (A-B-E-D-A)")
    )

    def build_linear_path():
        g = fresh_graph(directed=False)
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        return g

    check(
        "has_cycle no cycle in linear path A-B-C",
        lambda: build_linear_path().has_cycle(),
        lambda v: (v is False, "linear path A-B-C should have no cycle")
    )

    def build_directed_cycle():
        g = fresh_graph(directed=True)
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('C', 'A')
        return g

    check(
        "has_cycle detects cycle in directed graph A->B->C->A",
        lambda: build_directed_cycle().has_cycle(),
        lambda v: (v is True, "A->B->C->A should be a cycle")
    )

    print(f"\nResults: {passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
