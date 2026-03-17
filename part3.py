from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import numpy as np

cities, names = [], []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3: continue
        names.append(parts[0])
        cities.append([float(parts[1]), float(parts[2])])
cities = np.array(cities)

n = len(cities)
while True:
    K = int(input("Введите количество кластеров: "))
    if 1 <= K <= n: break
    print(f"Количество кластеров должно быть от 1 до {n}")

model = AgglomerativeClustering(n_clusters=K, linkage='single')  # минимальное расстояние
labels = model.fit_predict(cities)

for k in range(K):
    cluster_idx = np.where(labels==k)[0]
    print(f"\nКластер {k+1}")
    for i in cluster_idx:
        # расстояние до "центра" можно вычислить как среднее точки
        cx, cy = cities[cluster_idx].mean(axis=0)
        d = np.linalg.norm(cities[i]-[cx,cy])
        print(f"  {names[i]} ({d:.2f})")
    print(f"Центр: ({cx:.2f},{cy:.2f})")

colors = ["red","blue","green","orange","purple","brown","pink","cyan"]
plt.figure(figsize=(8,6))
for k in range(K):
    idx = np.where(labels==k)[0]
    plt.scatter(cities[idx,1], cities[idx,0], color=colors[k%len(colors)], label=f"Кластер {k+1}")
    for i in idx:
        plt.text(cities[i,1], cities[i,0], names[i])
# центры
for k in range(K):
    idx = np.where(labels==k)[0]
    cx, cy = cities[idx].mean(axis=0)
    plt.scatter(cy, cx, marker='x', s=200, color='black')
plt.xlabel("Долгота"); plt.ylabel("Широта"); plt.title("Агломеративная кластеризация")
plt.legend(); plt.grid(); plt.axis("equal"); plt.show()
