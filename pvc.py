import haversine as hs
import numpy as np
import folium

allPoints = [
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


def display_all_points():
    for point in allPoints:
        for coordinate in point:
            print(coordinate)


def calc_distance(pointA, pointB, all_points):
    loc1 = (all_points[pointA][0], all_points[pointA][1])
    loc2 = (all_points[pointB][0], all_points[pointB][1])
    result = hs.haversine(loc1, loc2)
    return result


print(calc_distance(0, 1, allPoints))

a = np.array([[1], [5], [9]])
print(a[1][0])


# def calc_all_distances(allPoints):
#     distances = np.array([[0], [1]])
#     for i in range(0, len(allPoints)):
#         # distances[i] = []
#         for j in range(i, len(allPoints)):
#             if i == j:
#                 distances[[i], [j]] = 0
#             else:
#                 distances[[i], [j]] = calc_distance(i, j, allPoints)
#             print(f"La distance entre les points {i} et {j} est égale à {distances[i][j]} km")

def calc_all_distances(allPoints):
    for i in range(0, len(allPoints)):
        for j in range(i, len(allPoints)):
            if i == j:
                result = 0
            else:
                result = calc_distance(i, j, allPoints)
                print(f"La distance entre les points {i} et {j} est égale à {result} km")


calc_all_distances(allPoints)

m = folium.Map(location=(45.171112, 5.695952))
m.save("index.html")