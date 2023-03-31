import random


class CircleTarget:

    def __init__(self, radius, vanishTime):
        self.radius = radius
        self.vanishTime = vanishTime
        self.xPos = 0
        self.yPos = 0

    def set_radius(self, newRadius):
        self.radius = newRadius

    def get_radius(self):
        return self.radius

    def set_vanish_time(self, newTime):
        self.vanishTime = newTime

    def get_vanish_time(self):
        return self.vanishTime

    def gen_coordinates(self, width, height):
        self.xPos = random.randrange(self.radius, width - self.radius)
        self.yPos = random.randrange(self.radius, height - self.radius)

    def get_coordinates(self):
        return self.xPos, self.yPos
