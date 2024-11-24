from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import math

app = Flask(__name__)
CORS(app)  

def calculate_distance_matrix(points):
    n = len(points)
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = points[i][0], points[i][1]
                x2, y2 = points[j][0], points[j][1]
                distances[i][j] = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distances

def greedy_tsp(distances, start):
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

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.get_json()
    locations = data['locations']

    points = [(loc['lat'], loc['lng']) for loc in locations]

    distance_matrix = calculate_distance_matrix(points)
    start_index = 0
    path, total_distance = greedy_tsp(distance_matrix, start_index)

    route = [{'lat': points[i][0], 'lng': points[i][1]} for i in path]
    return jsonify({'route': route, 'totalDistance': round(total_distance, 2)})

if __name__ == '__main__':
    app.run(debug=True)
