import math
cities = []
names = []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        name, x, y = parts[0], float(parts[1]), float(parts[2])
        names.append(name)
        cities.append((x, y))
n = len(cities)
while True:
    K = int(input("Введите количество кластеров: "))
    if 1 <= K <= n:
        break
    print(f"Количество кластеров должно быть от 1 до {n}. Попробуйте ещё раз.")
# Построение матрицы смежности (евклидово расстояние)
dist = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        dx = cities[i][0] - cities[j][0]
        dy = cities[i][1] - cities[j][1]
        dist[i][j] = math.hypot(dx, dy)
print("\nМатрица расстояний:")
print("     " + "  ".join(f"{name}" for name in names))
for i in range(n):
    row = "  ".join(f"{dist[i][j]:.2f}" for j in range(n))
    print(f"{names[i]:<5} {row}")
# Изначально каждый город — отдельный кластер
clusters = [[i] for i in range(n)]
# Основной цикл
while len(clusters) > K:
    min_sum = float("inf")
    best_pair = (0, 1)
    # Сумма расстояний между всеми точками двух кластеров
    for i in range(len(clusters)):
        for j in range(i+1, len(clusters)):
            total = 0
            for a in clusters[i]:
                for b in clusters[j]:
                    total += dist[a][b]
            if total < min_sum:
                min_sum = total
                best_pair = (i, j)
    # Объединяем выбранные кластеры
    i, j = best_pair
    clusters[i] += clusters[j]
    clusters.pop(j)
print("\nРезультат кластеризации:")
for idx, cluster in enumerate(clusters):
    cluster_names = [names[i] for i in cluster]
    print(f"Кластер {idx+1}: {', '.join(cluster_names)}")
