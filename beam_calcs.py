import math


def calculate_a(b, d, fc, ultimate_moment):
    if 17 <= fc <= 28:
        beta_1 = 0.85
    elif 28 < fc < 55:
        beta_1 = 0.85 - (0.05 * (fc - 28)) / 7
    else:
        beta_1 = 0.65

    a = d - math.sqrt(d ** 2 - (2 * abs(ultimate_moment) * 10 ** 6) / (0.85 * fc * 0.9 * b))
    # if error, probably the moment inputted is too big, causing minus value inside the sqrt

    c_max = (0.003 / (0.003 + 0.005)) * d
    a_max = beta_1 * c_max

    return a, a_max, c_max


def rebar1(ultimate_moment, fy, d, a):
    tensile_steel = abs(ultimate_moment) * 10 ** 6 / (0.9 * fy * (d - a / 2))
    compressive_steel = tensile_steel / 2
    return tensile_steel, compressive_steel


def rebar2(a_max, c_max, b, fc, fy, d, dc, ultimate_moment):
    compressive_force = 0.85 * fc * b * a_max
    m_uc = (compressive_force * (d - a_max / 2) * 0.9) * 10 ** -6  # in kNm
    m_us = abs(ultimate_moment) - m_uc  # in kNm
    print(f"Mus = Mu - Muc; Mus = {abs(ultimate_moment)} - {m_uc}\nMus = {m_us} kNm\n")

    fs = 2 * 10 ** 5 * 0.003 * ((c_max - dc) / c_max)
    if fs > fy:
        fs = fy
    else:
        pass

    print(f"fs = {fs} MPa")

    compressive_steel = m_us * 10 ** 6 / ((fs - 0.85 * fc) * (d - dc))

    as_1 = m_uc * 10 ** 6 / (fy * (d - a_max / 2))
    as_2 = m_us * 10 ** 6 / (fy * (d - dc) * 0.9)

    tensile_steel = as_1 + as_2
    return tensile_steel, compressive_steel


def min_max_area(fc, b, d, fy):
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


def steel_result(steel_required, min_rebar_area, max_rebar_area):
    if steel_required <= min_rebar_area:
        steel_required = min_rebar_area
    elif steel_required >= max_rebar_area:
        print("\n***\nMaximum steel exceeded, increase the size of the beam\n***\n".upper())
    return steel_required


def round_rebar(rebar_count):
    if rebar_count <= math.floor(rebar_count) + 0.1:
        rebar_count = math.floor(rebar_count)
    else:
        rebar_count = math.ceil(rebar_count)

    return rebar_count


def iterate_diameter(diameter, rebar_area, tensile_steel, compressive_steel, b, diameter_list):
    while True:
        tensile_rebar_count = tensile_steel / rebar_area
        actual_tensile_count = round_rebar(tensile_rebar_count)

        compressive_rebar_count = compressive_steel / rebar_area
        actual_compressive_count = round_rebar(compressive_rebar_count)

        max_count_per_layer = math.floor((b - 60 + 40) / (40 + diameter))

        if max(actual_tensile_count, actual_compressive_count) > max_count_per_layer * 2:
            index_current_diameter = list(diameter_list).index(diameter)
            index_next_diameter = index_current_diameter + 1
            next_diameter = list(diameter_list)[index_next_diameter]
            diameter = next_diameter
            rebar_area = diameter_list.get(diameter)

            if diameter >= 32:
                print("Reached the maximum diameter size")
                break
        else:
            break
    return diameter, rebar_area, actual_tensile_count, actual_compressive_count, max_count_per_layer
