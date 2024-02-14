import random
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
    [45.171244, 5.689872]
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


def find_shortest_path(start_point):
    path = []
    visited = [False] * len(all_points)
    path.append(start_point)
    next_point = start_point
    for i in range(0, len(all_points) - 1):
        next_point = find_next_move(next_point, visited, path)
    return path


def calc_dist_total(path):
    total = 0
    for i in range(0, len(path) - 1):
        total = total + distances[path[i]][path[i + 1]]
    return total


path = find_shortest_path(0)
print("Résultat Plus proche voisin :", path)
total = calc_dist_total(path)
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


path2opt = algo_opt(path.copy())
print("Résultat 2-opt :", path2opt)
total2 = calc_dist_total(path2opt)
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
            if calc_dist_total(temp) < calc_dist_total(result):
                result = temp[:]
            temp.pop(j)
    return result


path_glouton = algo_glouton(0, original_path.copy())
print("Résultat Glouton :", path_glouton)
total3 = calc_dist_total(path_glouton)
print("La distance est égale à :", total3, "Km")

path_glouton_2opt = algo_opt(path_glouton.copy())
print("Résultat glouton + 2-opt :", path_glouton_2opt)
total4 = calc_dist_total(path_glouton_2opt)
print("La distance est égale à :", total4, "Km")


# Algo Génétique______________________________________________________________________
def individu():
    groupe = []
    for i in range(0, len(all_points)):
        groupe.append(find_shortest_path(i))
        # print(groupe[i])
        # print(calc_dist_total(groupe[i]))
    return groupe


groupe_individu = individu()


def best_parent(groupe):
    parents = groupe
    shortest_way = 10000
    best = []
    for i in range(0, len(parents) - 1):
        if calc_dist_total(parents[i]) < shortest_way:
            shortest_way = calc_dist_total(parents[i])
            best.append(parents[i])
    return best


def worst_parent(groupe):
    parents = groupe
    longer_way = 0
    worst_index = 0
    for i in range(0, len(parents) - 1):
        if calc_dist_total(parents[i]) > longer_way:
            longer_way = calc_dist_total(parents[i])
            worst_index = i
    return worst_index


def crossover(parent_a, parent_b):
    pivot = random.randint(len(parent_a) // 4, len(parent_a) * 3 // 4)
    fils = parent_a[0:pivot]
    print("genes du parent_a", fils)
    for i in range(len(parent_b)):
        if parent_b[i] not in fils:
            fils.append(parent_b[i])
    print("fils", fils, calc_dist_total(fils))
    return fils


def swap(list, i, j):
    list[i], list[j] = list[j], list[i]


# def mutation(fils):
#     min = 1000
#     index = 1000
#     for i in range(len(fils) - 1):
#         if distances[fils[i]][fils[i + 1]] < min:
#             min = distances[fils[i]][fils[i + 1]]
#             index = i
#     swap(fils, index, index - 1)
#     return fils
def mutation(fils):
    i = random.randint(0, len(fils) - 1)
    j = random.randint(0, len(fils) - 1)
    if i == j:
        j = random.randint(0, len(fils) - 1)
    swap(fils, i, j)
    return fils


def algo_genetic(groupe):
    new_generation = groupe
    parent_a = best_parent(new_generation)[-1]
    parent_b = best_parent(new_generation)[-2]
    print("parent_a", parent_a, calc_dist_total(parent_a))
    print("parent_b", parent_b, calc_dist_total(parent_b))
    fils = crossover(parent_a, parent_b)
    # if hasard > pourcentage:
    fils_mute = mutation(fils)
    fils_amelio = algo_opt(fils_mute)
    print("fils amélioré", fils_amelio, calc_dist_total(fils_amelio))
    if calc_dist_total(fils_amelio) < calc_dist_total(parent_b):
        print(worst_parent(new_generation))
        # new_generation.pop(worst_parent(new_generation))
        new_generation.append(fils_amelio)
        print(new_generation)
        print(len(new_generation))
    return new_generation


def genetic():
    result = []
    for i in range(len(all_points) * len(all_points)):
        result = algo_genetic(algo_genetic(groupe_individu))
    best_result = best_parent(result)[-1]
    print(best_result, calc_dist_total(best_result))
    return best_result


path_genetic = genetic()
# Algo Fourmis________________________________________________________________________


# Affichage___________________________________________________________________________
m = folium.Map([45.18486504179179, 5.731181509376984], zoom_start=14)

folium.Marker(
    location=[45.18486504179179, 5.731181509376984],
    tooltip="Le Campus Numérique",
    # popup="Le Campus Numérique",
    icon=folium.Icon(color="purple", icon="cloud"),
).add_to(m)


def display_points(all_points):
    for i in range(0, len(all_points)):
        folium.Marker(
            location=[all_points[i][0], all_points[i][1]],
            tooltip=i,
            icon=folium.Icon(color="green", icon=""),
        ).add_to(m)


display_points(all_points)


def path_coordinates(path):
    path_coords = []
    for i in range(0, len(path)):
        path_coords.append([all_points[path[i]][0], all_points[path[i]][1]])
    return path_coords


# folium.PolyLine(path_coordinates(path), color="red", tooltip="shortest_path").add_to(m)
# folium.PolyLine(path_coordinates(path2opt), color="blue", tooltip="2opt_path").add_to(m)
# folium.PolyLine(path_coordinates(path_glouton), color="green", tooltip="2opt_path").add_to(m)
# folium.PolyLine(path_coordinates(path_glouton_2opt), color="red", tooltip="2opt_path").add_to(m)
folium.PolyLine(path_coordinates(path_genetic), color="blue", tooltip="2opt_path").add_to(m)

m.save("index.html")
