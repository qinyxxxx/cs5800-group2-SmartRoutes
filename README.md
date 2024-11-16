# SmartRoutes

SmartRoutes is a project focused on exploring and implementing efficient algorithms to solve routing problems. Our goal is to find near-optimal solutions for visiting multiple locations using graph-based methods, with potential applications in delivery services, school buses, and robotic path planning.

## Project Overview

Routing problems, such as determining the most efficient path to visit a set of locations, are known to be NP-complete. Instead of finding the exact optimal solution, we implement and compare two approximation strategies:
- **Greedy (Nearest Neighbor)**: A simple heuristic that selects the closest unvisited location at each step.
- **Minimum Spanning Tree (MST)**: A graph-based approach using Kruskal's and Prim's algorithms, extended with optimization techniques like Christofides' Algorithm.

## Key Features

1. **Algorithm Implementation**:
   - Greedy Nearest Neighbor.
   - Minimum Spanning Tree with optimization.
2. **Performance Comparison**:
   - Evaluate both algorithms on simulated datasets of varying sizes.
   - Analyze computation time, total distance, and accuracy.
3. **Visualization**:
   - Graphs and tables to showcase the performance and results.

## How It Works

1. **Input**: A set of points (e.g., delivery locations) with distances between them.
2. **Algorithms**: 
   - Greedy Nearest Neighbor to quickly find a suboptimal route.
   - MST-based methods for more balanced solutions.
3. **Output**: Routes optimized for total distance or time.

## Project Structure

- `data/`: Contains datasets for testing, including both simulated and real-world examples.
- `src/`: Source code for algorithms and performance evaluation.
- `results/`: Generated graphs, tables, and summaries.
- `docs/`: Presentation materials and detailed project documentation.
