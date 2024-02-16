import random
import time

import haversine as hs
import folium
import csv
import numpy as np

all_points = [
    [45.171112, 5.695952],
    [45.183152, 5.699386],
    [45.174115, 5.711106],
    [45.176123, 5.722083],
    [45.184301, 5.719791],
    [45.184252, 5.730698],
    [45.170588, 5.716664],
    [45.193702, 5.691028],
    [45.165641, 5.739938],
    [45.178718, 5.744940],
    [45.176857, 5.762518],
    [45.188512, 5.767172],
    [45.174017, 5.706729],
    [45.174458, 5.687902],
    [45.185110, 5.733667],
    [45.185702, 5.734507],
    [45.184726, 5.734666],
    [45.184438, 5.733735],
    [45.184902, 5.735256],
    [45.174812, 5.698095],
    [45.169851, 5.695723],
    [45.180943, 5.698965],
    [45.176205, 5.692165],
    [45.171244, 5.689872],
]


def loadFile():
    all_points.clear()
    with open('Data/70villes.csv') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # skip header line
        for row in csvreader:
            lat = float(row[0])
            lon = float(row[1])
            all_points.append([lat, lon])
    return all_points


loadFile()


def calc_distance_between_two_points(pointA, pointB, all_points):
    loc1 = (all_points[pointA][0], all_points[pointA][1])
    loc2 = (all_points[pointB][0], all_points[pointB][1])
    result = hs.haversine(loc1, loc2)
    return result


def calc_distances_between_all_points(all_points):
    distances = []
    for i in range(0, len(all_points)):
        row = []
        for j in range(0, len(all_points)):
            if i == j:
                result = 0
            else:
                result = calc_distance_between_two_points(i, j, all_points)
            row.append(result)
            # print(f"La distance entre les points {i} et {j} est égale à {result} km")
        distances.append(row)
    return distances


distances = calc_distances_between_all_points(all_points)

original_path = []
for i in range(len(all_points)):
    original_path.append(i)


def calc_dist_total(path):
    total = 0
    for i in range(0, len(path) - 1):
        total = total + distances[path[i]][path[i + 1]]
    return total


def calc_boucle(path):
    boucle = calc_dist_total(path) + distances[path[0]][path[-1]]
    return boucle


# Algo Plus proche voisin______________________________________________________
def find_next_move(last_point, visited, path):
    shortest_way = 10000
    next_index = 10000
    for i in range(0, len(all_points)):
        if distances[last_point][i] > 0 and not visited[i]:
            if distances[last_point][i] < shortest_way:
                shortest_way = distances[last_point][i]
                next_index = i
    visited[last_point] = True
    path.append(next_index)
    return next_index


def calc_path(start_point):
    path = []
    visited = [False] * len(all_points)
    path.append(start_point)
    next_point = start_point
    for i in range(0, len(all_points) - 1):
        next_point = find_next_move(next_point, visited, path)
    path.append(path[0])
    return path


def shortest_path():
    shortest_way = 10000
    best_path = []
    for i in range(0, len(all_points) - 1):
        path = calc_path(i)
        if calc_boucle(path) < shortest_way:
            shortest_way = calc_boucle(path)
            best_path.insert(0, path)
    return best_path[0]


path_shortest = shortest_path()
print("Résultat Plus proche voisin :", path_shortest)
total = calc_boucle(path_shortest)
print("La distance est égale à :", total, "Km")


# Algo 2-opt_____________________________________________________________________________________
def reverse(list):
    temp = []
    while list:
        temp.append(list.pop())
    return temp


def gain_reverse(path, i, j):
    if i < j:
        # a = distance entre i et i+2
        a = distances[path[i]][path[j + 1]]
        # b = distance entre i-1 et i+1
        b = distances[path[(i + len(path) - 1) % len(path)]][path[j]]
        # c = distance entre i-1 et i
        c = distances[path[(i + len(path) - 1) % len(path)]][path[i]]
        # a = distance entre i+1 et i+2
        d = distances[path[j]][path[(j + 1) % len(path)]]
        gain = a + b - c - d
    return gain


def algo_opt(path):
    for i in range(1, len(path)):
        for j in range(i + 1, len(path) - 1):
            path[i:j + 1] = reverse(path[i:j + 1])
            if gain_reverse(path, i, j) < 0:
                path[i:j + 1] = reverse(path[i:j + 1])
    return path


path_2opt = algo_opt(path_shortest.copy())
print("Résultat Plus proche voisin + 2-opt :", path_2opt)
total2 = calc_boucle(path_2opt)
print("La distance est égale à :", total2, "Km")


# Algo Glouton________________________________________________________________________
def algo_glouton(start_point, path):
    result = []
    result.insert(0, path.pop(start_point))
    while len(path) > 0:
        new_point = path.pop()
        temp = result[:]  # équivalent à result.copy()
        result.append(new_point)
        for j in range(1, len(result)):
            temp.insert(j, new_point)
            if calc_boucle(temp) < calc_boucle(result):
                result = temp[:]
            temp.pop(j)
    result.append(result[0])
    return result


def shortest_glouton(path):
    shortest_way = 10000
    best_path = []
    for i in range(0, len(path) - 1):
        p = algo_glouton(i, path.copy())
        if calc_boucle(p) < shortest_way:
            shortest_way = calc_boucle(p)
            best_path.insert(0, p)
    return best_path[0]


path_glouton = shortest_glouton(original_path.copy())
print("Résultat Glouton :", path_glouton)
total3 = calc_boucle(path_glouton)
print("La distance est égale à :", total3, "Km")

path_glouton_2opt = algo_opt(path_glouton.copy())
print("Résultat glouton + 2-opt :", path_glouton_2opt)
total4 = calc_boucle(path_glouton_2opt)
print("La distance est égale à :", total4, "Km")


# Algo Quick sort______________________________________________________________________
def swap(list, i, j):
    list[i], list[j] = list[j], list[i]


def tri_quick(list, first, last):
    if first < last:
        pivot = partition(list, first, last)
        tri_quick(list, first, pivot - 1)
        tri_quick(list, pivot + 1, last)
    return list


def partition(list, first, last):
    pivot = last
    mur = first
    for i in range(first, last):
        if calc_boucle(list[i]) <= calc_boucle(list[pivot]):
            swap(list, i, mur)
            mur += 1
    swap(list, last, mur)
    return mur


# Algo Génétique______________________________________________________________________
def individu():
    groupe = []
    for i in range(0, len(all_points)):
        groupe.append(algo_glouton(i, original_path.copy()))
    tri_quick(groupe, 0, len(groupe) - 1)
    return groupe


groupe_individu = individu()


def best_parent(groupe):
    parents = groupe
    shortest_way = 10000
    best = []
    for i in range(0, len(parents) - 1):
        if calc_boucle(parents[i]) < shortest_way:
            shortest_way = calc_boucle(parents[i])
            best.insert(0, parents[i])
    return best


def worst_parent(groupe):
    parents = groupe
    longer_way = 0
    worst_index = 0
    for i in range(0, len(parents) - 1):
        if calc_boucle(parents[i]) > longer_way:
            longer_way = calc_boucle(parents[i])
            worst_index = i
    return worst_index


def crossover(parent_a, parent_b):
    pivot = random.randint(len(parent_a) // 4, len(parent_a) * 3 // 4)
    fils = parent_a[0:pivot]
    for i in range(len(parent_b)):
        if parent_b[i] not in fils:
            fils.append(parent_b[i])
    fils.append(parent_a[0])
    return fils


def mutation(fils):
    i = random.randint(0, len(fils) - 1)
    j = random.randint(0, len(fils) - 1)
    if i == j:
        j = random.randint(0, len(fils) - 1)
    swap(fils, i, j)
    return fils


def algo_genetic(groupe):
    new_generation = groupe
    parent_a = best_parent(new_generation)[0]
    parent_b = new_generation[random.randint(0, len(new_generation) - 1)]
    fils = crossover(parent_a, parent_b)
    if random.randint(0, 100) > 20:
        fils_mute = mutation(fils)
    else:
        fils_mute = fils
    fils_amelio = algo_opt(fils_mute)
    new_generation.append(fils_amelio)
    new_generation.pop(worst_parent(new_generation))
    return new_generation


def genetic():
    start_time = time.time()
    result = []
    for i in range(len(all_points) * len(all_points)):
        result = algo_genetic(algo_genetic(groupe_individu))
    best_result = best_parent(result)[0]
    print("\033[1;32mRésulat génétic :", best_result)
    print("La distance est égale à :", calc_boucle(best_result), "Km")
    end_time = time.time()
    print("Temps écoulé :", end_time - start_time)
    return best_result


path_genetic = genetic()


def format_path(path):
    max = 0
    index_max = 0
    for i in range(0, len(path) - 1):
        if distances[path[i]][path[i + 1]] > max:
            max = distances[path[i]][path[i + 1]]
            index_max = i + 1
    path.pop(-1)
    best_path = path[index_max:]
    best_path.extend(path[:index_max])
    return best_path


# best_path = format_path(path_genetic)
# print("Résultat génétic formaté :", best_path)
# total5 = calc_dist_total(best_path)
# print("La distance est égale à :", total5, "Km")


# Algo Fourmis________________________________________________________________________
def calc_distances_numpy(all_points):
    num_points = len(all_points)
    distances = np.zeros((num_points, num_points))
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                distance = calc_distance_between_two_points(i, j, all_points)
                distances[i][j] = distance
                distances[j][i] = distance  # Since it's symmetric, fill both sides
    return distances


dist1 = calc_distances_numpy(all_points)


class AntColony:
    def __init__(self, distan, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        """
        self.distan = distan
        self.pheromone_level = 1 / (len(distan) * random.uniform(0.5, 1))
        self.pheromones = [] * len(distan) * len(distan)
        self.all_inds = range(len(distan))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", float("inf"))
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self.pheromone_level *= self.decay
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone_level += 1.0 / self.distan[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distan[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(i)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distan) - 1):
            print(prev)
            print(self.distan[i])
            move = self.pick_move(self.pheromones[prev], self.distan[prev, :], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # going back to where we started
        return path

    def pick_move(self, pheromones, dist, visited):
        pheromone = list(pheromones)
        dist = list(dist)
        pheromone = [pheromones[i] ** self.alpha for i in range(len(pheromones))]
        dist = [(1.0 / dist[i]) ** self.beta for i in range(len(dist))]
        pheromone_total = sum(pheromone)
        dist_total = sum(dist)
        move_probs = [0 for i in range(len(pheromone))]
        for i in range(len(pheromone)):
            move_probs[i] = (pheromone[i] / pheromone_total) * (dist[i] / dist_total)
        move_probs = [i / sum(move_probs) for i in move_probs]
        move = self.pick_weighted_random(move_probs, visited)
        return move

    def pick_weighted_random(self, weighted_list, visited):
        sum_weights = sum(weighted_list)
        if sum_weights <= 0:
            return random.choice(list((set(range(len(weighted_list))) - visited)))
        cum_weights = [0] + list(np.cumsum(weighted_list))
        r = random.random() * sum_weights
        for j in range(len(cum_weights)):
            if cum_weights[j] > r:
                return j - 1


"""
       Args:
           distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
           n_ants (int): Number of ants running per iteration
           n_best (int): Number of best ants who deposit pheromone
           n_iteration (int): Number of iterations
           decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
           alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
           beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
       """


# fourmis = AntColony(dist1, len(all_points), len(all_points), len(all_points), 0.95)
# result = fourmis.run()
# print(result)


# Affichage___________________________________________________________________________
def display_map(name, path):
    path_coords = []
    for i in range(0, len(path)):
        path_coords.append([all_points[path[i]][0], all_points[path[i]][1]])
    if len(path_coords) < 30:
        zoom = 14
    else:
        zoom = 9
    est = 0
    ouest = 90
    north = 90
    south = 0
    for i in range(len(path_coords) - 1):
        if path_coords[i][1] < ouest:
            ouest = path_coords[i][1]
        if path_coords[i][1] > est:
            est = path_coords[i][1]
        if path_coords[i][0] < north:
            north = path_coords[i][0]
        if path_coords[i][0] > south:
            south = path_coords[i][0]
    lat = (south + north) / 2
    lon = (est + ouest) / 2
    m = folium.Map([lat, lon], zoom_start=zoom)
    folium.Marker(
        location=[45.18486504179179, 5.731181509376984],
        tooltip="Le Campus Numérique",
        # popup="Le Campus Numérique",
        icon=folium.Icon(color="purple", icon="cloud"),
    ).add_to(m)
    for i in range(0, len(all_points)):
        folium.Marker(
            location=[all_points[i][0], all_points[i][1]],
            tooltip=i,
            icon=folium.Icon(color="green", icon=""),
        ).add_to(m)
    folium.PolyLine(path_coords, color="blue", tooltip="path").add_to(m)
    m.save(name)


display_map("map1.html", path_shortest)
display_map("map2.html", path_2opt)
display_map("map3.html", path_glouton)
display_map("map4.html", path_glouton_2opt)
display_map("map5.html", path_genetic)
# display_map("map5.html", best_path)
