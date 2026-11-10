
import math
import time
import os

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 +
                     (p1[1] - p2[1])**2)


def brute_force(points):

    minimum = float('inf')
    pair = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):

            d = distance(points[i], points[j])

            if d < minimum:
                minimum = d
                pair = (points[i], points[j])

    return minimum, pair


def closest_pair(px, py):

    n = len(px)

    if n <= 3:
        return brute_force(px)

    mid = n // 2
    mid_x = px[mid][0]

    left_x = px[:mid]
    right_x = px[mid:]

    left_ids = {p[2] for p in left_x}

    left_y = [p for p in py if p[2] in left_ids]
    right_y = [p for p in py if p[2] not in left_ids]

    d1, pair1 = closest_pair(left_x, left_y)
    d2, pair2 = closest_pair(right_x, right_y)

    if d1 < d2:
        minimum = d1
        best_pair = pair1
    else:
        minimum = d2
        best_pair = pair2

    strip = [p for p in py if abs(p[0] - mid_x) < minimum]

    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):

            d = distance(strip[i], strip[j])

            if d < minimum:
                minimum = d
                best_pair = (strip[i], strip[j])

    return minimum, best_pair


def read_file(filename):

    with open(filename, 'r') as file:

        n = int(file.readline())

        points = []

        for i in range(n):
            x, y = map(int, file.readline().split())
            points.append((x, y, i))

    return points


def main():

    folder = "Closest_Pair"
    os.makedirs("Results", exist_ok=True)

    result_file = open("Results/closest_pair_results.txt", "w")

    for filename in sorted(os.listdir(folder)):

        if filename.endswith(".txt"):

            filepath = os.path.join(folder, filename)

            points = read_file(filepath)

            px = sorted(points, key=lambda p: p[0])
            py = sorted(points, key=lambda p: p[1])

            start = time.perf_counter()

            minimum, pair = closest_pair(px, py)

            end = time.perf_counter()

            execution_time = end - start

            output = f"""
Dataset: {filename}
Number of Points: {len(points)}
Closest Point 1: ({pair[0][0]}, {pair[0][1]})
Closest Point 2: ({pair[1][0]}, {pair[1][1]})
Minimum Distance: {minimum:.4f}
Execution Time: {execution_time:.6f} seconds
"""

            print(output)
            result_file.write(output)

    result_file.close()

    print("All datasets processed successfully!")


if __name__ == "__main__":
    main()