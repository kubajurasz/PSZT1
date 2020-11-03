import random
from PIL import Image, ImageDraw


class City:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y


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
    specimen = []
    for i in range(len(cities.cities)):
        specimen.append(random.randint(1, 1))
    paint_map(cities.cities, 1)
    print(check_map(cities.cities, specimen, 100))


if __name__ == '__main__':
    main()
