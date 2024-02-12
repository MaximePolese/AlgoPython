import haversine as hs
import folium

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


# def loadFile():
#     listVille.clear()
#     filename = filedialog.askopenfilename(initialdir="./",
#                                           title="Selection du Fichier",
#                                           filetypes=(("Text files",
#                                                       "*.csv*"),
#                                                      ("all files",
#                                                       "*.*")))
#     changeLabelFile("Fichier : " + filename)
#     with open(filename, 'r', encoding='UTF-8') as file:
#         csvreader = csv.reader(file)
#         next(csvreader)  # skip header line
#         for row in csvreader:
#             data = row[0].split(";")
#             try:
#                 ville = Ville(data[8], data[9], float(data[11]), float(data[12]), float(data[13]), 0)
#                 ville.distanceFromGrenoble = getDistanceFromGrenoble(ville)
#                 listVille.append(ville)
#             except:
#                 continue


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
path = []
visited = [False] * len(all_points)


def find_next_move(last_point):
    shortest_way = 1000
    next_index = 1000
    for i in range(0, len(all_points)):
        if distances[last_point][i] > 0 and not visited[i]:
            if distances[last_point][i] < shortest_way:
                shortest_way = distances[last_point][i]
                next_index = i
    visited[last_point] = True
    path.append(next_index)
    return next_index


def find_shortest_path(start_point):
    path.append(start_point)
    next_point = start_point
    for i in range(0, len(all_points) - 1):
        next_point = find_next_move(next_point)


find_shortest_path(0)
print("Résultat du plus proche voisin :", path)


def calc_dist_total(path):
    total = 0
    for i in range(0, len(path) - 1):
        total = total + distances[path[i]][path[i + 1]]
    return total


total = calc_dist_total(path)
print("La distance est égale à :", total, "Km")


# Algo 2-opt
def swap(list, i, j):
    list[i], list[j] = list[j], list[i]


def gain(path, i, j):
    if i < j:
        gain = distances[path[i]][path[j + 1]] + distances[path[(i + len(path) - 1) % len(path)]][path[j]] - \
               distances[path[(i + len(path) - 1) % len(path)]][path[i]] - distances[path[j]][path[(j + 1) % len(path)]]
    return gain


def algo_opt(path):
    for i in range(1, len(path)):
        for j in range(i + 1, len(path) - 1):
            swap(path, i, j)
            if gain(path, i, j) < 0:
                swap(path, i, j)
    return path


path2opt = path.copy()
algo_opt(path2opt)
print("Résultat 2-opt :", path2opt)
total = calc_dist_total(path2opt)
print("La distance est égale à :", total, "Km")

# Affichage
m = folium.Map([45.18486504179179, 5.731181509376984], zoom_start=14)

folium.Marker(
    location=[45.18486504179179, 5.731181509376984],
    tooltip="Le Campus Numérique",
    # popup="Le Campus Numérique",
    icon=folium.Icon(color="purple", icon=""),
).add_to(m)


def display_points(all_points):
    for i in range(0, len(all_points)):
        folium.Marker(
            location=[all_points[i][0], all_points[i][1]],
            tooltip=i,
            icon=folium.Icon(color="green", icon=""),
        ).add_to(m)


display_points(all_points)

path_coords = []
path2opt_coords = []


def display_path(path, path_coords):
    for i in range(0, len(path)):
        path_coords.append([all_points[path[i]][0], all_points[path[i]][1]])


display_path(path, path_coords)
# print(path_coords)
folium.PolyLine(path_coords, color="red", tooltip="shortest_path").add_to(m)

display_path(path2opt, path2opt_coords)
folium.PolyLine(path2opt_coords, color="orange", tooltip="shortest_path").add_to(m)

m.save("index.html")
