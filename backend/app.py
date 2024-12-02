from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from collections import defaultdict
import heapq


load_dotenv()

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print("Google Maps API Key:", GOOGLE_MAPS_API_KEY)
FIX_START = "4 N 2nd St Suite 150, San Jose, CA 95113"

def get_distance_matrix(locations):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(locations),
        "destinations": "|".join(locations),
        "key": GOOGLE_MAPS_API_KEY,
    }
    
    print("Sending request to API with parameters:", params)

    try:
        response = requests.get(url, params=params, timeout=10)  # Adding timeout
        response.raise_for_status()  # Check if the response status is not 4xx or 5xx
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise

    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        data = response.json()

        if "rows" in data:
            return data["rows"]
        else:
            raise Exception("Invalid response format, 'rows' not found.")
    else:
        raise Exception(f"Failed to fetch distance matrix from Google Maps API. Status Code: {response.status_code}")


def solve_tsp_greedy(distances):
    n = len(distances)
    visited = [False] * n
    path = [0]
    visited[0] = True

    for _ in range(n - 1):
        last = path[-1]
        # find the nearest non-visited
        next_point = min(
            [(i, distances[last][i]) for i in range(n) if not visited[i]],
            key=lambda x: x[1],
        )[0]
        path.append(next_point)
        visited[next_point] = True

    path.append(0)  # back to the start point
    return path

@app.route("/greedy", methods=["POST"])
def calculate_tsp():
    try:
        data = request.get_json()
        locations = data.get("locations")
        if FIX_START not in locations:
            locations.insert(0, FIX_START)

        if not locations or len(locations) < 2:
            return jsonify({"success": False, "message": "At least two locations are required"})

        distance_matrix = get_distance_matrix(locations)

        distances = [
            [row["elements"][i]["distance"]["value"] for i in range(len(row["elements"]))]
            for row in distance_matrix
        ]

        durations = [
            [row["elements"][i]["duration"]["value"] for i in range(len(row["elements"]))]
            for row in distance_matrix
        ]

        tsp_order = solve_tsp_greedy(distances)

        if not distances or not tsp_order or len(tsp_order) < 2:
            raise Exception("Invalid data for TSP calculation")

        total_distance = sum(
            distances[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        total_duration = sum(
            durations[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        ordered_locations = [locations[i] for i in tsp_order]

        travel_details = []
        for i in range(len(tsp_order) - 1):
            start_location = ordered_locations[i]
            end_location = ordered_locations[i + 1]
            distance = distances[tsp_order[i]][tsp_order[i + 1]]
            duration = durations[tsp_order[i]][tsp_order[i + 1]]
            travel_details.append({
                "from": start_location,
                "to": end_location,
                "distance": distance,
                "duration": duration
            })

        return jsonify({
            "success": True,
            "orderedLocations": ordered_locations,
            "totalDistance": total_distance,
            "totalDuration": total_duration,
            "travelDetails": travel_details
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



# Krustral Algorithm
def kruskal_mst(distances):
    n = len(distances)
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            edges.append((distances[i][j], i, j))

    edges.sort(key=lambda x: x[0])

    parent = list(range(n))
    rank = [0] * n

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1

    mst = defaultdict(list)
    for weight, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            mst[u].append(v)
            mst[v].append(u)

    # Print MST after it's constructed
    print("MST from Kruskal's Algorithm (Edges):")
    for node, neighbors in mst.items():
        print(f"Node {node}: {neighbors}")

    return mst


def krustral_tsp(mst, start):
    visited = set()
    path = []

    def dfs(node):
        visited.add(node)
        path.append(node)
        for neighbor in mst[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    path.append(start)  
    return path

@app.route("/kruskal", methods=["POST"])
def calculate_tsp_kruskal():
    try:
        data = request.get_json()
        locations = data.get("locations")

        if FIX_START not in locations:
            locations.insert(0, FIX_START)

        if not locations or len(locations) < 2:
            return jsonify({"success": False, "message": "At least two locations are required"})

        distance_matrix = get_distance_matrix(locations)

        distances = [[row["elements"][i]["distance"]["value"] for i in range(len(row["elements"]))] for row in distance_matrix]
        durations = [[row["elements"][i]["duration"]["value"] for i in range(len(row["elements"]))] for row in distance_matrix]

        print("Distances:", distances)
        print("Durations:", durations)

        mst = kruskal_mst(distances)

        # Get path order
        tsp_order = krustral_tsp(mst, 0)

        # Transfer to the location order
        ordered_locations = [locations[i] for i in tsp_order]

        total_distance = sum(
            distances[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        total_duration = sum(
            durations[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        print("Total distance:", total_distance)
        print("Total duration:", total_duration)

        travel_details = []
        for i in range(len(tsp_order) - 1):
            start_location = ordered_locations[i]
            end_location = ordered_locations[i + 1]
            distance = distances[tsp_order[i]][tsp_order[i + 1]]
            duration = durations[tsp_order[i]][tsp_order[i + 1]]
            travel_details.append({
                "from": start_location,
                "to": end_location,
                "distance": distance,
                "duration": duration
            })

        return jsonify({
            "success": True,
            "orderedLocations": ordered_locations,
            "totalDistance": total_distance,
            "totalDuration": total_duration
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


#Prim's TSP algorithm
def prim_mst(distances):
    n = len(distances)
    # To store the MST
    mst = defaultdict(list)
    visited = [False] * n
    min_heap = [(0, 0, -1)]  # (weight, node), starting from node 0

    while min_heap:
        weight, u, v = heapq.heappop(min_heap)

        if visited[u]:
            continue
        visited[u] = True
        if v != -1:
            mst[u].append(v)
            mst[v].append(u)

        # Add the selected node to the MST
        for v in range(n):
            if not visited[v] and distances[u][v] > 0:  # Avoid self-loops
                heapq.heappush(min_heap, (distances[u][v], v, u))
                # mst[u].append(v)
                # mst[v].append(u)

    # Print MST after it's constructed
    print("MST from Prim's Algorithm (Edges):")
    for node, neighbors in mst.items():
        print(f"Node {node}: {neighbors}")

    return mst

# Prim's TSP path reconstruction (using DFS to visit all nodes)
def prim_tsp(mst, start):
    visited = set()
    path = []

    def dfs(node):
        visited.add(node)
        path.append(node)
        for neighbor in mst[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    path.append(start)  # Return to the starting point
    return path

@app.route("/prim", methods=["POST"])
def calculate_tsp_prim():
    try:
        data = request.get_json()
        locations = data.get("locations")

        if FIX_START not in locations:
            locations.insert(0, FIX_START)

        if not locations or len(locations) < 2:
            return jsonify({"success": False, "message": "At least two locations are required"})

        distance_matrix = get_distance_matrix(locations)

        # Calculate the distances matrix from the distance matrix response
        distances = [
            [row["elements"][i]["distance"]["value"] for i in range(len(row["elements"]))]
            for row in distance_matrix
        ]
        durations = [
            [row["elements"][i]["duration"]["value"] for i in range(len(row["elements"]))]
            for row in distance_matrix
        ]

        print("Prim Distances:", distances)
        print("Prim Durations:", durations)

        # Apply Prim's Algorithm to find the MST
        mst = prim_mst(distances)

        # Get the TSP path using DFS on the MST
        tsp_order = prim_tsp(mst, 0)

        # Convert the path order to the corresponding locations
        ordered_locations = [locations[i] for i in tsp_order]

        # Calculate total distance
        total_distance = sum(
            distances[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        total_duration = sum(
            durations[tsp_order[i]][tsp_order[i + 1]] for i in range(len(tsp_order) - 1)
        )

        return jsonify({
            "success": True,
            "orderedLocations": ordered_locations,
            "totalDistance": total_distance,
            "totalDuration": total_duration
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001) 