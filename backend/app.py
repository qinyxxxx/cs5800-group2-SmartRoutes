from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
print("Google Maps API Key:", GOOGLE_MAPS_API_KEY)

def get_distance_matrix(locations):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(locations),
        "destinations": "|".join(locations),
        "key": GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["rows"]
    else:
        raise Exception("Failed to fetch distance matrix from Google Maps API")


def solve_tsp_greedy(distances):
    n = len(distances)
    visited = [False] * n
    path = [0]  # start from the first position
    visited[0] = True

    for _ in range(n - 1):
        last = path[-1]
        next_city = min(
            [(i, distances[last][i]) for i in range(n) if not visited[i]],
            key=lambda x: x[1],
        )[0]
        path.append(next_city)
        visited[next_city] = True

    return path

@app.route("/greedy", methods=["POST"])
def calculate_tsp():
    try:
        data = request.get_json()
        locations = data.get("locations")
        if not locations or len(locations) < 2:
            return jsonify({"success": False, "message": "At least two locations are required"})

        distance_matrix = get_distance_matrix(locations)
        distances = [[row["elements"][i]["distance"]["value"] for i in range(len(row["elements"]))] for row in distance_matrix]

        tsp_order = solve_tsp_greedy(distances)
        ordered_locations = [locations[i] for i in tsp_order]

        return jsonify({"success": True, "orderedLocations": ordered_locations})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


def greedy_tsp(distances, start):
    n = len(distances)
    if n < 2:
        return [start], 0

    visited = [False] * n
    path = [start]
    total_distance = 0
    visited[start] = True
    current = start
    for _ in range(n - 1):
        nearest = None
        min_distance = float('inf')

        for next_point in range(n):
            if not visited[next_point] and distances[current][next_point] < min_distance:
                nearest = next_point
                min_distance = distances[current][next_point]

        if nearest is None:
            break

        path.append(nearest)
        total_distance += min_distance
        visited[nearest] = True
        current = nearest
    total_distance += distances[current][start]
    path.append(start)

    return path, total_distance


if __name__ == '__main__':
    app.run(debug=True)