import math, random, time
import matplotlib.pyplot as plt

def kmeans(cities, K, iters=50):
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

def inertia(cities, clusters, centers):
    return sum((cities[i][0]-centers[k][0])**2 + (cities[i][1]-centers[k][1])**2
               for k,c in enumerate(clusters) for i in c)

def find_elbow(errs):
    diffs = [errs[i-1]-errs[i] for i in range(1,len(errs))]
    for i in range(1,len(diffs)):
        if diffs[i] < 0.5*diffs[i-1]:
            return i+1
    return errs.index(min(errs))+1
def generate_cities(type_, n):
    cities = []
    if type_=="compact":
        for _ in range(n):
            x = random.uniform(0,10)
            y = random.uniform(0,10)
            cities.append((x,y))
    elif type_=="spread":
        for _ in range(n):
            x = random.uniform(0,100)
            y = random.uniform(0,100)
            cities.append((x,y))
    elif type_=="mixed":
        for _ in range(n//2):
            x = random.uniform(0,10)
            y = random.uniform(0,10)
            cities.append((x,y))
        for _ in range(n - n//2):
            x = random.uniform(0,100)
            y = random.uniform(0,100)
            cities.append((x,y))
    return cities

random.seed(42)
test_types = ["compact","spread","mixed"]
n_cities_list = [10,50,100]

for test_type in test_types:
    for n_cities in n_cities_list:
        cities = generate_cities(test_type, n_cities)
        Ks = range(1, min(10,len(cities))+1)
        errs = []
        start = time.time()
        for K in Ks:
            best_err = float('inf')
            for _ in range(3):
                cl, cen = kmeans(cities, K)
                e = inertia(cities, cl, cen)
                if e < best_err: best_err = e
            errs.append(best_err)
        elapsed = time.time() - start
        recommended_K = find_elbow(errs)
        print(f"Тест: {test_type}, города={n_cities}, время={elapsed:.2f}s, рекомендуемое K={recommended_K}")
        print("Суммы квадратов:", ["{:.2f}".format(e) for e in errs])

        plt.plot(list(Ks), errs, marker='o', label=f"{test_type}, n={n_cities}")
        plt.axvline(recommended_K, color='red', linestyle='--')
plt.xlabel("K")
plt.ylabel("Сумма квадратов расстояний")
plt.title("Метод локтя для разных типов распределения городов")
plt.legend()
plt.grid()
plt.show()
