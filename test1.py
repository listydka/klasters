import random
import time
import math
#АЛГОРИТМ
def agglomerative_clustering(cities, K):
    n = len(cities)

    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = cities[i][0] - cities[j][0]
            dy = cities[i][1] - cities[j][1]
            dist[i][j] = math.hypot(dx, dy)

    clusters = [[i] for i in range(n)]

    while len(clusters) > K:
        min_sum = float("inf")
        best_pair = (0, 1)

        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                total = 0
                for a in clusters[i]:
                    for b in clusters[j]:
                        total += dist[a][b]
                if total < min_sum:
                    min_sum = total
                    best_pair = (i, j)

        i, j = best_pair
        clusters[i] += clusters[j]
        clusters.pop(j)

    return clusters
mode_names = {
    "compact": "Компактные данные",
    "spread": "Разбросанные данные",
    "mixed": "Смешанные данные"
}
# компактные кластеры
def generate_compact(n):
    cities = []
    for _ in range(n):
        cities.append((random.uniform(0, 10), random.uniform(0, 10)))
    return cities

# разбросанные точки
def generate_spread(n):
    cities = []
    for _ in range(n):
        cities.append((random.uniform(0, 1000), random.uniform(0, 1000)))
    return cities

# смешанный вариант
def generate_mixed(n):
    cities = []

    for _ in range(n//2):
        cities.append((random.uniform(0, 10), random.uniform(0, 10)))

    for _ in range(n//2):
        cities.append((random.uniform(100, 200), random.uniform(100, 200)))

    return cities

def run_tests():
    sizes = [10, 50, 100, 150]
    K_values = [2, 3, 5]
    repeats = 3


    print("\nРезультаты тестирования\n")

    for mode in ["compact", "spread", "mixed"]:
        print(f"\nТип данных: {mode_names[mode]} ")

        for n in sizes:
            for K in K_values:

                total_time = 0

                for _ in range(repeats):

                    if mode == "compact":
                        cities = generate_compact(n)
                    elif mode == "spread":
                        cities = generate_spread(n)
                    else:
                        cities = generate_mixed(n)

                    start = time.time()

                    agglomerative_clustering(cities, K)

                    end = time.time()
                    total_time += (end - start)

                avg_time = total_time / repeats

                print(f"n={n}, K={K} -> {avg_time:.4f} сек")

run_tests()
