import random
from PIL import Image, ImageDraw
import time
import operator


class City:

    def __init__(self, id, name, x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y


class Evolution:

    def __init__(self, cities, population_size):
        self.cities = cities
        self.population = [Specimen(len(cities)) for i in range(population_size)]

    def rank_population(self, r):
        for i in self.population:
            i.check_quality(self.cities, r)
            self.population.sort(key=operator.attrgetter('quality'))

    def evolve(self, number_of_generations, r):
        self.rank_population(r)
        for i in range(number_of_generations):
            for j in self.population:
                j.mutation()
            self.rank_population(r)
        return self.population[0]


class Specimen:
    def __init__(self, size):
        self.size = size
        self.quality = 999
        self.hospitals = [random.randint(0, 1) for i in range(size)]

    def check_quality(self, cities, r):
        img_x = Image.open('map4.png')
        draw = ImageDraw.Draw(img_x)
        score = 0

        for i in range(len(cities)):
            if self.hospitals[i] == 1:
                draw.ellipse((cities[i].x - r, cities[i].y - r, cities[i].x + r, cities[i].y + r),
                             fill=(0, 0, 255))

        img_x.save('imageCheck.png', 'PNG')

        if open("imageCheck.png", "rb").read() == open("imageCheck3.png", "rb").read():
            for i in range(len(self.hospitals)):
                if self.hospitals[i] == 1:
                    score += 1
            self.quality = score
        else:
            self.quality = 999
        print(self.quality)

    def mutation(self):
        mutating_gene = random.randint(0, 73)
        self.hospitals[mutating_gene] = (self.hospitals[mutating_gene] + 1) % 2


class Cities:

    def __init__(self):
        self.cities = []

    def load_cities(self, file):
        data = []
        x = 0
        with open(file) as file:
            for line in file:
                temp = line.strip().split(",")
                data.append(temp)
        for i, j, k in data:
            self.cities.append(City(x, i, int(j), int(k)))
            x += 1


def paint_map(cities_with_hospitals, r):
    img1 = Image.open('map1.png')

    draw1 = ImageDraw.Draw(img1)

    for i in cities_with_hospitals:
        draw1.ellipse((i.x - r, i.y - r, i.x + r, i.y + r), outline=(0, 0, 100, 100))

    img1.show()


def main():
    cities = Cities()
    cities.load_cities("data.csv")
    start_time = time.time()
    cities_with_hospitals = []

    evolution = Evolution(cities.cities, 20)
    winner = evolution.evolve(5, 187)

    for i in range(len(winner.hospitals)):
        if winner.hospitals[i] == 1:
            cities_with_hospitals.append(cities.cities[i])

    paint_map(cities_with_hospitals, 187)

    for i in range(len(cities_with_hospitals)):
        print(cities_with_hospitals[i].name)

    print(len(cities_with_hospitals))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
