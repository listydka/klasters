import math, random
import matplotlib.pyplot as plt

cities, names = [], []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if len(p) < 3: continue
        names.append(p[0])
        cities.append((float(p[1]), float(p[2])))
n = len(cities)

def kmeans(K, iters=50):
    centers = random.sample(cities, K)
    for _ in range(iters):
        clusters = [[] for _ in range(K)]
        for i,(x,y) in enumerate(cities):
            idx = min(range(K), key=lambda j: math.hypot(x-centers[j][0], y-centers[j][1]))
            clusters[idx].append(i)
        new_centers = [(sum(cities[i][0] for i in c)/len(c),
                        sum(cities[i][1] for i in c)/len(c)) for c in clusters]
        if new_centers == centers: break
        centers = new_centers
    return clusters, centers

def inertia(clusters, centers):
    return sum((cities[i][0]-centers[k][0])**2 + (cities[i][1]-centers[k][1])**2
               for k,c in enumerate(clusters) for i in c)

Ks = range(1, min(10,n)+1)
errs = []
random.seed(42)

for K in Ks:
    best_err = float('inf')
    for _ in range(5):
        cl, cen = kmeans(K)
        e = inertia(cl, cen)
        if e < best_err: best_err = e
    errs.append(best_err)
    print(f"K={K}, сумма квадратов расстояний={best_err:.2f}")

def find_elbow(errs):
    diffs = [errs[i-1]-errs[i] for i in range(1,len(errs))]
    for i in range(1,len(diffs)):
        if diffs[i] < 0.5*diffs[i-1]:  # уменьшение резко замедлилось
            return i+1  # K = i+1
    return errs.index(min(errs))+1

recommended_K = find_elbow(errs)
plt.plot(list(Ks), errs, marker='o')
plt.axvline(recommended_K, color='red', linestyle='--', label=f'локоть K={recommended_K}')
plt.xlabel("K")
plt.ylabel("Сумма квадратов расстояний")
plt.title("Метод локтя")
plt.grid()
plt.legend()
plt.show()

K = int(input(f"Выберите K по графику (рекомендуется {recommended_K}): "))
clusters, centers = kmeans(K)

print("\nРезультат кластеризации:")
for idx, cluster in enumerate(clusters):
    cx, cy = centers[idx]
    print(f"\nКластер {idx+1} (центр: {cx:.2f},{cy:.2f}):")
    for i in cluster:
        d = math.hypot(cities[i][0]-cx, cities[i][1]-cy)
        print(f"  {names[i]} ({d:.2f})")

colors=["red","blue","green","orange","purple","brown","pink","cyan"]
plt.figure(figsize=(8,6))
for i,c in enumerate(clusters):
    xs=[cities[j][1] for j in c]
    ys=[cities[j][0] for j in c]
    plt.scatter(xs,ys,color=colors[i%len(colors)],label=f"Кластер {i+1}")
    for j in c: plt.text(cities[j][1],cities[j][0],names[j])
for x,y in centers: plt.scatter(y,x,marker='x',s=200,color='black')
plt.xlabel("Долгота")
plt.ylabel("Широта")
plt.title("Кластеризация городов")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()
