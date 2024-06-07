import math
class Beam():

    def __init__(self, width, height, fc, fy):
        self.width = width
        self.height = height
        self.fc = fc
        self.fy = fy

    def depth(self):
        depth = max(self.height-0.1*self.height, self.height-60)
        return depth
class BeamReinf(Beam):
    def __init__(self, width, height, fc, fy, diameter, moment):
        super().__init__(self, width, height, fc, fy)
        self.moment = moment
        self.diameter = diameter
    def calculate_a(self):
        if 17 <= self.fc <= 28:
            beta_1 = 0.85
        elif 28 < self.fc < 55:
            beta_1 = 0.85 - (0.05 * (self.fc - 28)) / 7
        else:
            beta_1 = 0.65

        a = self.depth() - math.sqrt(self.depth() ** 2 - (2 * abs(self.moment) * 10 ** 6) / (0.85 * self.fc * 0.9 * self.width))
        # if error, probably the moment inputted is too big, causing minus value inside the sqrt

        c_max = (0.003 / (0.003 + 0.005)) * self.depth()
        a_max = beta_1 * c_max

        return a, a_max, c_max




B1 = Beam(400, 700, 30, 420)

print(B1.depth())