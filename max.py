from collections import deque, defaultdict
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self):
        # graph[u][v] = remaining capacity from u to v
        self.graph = defaultdict(dict)

        # flow[u][v] = current flow from u to v (used for tracking actual flow)
        self.flow = defaultdict(lambda: defaultdict(int))

    def add_edge(self, u, v, capacity):
        """
        Adds a directed edge from u to v with the given capacity.
        Also ensures that reverse edge (v to u) is initialized with 0 capacity for residual graph.
        """
        if v not in self.graph[u]:
            self.graph[u][v] = 0
        if u not in self.graph[v]:
            self.graph[v][u] = 0

        # Allow parallel edges by adding to existing capacity
        self.graph[u][v] += capacity

    def bfs(self, source, sink, parent):
        """
        Breadth-First Search to find an augmenting path from source to sink
        in the residual graph. Fills parent map with the path.
        Returns True if a path is found, otherwise False.
        """
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                # Only consider edges with available capacity and not yet visited
                if v not in visited and self.graph[u][v] > 0:
                    parent[v] = u
                    visited.add(v)
                    if v == sink:
                        return True  # Path found
                    queue.append(v)

        return False  # No augmenting path found

    def ford_fulkerson(self, source, sink):
        """
        Runs the Ford-Fulkerson algorithm to compute the maximum flow
        from source to sink using BFS to find augmenting paths.
        """
        parent = {}
        max_flow = 0  # Initialize the total flow to zero

        # Loop until no more augmenting path is found
        while self.bfs(source, sink, parent):
            # Step 1: Find the minimum capacity (bottleneck) along the path
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Step 2: Update the residual capacities and track the flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow  # Reduce forward edge capacity
                self.graph[v][u] += path_flow  # Increase reverse edge capacity (residual)
                self.flow[u][v] += path_flow   # Track actual flow in original direction
                self.flow[v][u] -= path_flow   # Reverse flow (helps cancel out excess)
                v = parent[v]

            max_flow += path_flow  # Add bottleneck flow to the total

        return max_flow
# Create our graph object
g = Graph()
G = nx.DiGraph()  # For visualization

# List of edges in format: (from, to, capacity)
edges = [
    (0, 1, 14),
    (0, 2, 8),
    (1, 2, 10),
    (1, 3, 12),
    (2, 1, 4),
    (2, 4, 14),
    (3, 2, 9),
    (3, 5, 20),
    (4, 3, 7),
    (4, 5, 4)
]

# Add edges to both our graph implementation and NetworkX graph
for u, v, capacity in edges:
    g.add_edge(u, v, capacity)
    G.add_edge(u, v, capacity=capacity)  # Needed for visualization

# Define source and sink
source, sink = 0, 5

# Compute maximum flow
max_flow = g.ford_fulkerson(source, sink)
print("The maximum possible flow is", max_flow)
# Draw the graph with actual flow/capacity on each edge
pos = nx.spring_layout(G, seed=42)
edge_labels = {}

# Add "flow/capacity" labels to each edge
for u, v in G.edges():
    flow = g.flow[u][v]
    capacity = G[u][v]['capacity']
    edge_labels[(u, v)] = f"{flow}/{capacity}"

# Plotting
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Flow Network (Flow/Capacity)")
plt.axis('off')
plt.show()
