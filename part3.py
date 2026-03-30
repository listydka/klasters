import math, random
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

cities, names = [], []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if len(p) < 3: continue
        names.append(p[0])
        cities.append([float(p[1]), float(p[2])])
n = len(cities)

K = int(input(f"Введите количество кластеров (1-{n}): "))

model = AgglomerativeClustering(n_clusters=K)
labels = model.fit_predict(cities)

clusters = [[] for _ in range(K)]
for i,label in enumerate(labels):
    clusters[label].append(i)

print("\nРезультат кластеризации:")
for idx, cluster in enumerate(clusters):
    print(f"\nКластер {idx+1}:")
    for i in cluster:
        print(f"  {names[i]} ({cities[i][0]:.2f},{cities[i][1]:.2f})")

colors = ["red","blue","green","orange","purple","brown","pink","cyan"]
plt.figure(figsize=(8,6))
for i,c in enumerate(clusters):
    xs = [cities[j][1] for j in c]  # долгота
    ys = [cities[j][0] for j in c]  # широта
    plt.scatter(xs, ys, color=colors[i%len(colors)], label=f"Кластер {i+1}")
    for j in c: plt.text(cities[j][1], cities[j][0], names[j])
plt.xlabel("Долгота")
plt.ylabel("Широта")
plt.title("Агломеративная кластеризация городов")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()
