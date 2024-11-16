
import sys
import os
import numpy as np
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.plot_kruskal import plot_tsp_with_arrows

# Union-Find Data Structure for Kruskal's Algorithm
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

def read_coordinates(file_path):
    """
    Reads coordinates from a file and returns a list of points.
    :param file_path: Path to the coordinates file
    :return: List of (label, x, y)
    """
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            label, x, y = line.strip().split(',')
            points.append((label, float(x), float(y)))
    return points

def calculate_distance_matrix(points):
    """
    Calculates the distance matrix between points based on their coordinates.
    :param points: List of (label, x, y)
    :return: List of edges as tuples (distance, node1, node2)
    """
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):  
            x1, y1 = points[i][1], points[i][2]
            x2, y2 = points[j][1], points[j][2]
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            edges.append((distance, i, j))
    return edges

def kruskal_mst(points, edges):
    """
    Solves the Minimum Spanning Tree (MST) using Kruskal's Algorithm.
    :param points: List of (label, x, y)
    :param edges: List of edges as tuples (distance, node1, node2)
    :return: List of edges in the MST
    """
    edges.sort()  
    uf = UnionFind(len(points))
    mst = []
    total_distance = 0
    for edge in edges:
        distance, u, v = edge
        if uf.union(u, v):  
            mst.append(edge)
            total_distance += distance
    return mst, total_distance

def main():
    # Read coordinates from the file
    coordinates_file = "data/test_data.txt"
    points = read_coordinates(coordinates_file)
    
    # Calculate the list of edges
    edges = calculate_distance_matrix(points)
    # Run Kruskal's algorithm to find the MST
    mst, total_distance = kruskal_mst(points, edges)
    # Output the MST edges and total weight
    print("MST Edges:")
    for edge in mst:
        distance, u, v = edge
        print(f"{points[u][0]} -- {points[v][0]} : {round(distance, 2)}")
    print("Total weight of MST:", round(total_distance, 2))
    # Plot the results
    plot_tsp_with_arrows(points, mst, total_distance)

if __name__ == "__main__":
    main()


