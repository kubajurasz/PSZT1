import random
import time
import operator
from PIL import Image, ImageDraw
import xlsxwriter


class City:

    def __init__(self, id, name, x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y


class Evolution:

    def __init__(self, cities, population, rounds, delete_cities, mutate):
        self.cities = cities
        self.mutate = mutate
        self.delete_cities = delete_cities
        self.rounds = rounds
        self.population = population
        self.specimens = []

        for i in range(population):
            self.specimens.append(Specimen(0, 99, 0, self.delete_cities))

    def evolve(self):
        random.seed(None)
        winner_counter = -1
        duel = [0, 1]
        winner = -1

        while winner_counter < self.rounds:
            duel[0] = random.randint(0, self.population - 1)
            wrong = 1
            while wrong == 1:
                duel[1] = random.randint(0, self.population - 1)
                if duel[0] != duel[1]:
                    wrong = 0

            if self.specimens[duel[0]].quality == self.specimens[duel[1]].quality == 999:
                continue
            quality_1 = self.specimens[duel[0]].check_quality(self.cities)
            quality_2 = self.specimens[duel[1]].check_quality(self.cities)

            if random.randint(1, self.mutate) == 1:
              #  print("mutacja")
                if quality_1 < quality_2:
                    self.mutation(duel[0], duel[1])
                    self.specimens[duel[0]].counter = self.specimens[duel[0]].counter + 1
                    self.specimens[duel[1]].counter = 0
                    winner_counter = self.specimens[duel[0]].counter
                    winner = duel[0]
                else:
                    self.mutation(duel[1], duel[0])
                    self.specimens[duel[1]].counter = self.specimens[duel[1]].counter + 1
                    self.specimens[duel[0]].counter = 0
                    winner_counter = self.specimens[duel[1]].counter
                    winner = duel[1]
                continue

           # print("rep")
            if quality_1 < quality_2:
                self.replace_specimen(duel[0], duel[1])
                self.specimens[duel[0]].counter = self.specimens[duel[0]].counter + 1
                self.specimens[duel[1]].counter = 0
                winner_counter = self.specimens[duel[0]].counter
                winner = duel[0]
            else:
                self.replace_specimen(duel[1], duel[0])
                self.specimens[duel[1]].counter = self.specimens[duel[1]].counter + 1
                self.specimens[duel[0]].counter = 0
                winner_counter = self.specimens[duel[1]].counter
                winner = duel[1]

        return self.specimens[winner]

    def replace_specimen(self, winner, looser):
        found = 0
        random.seed(None)
        while found == 0:
            eliminated = random.randint(0, 73)
            if self.specimens[winner].hospitals[eliminated] == 1:
                found = 1

        self.specimens[looser].hospitals = self.specimens[winner].hospitals.copy()
        self.specimens[looser].hospitals[eliminated] = 0
        self.specimens[looser].quality = self.specimens[looser].check_quality(self.cities)

    def mutation(self, winner, looser):
        found = 0
        random.seed(None)

        while found == 0:
            eliminated = random.randint(0, 73)
            if self.specimens[winner].hospitals[eliminated] == 1:
                found = 1

        found = 0

        while found == 0:
            added = random.randint(0, 73)
            if self.specimens[winner].hospitals[added] == 0:
                found = 1

        self.specimens[looser].hospitals = self.specimens[winner].hospitals.copy()
        self.specimens[looser].hospitals[eliminated] = 0
        self.specimens[looser].hospitals[added] = 0
        self.specimens[looser].quality = self.specimens[looser].check_quality(self.cities)


class Specimen:
    def __init__(self, generation, quality, counter, delete_cities):
        self.generation = generation + 1
        self.hospitals = []
        self.quality = quality
        self.counter = counter
        self.delete_cities = delete_cities

        for i in range(74):
            self.hospitals.append(1)

        for i in range(self.delete_cities):
            self.hospitals[random.randint(0, 73)] = 0

    def check_quality(self, cities):
        img_x = Image.open('map2.png')
        draw = ImageDraw.Draw(img_x)
        score = 0

        for i in range(len(cities)):
            if self.hospitals[i] == 1:
                draw.ellipse((cities[i].x - 187, cities[i].y - 187, cities[i].x + 187, cities[i].y + 187),
                             fill=(0, 0, 255))

        img_x.save('imageCheck.png', 'PNG')

        if open("imageCheck.png", "rb").read() == open("image2.png", "rb").read():
            for i in range(len(self.hospitals)):
                if self.hospitals[i] == 1:
                    score = score + 1
            return score
        else:
            return 999


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
            x = x + 1


def main():
    id = 1
    cities = Cities()
    cities.load_cities("data2.csv")
    cities_with_hospitals = []

    # evolution = Evolution(cities.cities, 30, 500)
    # winner = evolution.evolve()

    # for i in range(len(winner.hospitals)):
    #     if winner.hospitals[i] == 1:
    #         cities_with_hospitals.append(cities.cities[i])
    # print("****************************************")
    # for i in range(len(cities_with_hospitals)):
    #     print(cities_with_hospitals[i].name)
    #
    # print("W sumie: ", len(cities_with_hospitals))
    workbook = xlsxwriter.Workbook('Scores2.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'ID')
    worksheet.write(0, 1, 'Wynik')
    worksheet.write(0, 2, 'Czas (s)')
    worksheet.write(0, 3, 'Populacja')
    worksheet.write(0, 4, 'Zasięg')

    for i in range(300):
        counter = random.randint(50, 500)
        start_time = time.time()
        population = random.randint(2, 30)
        mutate = random.randint(2, 20)
        delete_cities = random.randint(5, 60)
        evolution = Evolution(cities.cities, population, counter, delete_cities,
                              mutate)
        winner = evolution.evolve()
        for i in range(len(winner.hospitals)):
            if winner.hospitals[i] == 1:
                cities_with_hospitals.append(cities.cities[i])
        worksheet.write(id, 0, id)
        worksheet.write(id, 1, len(cities_with_hospitals))
        worksheet.write(id, 2, time.time() - start_time)
        worksheet.write(id, 3, population)
        worksheet.write(id, 4, counter)
        id = id+1
        cities_with_hospitals.clear()

    workbook.close()


if __name__ == '__main__':
    main()
