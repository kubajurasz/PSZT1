import random, cv2
import numpy as np
from PIL import Image, ImageDraw


class City:

    def __init__(self, id, name, x, y):
        self.id = id
        self.name = name
        self.x = x
        self.y = y


class Evolution:

    def __init__(self, cities):
        self.cities = cities
        self.specimen_1 = Specimen(1, 74)
        self.specimen_2 = Specimen(1, 74)
        self.map = []
        self.map_size = 74

    def evolve(self):
        quality_1 = 999
        quality_2 = 999
        counter_1 = 0
        counter_2 = 0
        random.seed(None)
        eliminated = random.randint(0, 73)
        self.specimen_1.hospitals[eliminated] = 0

        quality_1 = self.specimen_1.check_quality(self.cities)

        if quality_1 == 999:
            self.replace_specimen(self.specimen_1, 1)
        else:
            self.replace_specimen(self.specimen_2, 2)

        while counter_1 < 500 and counter_2 < 500:
            quality_1 = self.specimen_1.check_quality(self.cities)
            quality_2 = self.specimen_2.check_quality(self.cities)

            if random.randint(1, 8) == 1:
                print("mutacja")
                if quality_1 < quality_2:
                    self.mutation(self.specimen_1, 1)
                    counter_1 = counter_1 + 1
                    counter_2 = 0
                else:
                    self.mutation(self.specimen_2, 2)
                    counter_1 = 0
                    counter_2 = counter_2 + 1
                continue

            print("rep")
            if quality_1 < quality_2:
                self.replace_specimen(self.specimen_1, 1)
                counter_1 = counter_1 + 1
                counter_2 = 0
            else:
                self.replace_specimen(self.specimen_2, 2)
                counter_1 = 0
                counter_2 = counter_2 + 1

            print("counter_1 :", counter_1, "counter_2 :", counter_2, "Q1: ", quality_1, "Q2:", quality_2)

        if counter_1 == 500:
            return self.specimen_1
        else:
            return self.specimen_2

    def replace_specimen(self, specimen, num):
        found = 0
        random.seed(None)
        while found == 0:
            eliminated = random.randint(0, 73)
            if specimen.hospitals[eliminated] == 1:
                found = 1

        if num == 1:
            self.specimen_2.hospitals = specimen.hospitals.copy()
            self.specimen_2.hospitals[eliminated] = 0
            self.specimen_2.size = specimen.size - 1

        else:
            self.specimen_1.hospitals = specimen.hospitals.copy()
            self.specimen_1.hospitals[eliminated] = 0
            self.specimen_1.size = specimen.size - 1

    def mutation(self, specimen, num):
        found = 0
        random.seed(None)

        while found == 0:
            eliminated = random.randint(0, 73)
            if specimen.hospitals[eliminated] == 1:
                found = 1

        found = 0

        while found == 0:
            added = random.randint(0, 73)
            if specimen.hospitals[added] == 0:
                found = 1

        if num == 1:
            self.specimen_2.hospitals = specimen.hospitals.copy()
            self.specimen_2.hospitals[eliminated] = 0
            self.specimen_2.hospitals[added] = 1

        else:
            self.specimen_1.hospitals = specimen.hospitals.copy()
            self.specimen_1.hospitals[eliminated] = 0
            self.specimen_1.hospitals[added] = 1


class Specimen:
    def __init__(self, generation, size):
        self.generation = generation + 1
        self.size = size
        self.hospitals = []
        for i in range(74):
            self.hospitals.append(1)

    def check_quality(self, cities):
        img_x = Image.open('map2.png')
        draw = ImageDraw.Draw(img_x)
        score = 0

        test = Image.open('map1.png')
        testdraw = ImageDraw.Draw(test)

        for i in range(len(cities)):
            if self.hospitals[i] == 1:
                draw.ellipse((cities[i].x - 187, cities[i].y - 187, cities[i].x + 187, cities[i].y + 187),
                             fill=(0, 0, 255))
                testdraw.ellipse((cities[i].x - 187, cities[i].y - 187, cities[i].x + 187, cities[i].y + 187),
                                 outline=(0, 0, 100, 100))

        # img_x.show()
        img_x.save('imageCheck.png', 'PNG')
        test.save('test.png', 'PNG')

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


def check_map(cities, specimen, r):
    img2 = Image.open('map2.png')
    draw = ImageDraw.Draw(img2)

    for i in range(len(cities)):
        if specimen[i] == 1:
            draw.ellipse((cities[i].x - r, cities[i].y - r, cities[i].x + r, cities[i].y + r),
                         fill=(0, 0, 255))

    img2.show()
    img2.save('image1.png', 'PNG')

    return True if open("image1.png", "rb").read() == open("image2.png", "rb").read() else False


def paint_map(cities_with_hospitals, r):
    img1 = Image.open('map1.png')

    draw1 = ImageDraw.Draw(img1)

    for i in cities_with_hospitals:
        draw1.ellipse((i.x - r, i.y - r, i.x + r, i.y + r), outline=(0, 0, 100, 100))

    img1.show()


def main():
    cities = Cities()
    cities.load_cities("data2.csv")

    cities_with_hospitals = []

    evolution = Evolution(cities.cities)
    winner = evolution.evolve()

    for i in range(len(winner.hospitals)):
        if winner.hospitals[i] == 1:
            cities_with_hospitals.append(cities.cities[i])

    for i in range(len(cities_with_hospitals)):
        print(cities_with_hospitals[i].name)


if __name__ == '__main__':
    main()
