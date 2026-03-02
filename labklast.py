import random, math

#Чтение городов из файла
cities = []
with open("city.txt", encoding="utf-8") as f:
    for line in f:
        p = line.split()
        cities.append([float(p[-2]), float(p[-1]), " ".join(p[:-2])])  # [x, y, название]

K = int(input("Введите кол-во кластеров: "))

#Случайные начальные центры
centers = [cities[i][:2] for i in random.sample(range(len(cities)), K)]

#Алгоритм k-means
for _ in range(100):
    old = centers[:]

    #Назначение кластеров для городов
    for c in cities:
        # находим индекс ближайшего центра
        nearest = min(range(K), key=lambda i: math.hypot(c[0]-centers[i][0], c[1]-centers[i][1]))
        if len(c) == 3:
            c.append(nearest)
        else:
            c[3] = nearest

    #Пересчёт центров
    centers = [
        [sum(c[0] for c in cities if c[3]==i)/len([c for c in cities if c[3]==i]),
         sum(c[1] for c in cities if c[3]==i)/len([c for c in cities if c[3]==i])]
        if any(c[3]==i for c in cities) else old[i]
        for i in range(K)
    ]

#Вывод кластеров
for i in range(K):
    cx, cy = centers[i]
    print(f"\nКластер {i+1}, центр ({cx:.2f}, {cy:.2f})")
    for c in cities:
        if c[3] == i:
            d = math.hypot(c[0]-cx, c[1]-cy)  # расстояние до центра
            print(f"  {c[2]} ({d:.2f})")
