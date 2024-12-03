import numpy as np
import math
from collections import defaultdict
import matplotlib.pyplot as plt

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False

# Compute Euclidean Distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt((p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

# Kruskal Algorithm using the UnionFind class
def kruskal_mst(distances):
    n = len(distances)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            edges.append((distances[i][j], i, j))

    edges.sort(key=lambda x: x[0])

    uf = UnionFind(n)
    mst = defaultdict(list)

    for weight, u, v in edges:
        if uf.union(u, v):  
            mst[u].append(v)
            mst[v].append(u)

    return mst

# DFS traversal of the MST to generate a path
def dfs(mst, start, visited, path):
    visited.add(start)
    path.append(start)
    for neighbor in mst[start]:
        if neighbor not in visited:
            dfs(mst, neighbor, visited, path)

# Shortcutting to remove repeated cities and form a valid TSP cycle
def shortcut(path):
    visited = set()
    new_path = []
    for city in path:
        if city not in visited:
            new_path.append(city)
            visited.add(city)
    return new_path

# TSP approximation using Kruskal's MST and DFS
def krustral_tsp(mst, start):
    visited = set()
    path = []
    
    # Perform DFS on MST
    dfs(mst, start, visited, path)
    
    # Apply shortcutting to avoid repeated cities
    tsp_path = shortcut(path)
    
    # Make the path circular (return to the start)
    tsp_path.append(tsp_path[0])
    
    return tsp_path

def read_points_from_file(filename):
    points = []
    with open(filename, "r") as file:
        for line in file:
            label, x, y = line.strip().split(',')
            points.append((label, float(x), float(y)))  
    return points


def euclidean_distance(point1, point2):
    return np.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

def plot_tsp_with_arrows(locations, tsp_path):
    labels, x_coords, y_coords = zip(*locations)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    total_distance = 0
    for i in range(len(tsp_path) - 1):
        u = tsp_path[i]
        v = tsp_path[i + 1]
        
        ax.plot([x_coords[u], x_coords[v]], [y_coords[u], y_coords[v]], 'g-', alpha=0.7)
        
        ax.annotate("",
                    xy=(x_coords[v], y_coords[v]),
                    xytext=(x_coords[u], y_coords[u]),
                    arrowprops=dict(arrowstyle="->", color='blue'))
        
        mid_x = (x_coords[u] + x_coords[v]) / 2
        mid_y = (y_coords[u] + y_coords[v]) / 2
        distance = euclidean_distance(locations[u], locations[v])
        total_distance += distance
        ax.text(mid_x, mid_y, f"{distance:.2f}", fontsize=10, ha='center', va='center')

    ax.scatter(x_coords, y_coords, color='red')
    
    for i, label in enumerate(labels):
        ax.text(x_coords[i] + 0.1, y_coords[i] + 0.1, label, fontsize=12)

    ax.set_title(f"TSP Path Visualization\nTotal Distance: {total_distance:.2f}")
    ax.grid(True)
    plt.show()

def main():
    locations = read_points_from_file('data/test_data.txt')

    n = len(locations)
    distances = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(locations[i], locations[j])
            distances[i][j] = dist
            distances[j][i] = dist  

    mst = kruskal_mst(distances)

    tsp_path = krustral_tsp(mst, start=0)

    plot_tsp_with_arrows(locations, tsp_path)

if __name__ == "__main__":
    main()
