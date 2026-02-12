from collections import deque
from typing import Dict, List, Optional, Tuple
import heapq


class Graph:
    """Weighted graph (directed or undirected) with adjacency-list storage."""

    def __init__(self, directed: bool = False):
        """Initialize an empty graph.

        Args:
            directed: If True edges are one-directional; otherwise both directions
                      are added for each add_edge() call.
        """
        self.directed = directed
        # adjacency_list maps vertex → list of (neighbor, weight) tuples
        self.adjacency_list: Dict[object, List[Tuple[object, float]]] = {}

    def add_edge(self, u, v, weight: float = 1.0) -> None:
        """Add an edge u→v (and v→u for undirected graphs).

        Vertices are created automatically if they do not already exist.

        Args:
            u:      Source vertex.
            v:      Destination vertex.
            weight: Edge weight (default 1.0).
        """
        raise NotImplementedError

    def bfs(self, start) -> List:
        """Breadth-first traversal from start.

        Returns vertices in the order they are first visited.
        Neighbors are visited in insertion order.

        Args:
            start: The starting vertex.

        Returns:
            List of vertices in BFS order.
        """
        raise NotImplementedError

    def dfs(self, start) -> List:
        """Depth-first traversal from start.

        Returns vertices in the order they are first visited.
        Neighbors are visited in insertion order.

        Args:
            start: The starting vertex.

        Returns:
            List of vertices in DFS order.
        """
        raise NotImplementedError

    def shortest_path(self, start, end) -> Optional[List]:
        """Find the unweighted shortest path (fewest edges) from start to end.

        Args:
            start: Source vertex.
            end:   Destination vertex.

        Returns:
            List of vertices forming the path [start, ..., end],
            or None if no path exists.
        """
        raise NotImplementedError

    def dijkstra(self, start) -> Dict:
        """Compute minimum weighted distances from start to all vertices.

        Uses Dijkstra's algorithm (non-negative weights only).

        Args:
            start: The source vertex.

        Returns:
            Dict mapping vertex → minimum distance from start.
            Unreachable vertices map to float('inf').
        """
        raise NotImplementedError

    def has_cycle(self) -> bool:
        """Detect whether the graph contains at least one cycle.

        For undirected graphs: DFS-based approach ignoring the parent edge.
        For directed graphs: DFS coloring (white / grey / black).

        Returns:
            True if a cycle exists, False otherwise.
        """
        raise NotImplementedError
