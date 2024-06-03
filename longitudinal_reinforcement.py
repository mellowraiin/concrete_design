"""
calculating longitudinal reinforcement of beam (moment only, torsion excluded)
"""
import math
import beam_calcs as beam

h = 700  # b & h in mm
b = 400

fc = 30  # fc in MPa
fy = 420  # fy in MPa
dc = 60  # dc in mm
d = h - dc

ultimate_moment = -530.38  # kNm

"""check a_max"""

a, a_max, c_max = beam.calculate_a(b, d, fc, ultimate_moment)
print(f"a = {a}")
print(f"a_max = {a_max}")

"""
calculating the rebar required
"""


if a <= a_max:
    print(f"a <= a max; {a} <= {a_max}\n")
    tensile_steel, compressive_steel = beam.rebar1(ultimate_moment, fy, d, a)

else:
    print(f"a > a_max; {a} > {a_max}\n")
    tensile_steel, compressive_steel = beam.rebar2(a_max, c_max, b, fc, fy, d, dc, ultimate_moment)

min_rebar_area, max_rebar_area = beam.min_max_area(fc, b, d, fy)

tensile_steel = beam.steel_result(tensile_steel, min_rebar_area, max_rebar_area)
compressive_steel = beam.steel_result(compressive_steel, min_rebar_area, max_rebar_area)

print(f"As = {tensile_steel} mm2, {round(tensile_steel/(b*h)*100, 2)} %")
print(f"As' = {compressive_steel} mm2, {round(compressive_steel/(b*h)*100, 2)} %")


diameter_list = {10 : 0.25*math.pi*10**2,
                 13 : 0.25*math.pi*13**2,
                 16 : 0.25*math.pi*16**2,
                 19 : 0.25*math.pi*19**2,
                 22 : 0.25*math.pi*22**2,
                 25 : 0.25*math.pi*25**2,
                 29 : 0.25*math.pi*29**2,
                 32 : 0.25*math.pi*32**2}
diameter = 10
print(f"diameter = {diameter}")
rebar_area = diameter_list.get(diameter)


(diameter, rebar_area, actual_tensile_count,
 actual_compressive_count, max_count_per_layer) = beam.iterate_diameter(diameter, rebar_area, tensile_steel,
                                                                   compressive_steel, b, diameter_list)

print(f"\ndiameter_use = {diameter}")
print(f"rebar_area = {rebar_area}")
print(f"actual_tensile_count = {actual_tensile_count}")
print(f"actual_compressive_count = {actual_compressive_count}")
print(f"max_count_per_layer = {max_count_per_layer}\n")

percent_tensile = round(actual_tensile_count*rebar_area/(b*h)*100,2)
percent_compressive = round(actual_compressive_count*rebar_area/(b*h)*100,2)

print(f"tensile reinforcement = {actual_tensile_count}D{diameter}, {percent_tensile}%")
print(f"compressive reinforcement = {actual_compressive_count}D{diameter}, {percent_compressive}%")

beam.a_function()
print("this this work also?")
print("what is this")