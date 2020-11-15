import random
from PIL import Image, ImageDraw
import time
import operator


class City:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


class Evolution:

    def __init__(self, cities, population_size):
        self.cities = cities
        self.population = [Specimen(len(cities), [random.choices([0, 1], [0.7, 0.3])[0] for i in range(len(cities))]) for i in range(population_size)]
        self.next_generation = []

    def rank_population(self, r):
        for i in self.population:
            i.check_quality(self.cities, r)
        self.population.sort(key=operator.attrgetter('quality'))

    def evolve(self, number_of_generations, r):
        self.rank_population(r)
        for i in range(number_of_generations):
            self.next_generation = []
            for _ in range(10):
                self.next_generation += self.population[random.randint(0, 9)].cross(self.population[random.randint(0, 9)])

            for x in self.next_generation:
                x.mutation_2()
                x.check_quality(self.cities, r)
                # x.mutation(1/74)

            self.next_generation.sort(key=operator.attrgetter('quality'))
            self.population = self.population[0:10] + self.next_generation[0:10]
            self.rank_population(r)

            print("---------------new top 7---------------")
            for x in range(7):
                print(self.population[x].quality)

        return self.population[0]


class Specimen:
    def __init__(self, size, hospitals):
        self.size = size
        self.quality = 999
        self.hospitals = hospitals

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

    def mutation(self, p):
        for i in self.hospitals:
            if random.random() > p:
                i = (i + 1) % 2

    def mutation_2(self):
        mutating_gene = random.randint(0, 73)
        while self.hospitals[mutating_gene] == 0:
            mutating_gene = random.randint(0, 73)
        self.hospitals[mutating_gene] = (self.hospitals[mutating_gene] + 1) % 2

    def cross(self, other):
        where = random.randint(0, 73)
        gene1 = self.hospitals[where:] + other.hospitals[:where]
        gene2 = other.hospitals[where:] + self.hospitals[:where]
        return [Specimen(self.size, gene1), Specimen(self.size, gene2)]


class Cities:

    def __init__(self):
        self.cities = []

    def load_cities(self, file):
        data = []
        with open(file) as file:
            for line in file:
                temp = line.strip().split(",")
                data.append(temp)
        for i, j, k in data:
            self.cities.append(City(i, int(j), int(k)))


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
    winner = evolution.evolve(100, 187)

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
