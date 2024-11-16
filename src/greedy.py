import numpy as np
import math

from src.plot import plot_tsp_with_arrows


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
    :return: 2D numpy array representing the distance matrix
    """
    n = len(points)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = points[i][1], points[i][2]
                x2, y2 = points[j][1], points[j][2]
                distances[i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distances


def greedy_tsp(distances, start):
    """
    Solves the Traveling Salesman Problem (TSP) using a greedy approach.
    :param distances: 2D numpy array representing the distance matrix
    :param start: Index of the starting point
    :return: Visited path and total distance
    """
    n = distances.shape[0]
    visited = [False] * n
    path = [start]
    total_distance = 0

    visited[start] = True
    current = start
    for _ in range(n - 1):
        nearest = None
        min_distance = float('inf')
        for i in range(n):
            if not visited[i] and distances[current][i] < min_distance:
                nearest = i
                min_distance = distances[current][i]

        path.append(nearest)
        total_distance += min_distance
        visited[nearest] = True
        current = nearest

    total_distance += distances[current][start]
    path.append(start)

    return path, total_distance

def main():
    # Read coordinates from the file
    coordinates_file = "../data/test_data.txt"  # Update this path as needed
    points = read_coordinates(coordinates_file)

    # Calculate the distance matrix
    distance_matrix = calculate_distance_matrix(points)

    # Start TSP from the first point
    start_index = 0
    path, total_distance = greedy_tsp(distance_matrix, start_index)

    # Output results
    print("Visiting order:", [points[i][0] for i in path])
    print("Total distance:", round(total_distance, 2))

    # Plot the results
    plot_tsp_with_arrows(points, path, total_distance)


if __name__ == "__main__":
    main()