import random
import time

import haversine as hs
import folium
import csv

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


# loadFile()


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


# def format_path(path):
#     max = 0
#     index_max = 0
#     for i in range(0, len(path) - 1):
#         if distances[path[i]][path[i + 1]] > max:
#             max = distances[path[i]][path[i + 1]]
#             index_max = i + 1
#     path.pop(-1)
#     best_path = path[index_max:]
#     best_path.extend(path[:index_max])
#     print(best_path)
#     print(len(best_path))
#     return best_path


# path_glouton = format_path(shortest_glouton(original_path.copy()))
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
    fils_mute = mutation(fils)
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


# Algo Fourmis________________________________________________________________________


# Affichage___________________________________________________________________________
def display_map(name, path):
    m = folium.Map([45.18486504179179, 5.731181509376984], zoom_start=14)
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
    path_coords = []
    for i in range(0, len(path)):
        path_coords.append([all_points[path[i]][0], all_points[path[i]][1]])
    folium.PolyLine(path_coords, color="blue", tooltip="path").add_to(m)
    m.save(name)


display_map("map1.html", path_shortest)
display_map("map2.html", path_2opt)
display_map("map3.html", path_glouton)
display_map("map4.html", path_glouton_2opt)
display_map("map5.html", path_genetic)
