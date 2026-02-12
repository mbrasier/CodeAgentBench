# Task 10: Graph Algorithms (Python)

Implement a `Graph` class with BFS, DFS, shortest-path, Dijkstra, and cycle-detection in `graph.py`.

## What to implement

### `class Graph`

#### `__init__(self, directed: bool = False)`
Initialize an empty graph.  `directed=True` means edges are one-way.

#### `add_edge(u, v, weight: float = 1.0)`
Add an edge from `u` to `v` with the given weight.
For undirected graphs, also add the reverse edge `v → u`.
Create vertices automatically if they do not exist.

#### `bfs(start) -> list`
Return the list of vertices in **breadth-first** order starting from `start`.
Visit neighbors in the order they were added (i.e. insertion order of `add_edge` calls).

#### `dfs(start) -> list`
Return the list of vertices in **depth-first** order starting from `start` (iterative or recursive).
Visit neighbors in insertion order.

#### `shortest_path(start, end) -> list | None`
Return the shortest path (fewest edges, unweighted) from `start` to `end` as a list of vertices including both endpoints.
Return `None` if no path exists.

#### `dijkstra(start) -> dict`
Return a dict mapping every reachable vertex to its minimum weighted distance from `start`.
Unreachable vertices should map to `float('inf')`.

#### `has_cycle() -> bool`
Return `True` if the graph contains at least one cycle, `False` otherwise.

## File to modify

**`graph.py`** — implement the `Graph` class using an adjacency-list representation.
