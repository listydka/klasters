import math, random
import matplotlib.pyplot as plt

cities, names = [], []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 3: continue
        names.append(parts[0])
        cities.append((float(parts[1]), float(parts[2])))

n = len(cities)

while True:
    K = int(input("Введите количество кластеров: "))
    if 1 <= K <= n: break
    print(f"Количество кластеров должно быть от 1 до {n}")

dist = [[math.hypot(cities[i][0]-cities[j][0], cities[i][1]-cities[j][1])
         for j in range(n)] for i in range(n)]

print("\nМатрица расстояний:")
print("      " + "  ".join(names))
for i,row in enumerate(dist):
    print(f"{names[i]:<6}" + "  ".join(f"{d:.2f}" for d in row))

centers = random.sample(cities, K)  #первая итерация — реальные города
for it in range(20):
    clusters = [[] for _ in range(K)]
    for i,(x,y) in enumerate(cities):
        idx = min(range(K), key=lambda j: math.hypot(x-centers[j][0], y-centers[j][1]))
        clusters[idx].append(i)

    new_centers = [(sum(cities[i][0] for i in c)/len(c),
                    sum(cities[i][1] for i in c)/len(c)) for c in clusters]

    print(f"\n=== Итерация {it+1} ===")
    for idx,c in enumerate(clusters):
        cx,cy = new_centers[idx]
        print(f"\nКластер {idx+1}")
        print(f"Центр: ({cx:.2f},{cy:.2f})")
        print("Города:")
        for i in c:
            d = math.hypot(cities[i][0]-cx, cities[i][1]-cy)
            print(f"  {names[i]} ({d:.2f})")

    if it > 0 and new_centers == centers:
        break
    centers = new_centers

colors = ["red","blue","green","orange","purple","brown","pink","cyan"]
plt.figure(figsize=(8,6))
for i,c in enumerate(clusters):
    xs = [cities[j][1] for j in c]  # долгота
    ys = [cities[j][0] for j in c]  # широта
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
