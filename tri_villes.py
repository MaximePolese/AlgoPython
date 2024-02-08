from tkinter import *
from tkinter import filedialog
import csv
import haversine as hs


class Ville:
    def __init__(self, nom_commune, codes_postaux, latitude, longitude, dist, distanceFromGrenoble):
        self.nom_commune = nom_commune
        self.codes_postaux = codes_postaux
        self.latitude = latitude
        self.longitude = longitude
        self.dist = dist
        self.distanceFromGrenoble = distanceFromGrenoble


def loadFile():
    listVille.clear()
    filename = filedialog.askopenfilename(initialdir="./",
                                          title="Selection du Fichier",
                                          filetypes=(("Text files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))
    changeLabelFile("Fichier : " + filename)
    with open(filename, 'r', encoding='UTF-8') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # skip header line
        for row in csvreader:
            data = row[0].split(";")
            try:
                ville = Ville(data[8], data[9], float(data[11]), float(data[12]), float(data[13]), 0)
                ville.distanceFromGrenoble = getDistanceFromGrenoble(ville)
                listVille.append(ville)
            except:
                continue


def getDistanceFromGrenoble(ville):
    loc1 = (45.166667, 5.716667)
    loc2 = (ville.latitude, ville.longitude)
    result = hs.haversine(loc1, loc2)
    return result


def isLess(listVille, i, j):
    return getDistanceFromGrenoble(listVille[i]) < getDistanceFromGrenoble(listVille[j])


def swap(listVille, i, j):
    listVille[i], listVille[j] = listVille[j], listVille[i]


def changeLabelFile(text):
    labelFileExplorer = Label(fenetre,
                              text=text,
                              width=120, height=4,
                              fg="black", background="#579BB1")
    labelFileExplorer.place(x=150, y=offset + 40)


def changeLabelButtonSubmit(text):
    buttonValidation['text'] = text
    buttonValidation.place(x=150, y=offset + 120)


def onSelectTypeTri(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        global typeTriSelection
        typeTriSelection = data
        changeLabelButtonSubmit("Lancement du {}".format(data))


def sort():
    # effacement de la liste affichée
    listVilleSortedBox.delete(0, END)
    listVilleSorted = listVille.copy()

    if typeTriSelection == "Tri par insertion":
        listVilleSorted = insertsort(listVilleSorted)
    elif typeTriSelection == "Tri par sélection":
        listVilleSorted = selectionsort(listVilleSorted)
    elif typeTriSelection == "Tri à bulles":
        listVilleSorted = bubblesort(listVilleSorted)
    elif typeTriSelection == "Tri de Shell":
        listVilleSorted = shellsort(listVilleSorted)
    elif typeTriSelection == "Tri par fusion":
        listVilleSorted = mergesort(listVilleSorted)
    elif typeTriSelection == "Tri par tas":
        listVilleSorted = heapsort(listVilleSorted)
    elif typeTriSelection == "Tri rapide":
        listVilleSorted = quicksort(listVilleSorted)

    for ville in range(len(listVilleSorted)):
        listVilleSortedBox.insert(END, listVilleSorted[ville].nom_commune + " - " + str(
            listVilleSorted[ville].distanceFromGrenoble))
        listVilleSortedBox.itemconfig(ville, fg="black")

    listVilleSortedBox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listVilleSortedBox.yview)


def insertsort(listVille):
    for i in range(1, len(listVille)):
        temp = listVille[i]
        j = int(i)
        while j > 0 and listVille[j - 1].distanceFromGrenoble > temp.distanceFromGrenoble:
            listVille[j] = listVille[j - 1]
            j = j - 1
        listVille[j] = temp
    return listVille


def selectionsort(listVille):
    for i in range(0, len(listVille)):
        index_min = i
        for j in range(i + 1, len(listVille)):
            if listVille[j].distanceFromGrenoble < listVille[index_min].distanceFromGrenoble:
                index_min = j
        swap(listVille, i, index_min)
    return listVille


def bubblesort(listVille):
    passage = 0
    permut = True
    while permut:
        permut = False
        for i in range(0, (len(listVille) - 1 - passage)):
            if listVille[i].distanceFromGrenoble > listVille[i + 1].distanceFromGrenoble:
                swap(listVille, i, (i + 1))
                permut = True
        passage = passage + 1
    return listVille


def shellsort(listVille):
    e = 0
    while e < (len(listVille) / 3):
        e = (3 * e + 1)
    while e != 0:
        for i in range(e, len(listVille)):
            temp = listVille[i]
            j = i
            while (j > e - 1) and (listVille[j - e].distanceFromGrenoble > temp.distanceFromGrenoble):
                listVille[j] = listVille[j - e]
                j = j - e
            listVille[j] = temp
        e = int(((e - 1) / 3))
    return listVille


def mergesort(listVille):
    if len(listVille) > 1:
        half_list = len(listVille) // 2
        list_begin = listVille[0: half_list]
        list_end = listVille[half_list: len(listVille)]
        mergesort(list_begin)
        mergesort(list_end)
        i = j = k = 0
        while i < len(list_begin) and j < len(list_end):
            if list_begin[i].distanceFromGrenoble < list_end[j].distanceFromGrenoble:
                listVille[k] = list_begin[i]
                i += 1
            else:
                listVille[k] = list_end[j]
                j += 1
            k += 1
        while i < len(list_begin):
            listVille[k] = list_begin[i]
            i += 1
            k += 1
        while j < len(list_end):
            listVille[k] = list_end[j]
            j += 1
            k += 1
    return listVille


def heapsort(listVille):
    print("implement me !")
    return listVille


def quicksort(listVille):
    print("implement me !")
    return listVille


# Creation de la fenêtre
fenetre = Tk()
width = 1000
height = 180
offset = 10
listVille = []
listTri = ["Tri par insertion",
           "Tri par sélection",
           "Tri à bulles",
           "Tri de Shell",
           "Tri par fusion",
           "Tri par tas",
           "Tri rapide"]

typeTriSelection = "Tri par insertion"

labelFileExplorer = Label()
canvas = Canvas(fenetre, width=width + 2 * offset,
                height=height + 2 * offset, bg='white')
buttonValidation = Button(command=sort)

list = Listbox(fenetre, width=20, height=len(listTri), selectmode="single")
list.place(x=offset, y=offset)
list.bind("<<ListboxSelect>>", onSelectTypeTri)

for typeTri in range(len(listTri)):
    list.insert(END, listTri[typeTri])
    list.itemconfig(typeTri, fg="black")

buttonFile = Button(
    fenetre, text="Importation du fichier", command=loadFile)
buttonFile.place(x=150, y=offset)

changeLabelButtonSubmit("Lancement du {}".format(typeTriSelection))

changeLabelFile("Aucun Fichier ...")

canvas.pack()

listVilleSortedBox = Listbox(
    fenetre, width=100, height=25, selectmode="single")
listVilleSortedBox.pack(side=LEFT, fill=BOTH)

scrollbar = Scrollbar(fenetre, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=BOTH)
fenetre.mainloop()
