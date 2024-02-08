import random
import time

list_size = 5000
list1 = [random.randint(0, list_size * 2) for _ in range(list_size)]


def swap(list, i, j):
    list[i], list[j] = list[j], list[i]


def tri_selection(list):
    count = 0
    print("\033[1;32mtri_selection", list)
    for i in range(0, len(list)):
        index_min = i
        for j in range(i + 1, len(list)):
            if list[j] < list[index_min]:
                index_min = j
                count = count + 1
        swap(list, i, index_min)
    print("Compteur : ", count)
    return list


def tri_bulle(list):
    count = 0
    print("tri_bulle", list)
    passage = 0
    permut = True
    while permut:
        permut = False
        for i in range(0, (len(list) - 1 - passage)):
            if list[i] > list[i + 1]:
                swap(list, i, (i + 1))
                count = count + 1
                permut = True
        passage = passage + 1
    print("Compteur : ", count)
    return list


def tri_insertion(list):
    count = 0
    print("tri_insertion", list)
    for i in range(1, len(list)):
        temp = list[i]
        j = i
        while j > 0 and list[j - 1] > temp:
            list[j] = list[j - 1]
            j = j - 1
            count = count + 1
        list[j] = temp
    print("Compteur : ", count)
    return list


def tri_shell(list):
    count = 0
    print("tri_shell", list)
    e = 0
    while e < (len(list) / 3):
        e = (3 * e + 1)
    while e != 0:
        for i in range(e, len(list)):
            temp = list[i]
            j = i
            while (j > e - 1) and (list[j - e] > temp):
                list[j] = list[j - e]
                j = j - e
                count = count + 1
            list[j] = temp
        e = int(((e - 1) / 3))
    print("Compteur : ", count)
    return list


def tri_merge(list):
    if len(list) > 1:
        half_list = len(list) // 2
        list_begin = list[0: half_list]
        list_end = list[half_list: len(list)]
        tri_merge(list_begin)
        tri_merge(list_end)
        i = j = k = 0
        while i < len(list_begin) and j < len(list_end):
            if list_begin[i] < list_end[j]:
                list[k] = list_begin[i]
                i += 1
            else:
                list[k] = list_end[j]
                j += 1
            k += 1
        while i < len(list_begin):
            list[k] = list_begin[i]
            i += 1
            k += 1
        while j < len(list_end):
            list[k] = list_end[j]
            j += 1
            k += 1
    # print(list)
    return list


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
        if list[i] <= list[pivot]:
            swap(list, i, mur)
            mur += 1
    swap(list, last, mur)
    return mur


def chrono(tri, list):
    start_time = time.time()
    mon_tri = tri(list)
    end_time = time.time()
    print("Temps d'éxécution : ", (end_time - start_time))
    print("Liste triée : ", mon_tri)
    print()


chrono(tri_selection, list1.copy())
chrono(tri_bulle, list1.copy())
chrono(tri_insertion, list1.copy())
chrono(tri_shell, list1.copy())

print("tri_merge", list1.copy())
chrono(tri_merge, list1.copy())

list2 = list1.copy()
print("tri_quick", list2)
start_time = time.time()
tri_quick(list2, 0, len(list2) - 1)
end_time = time.time()
print("Temps d'éxécution : ", (end_time - start_time))
print("Liste triée : ", list2)
