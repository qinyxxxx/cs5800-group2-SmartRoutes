import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import math


def plot_tsp_with_arrows(points, path, total_distance):
    """
    Plot TSP solution with direction arrows and distances
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate plot limits with padding
    x_coords = [p[1] for p in points]
    y_coords = [p[2] for p in points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    padding = max(x_max - x_min, y_max - y_min) * 0.1

    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    # Plot points
    ax.scatter(x_coords, y_coords, color='red', zorder=2)

    # Add labels
    for i, point in enumerate(points):
        ax.text(point[1], point[2], f" {point[0]}", fontsize=12)

    # Plot path with arrows
    for i in range(len(path) - 1):
        current = path[i]
        next_point = path[i + 1]

        # Get coordinates
        x1, y1 = points[current][1], points[current][2]
        x2, y2 = points[next_point][1], points[next_point][2]

        # Add arrow
        arrow = FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle='-|>',
            color='blue',
            mutation_scale=20,
            zorder=1
        )
        ax.add_patch(arrow)

        # Add distance label for each segment
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        ax.text(mid_x, mid_y, f'{distance:.1f}',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # Add title with total distance
    ax.set_title(f"TSP Path Visualization\nTotal Distance: {total_distance:.2f}")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.grid(True)

    plt.tight_layout()
    plt.show()
