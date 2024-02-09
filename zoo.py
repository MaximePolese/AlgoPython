class Animal:
    def __init__(self, poids, taille):
        self.__poids = poids
        self.taille = taille

    def se_deplacer(self):
        pass

    @property
    def poids(self):
        return self.__poids

    @poids.setter
    def poids(self, poids):
        try:
            if poids < 0:
                raise ValueError("Le poids doit être un nombre positif.")
            self.__poids = poids
        except ValueError as e:
            print("Erreur :", e)

    def __str__(self):
        return f"Animal: poids = {self.__poids}, taille = {self.taille}"


class Serpent(Animal):
    def se_deplacer(self):
        print("je rampe")


class Oiseau(Animal):
    def __init__(self, poids, taille, altitude_max):
        super().__init__(poids, taille)
        self.altitude_max = altitude_max

    def se_deplacer(self):
        print("je vole")

    # def __str__(self):
    #     return f"Oiseau: poids = {self.__poids}, taille = {self.taille}, altitude_max = {self.altitude_max}"


class Zoo:
    def __init__(self, animal_list=[Animal]):
        self.animal_list = animal_list

    def add_animal(self, animal):
        self.animal_list.append(animal)

    def __add__(self, other):
        new_animal_list = self.animal_list + other.animal_list
        return Zoo(new_animal_list)

    def display_animal_list(self):
        for animal in self.animal_list:
            print(animal)

    def __str__(self):
        return f"Zoo: animal_list = {self.animal_list}"


mon_animal = Animal(200, 2)
print(mon_animal.poids, mon_animal.taille)
print(mon_animal)

mon_animal.poids = -50
print("nouveau poids : ", mon_animal.poids)

mon_serpent = Serpent(5, 3)
print(mon_serpent)
mon_serpent.se_deplacer()

mon_oiseau = Oiseau(1, 1.8, 10000)
print(mon_oiseau)
mon_oiseau.se_deplacer()
print(mon_oiseau.altitude_max)

list1 = [mon_animal, mon_serpent, mon_oiseau]
my_zoo = Zoo(list1)
serpent2 = Serpent(500, 51)
my_zoo.add_animal(serpent2)
print(my_zoo)
my_zoo.display_animal_list()

zoo1 = Zoo([mon_animal, mon_serpent])
zoo2 = Zoo([mon_oiseau])
zoos = zoo1 + zoo2
print(zoos)
