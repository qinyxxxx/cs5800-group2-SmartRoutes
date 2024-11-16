
import matplotlib.pyplot as plt
import numpy as np


def plot_tsp_with_arrows(points, mst, total_distance):
    """
    Plots the points and the edges in the minimum spanning tree (MST).
    :param points: List of (label, x, y) tuples representing points.
    :param mst: List of edges in the MST.
    :param total_distance: Total distance of the MST.
    """
    # Extract coordinates of points
    labels, x_coords, y_coords = zip(*[(label, x, y) for label, x, y in points])
    
    # Plot the points
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, color='red', label='Points', zorder=5)
    
    # Plot the edges of the MST
    for edge in mst:
        distance, u, v = edge
        x1, y1 = x_coords[u], y_coords[u]
        x2, y2 = x_coords[v], y_coords[v]
        plt.plot([x1, x2], [y1, y2], color='blue', lw=2, zorder=1)
        # Add an arrow to indicate the direction
        plt.arrow(x1, y1, x2 - x1, y2 - y1, head_width=0.05, head_length=0.1, fc='black', ec='black', zorder=2)
    # Label points
    for i, label in enumerate(labels):
        plt.text(x_coords[i] + 0.1, y_coords[i] + 0.1, label, fontsize=12, ha='left', va='bottom')
    # Set plot labels and title
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title(f"Minimum Spanning Tree (MST)\nTotal Distance: {round(total_distance, 2)}")
    
    # Show the plot
    plt.legend()
    plt.grid(True)
    plt.show()
