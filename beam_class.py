import math


class Beam:

    def __init__(self, width, height, fc, fy):
        self.width = width
        self.height = height
        self.fc = fc
        self.fy = fy
        self.depth = max(self.height - 0.1 * self.height, self.height - 60)


class Rebar(Beam):
    def __init__(self, width, height, fc, fy, diameter, moment):
        super().__init__(width, height, fc, fy)
        self.moment = moment  # if for 1 beam you want to calc END & MID moment, must make list
        # maybe like self.moments = [MEndTop, MEndBot, MMidTop, MMidBot]
        # but then maybe must make a function to import from excel.
        # that's for later, make a function of rebar that return [EndTopAs, EndBotAs, MidTopAs, MidBot,As]
        self.diameter = diameter
        self.a, self.a_max, self.c_max = self.calculate_a()

    def calculate_a(self):
        if 17 <= self.fc <= 28:
            beta_1 = 0.85
        elif 28 < self.fc < 55:
            beta_1 = 0.85 - (0.05 * (self.fc - 28)) / 7
        else:
            beta_1 = 0.65

        # To avoid math domain error, ensure the value inside sqrt is non-negative

        d = self.depth
        sqrt_value = d ** 2 - (2 * abs(self.moment) * 10 ** 6) / (0.85 * self.fc * 0.9 * self.width)

        if sqrt_value < 0:
            raise ValueError("The moment inputted is too big, causing a negative value inside the sqrt")

        a = d - math.sqrt(sqrt_value)

        c_max = (0.003 / (0.003 + 0.005)) * d
        a_max = beta_1 * c_max

        return a, a_max, c_max

    def rebar(self):
        def rebar1():
            tensile_steel = abs(self.moment) * 10 ** 6 / (0.9 * self.fy * (self.depth - self.a / 2))
            compressive_steel = 0
            return tensile_steel, compressive_steel

        def rebar2():
            d = self.depth
            dc = self.height - d

            compressive_force = 0.85 * self.fc * self.width * self.a_max
            m_uc = (compressive_force * (d - self.a_max / 2) * 0.9) * 10 ** -6  # in kNm
            m_us = abs(self.moment) - m_uc  # in kNm
            print(f"Mus = Mu - Muc; Mus = {abs(self.moment)} - {m_uc}\nMus = {m_us} kNm\n")

            fs = 2 * 10 ** 5 * 0.003 * ((self.c_max - dc) / self.c_max)
            if fs > self.fy:
                fs = self.fy
            else:
                pass

            print(f"fs = {fs} MPa")

            compressive_steel = m_us * 10 ** 6 / ((fs - 0.85 * self.fc) * (d - dc))

            as_1 = m_uc * 10 ** 6 / (self.fy * (d - self.a_max / 2))
            as_2 = m_us * 10 ** 6 / (self.fy * (d - dc) * 0.9)

            tensile_steel = as_1 + as_2
            return tensile_steel, compressive_steel

        if self.a <= self.a_max:
            print(f"a <= a max; {self.a} <= {self.a_max}\n")
            tensile_steel, compressive_steel = rebar1()

        else:
            print(f"a > a_max; {self.a} > {self.a_max}\n")
            tensile_steel, compressive_steel = rebar2()

        return tensile_steel, compressive_steel

    def min_max_area(self):
        fc = self.fc
        fy = self.fy
        b = self.width
        d = self.depth

        min_rebar_area = max(0.25 * math.sqrt(fc) / fy * b * d, 1.4 / fy * b * d)
        print(f"min_rebar_area = {min_rebar_area} mm2")

        if fy <= 413.685:
            max_rebar_area = 0.025 * b * d
        elif fy > 551.581:
            max_rebar_area = 0.02 * b * d
        else:
            max_rebar_area = (0.025 - 0.05 * (fy - 413.685) / (551.581 - 413.685)) * b * d

        print(f"max_rebar_area = {max_rebar_area} mm2")
        return min_rebar_area, max_rebar_area
