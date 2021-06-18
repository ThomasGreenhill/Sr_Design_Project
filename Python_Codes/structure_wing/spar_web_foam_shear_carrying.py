import numpy as np
import sys
import math
import matplotlib.pyplot as plt

sys.path.append("../../Utilities")
import mses
import min_Ixx
from scipy.optimize import fsolve


def find_rect_web_base_required(shear_func, base, spar_loc, max_span, af_file_path, num_span=101):
    span_arr = np.linspace(0, max_span, num_span)
    shear_arr = np.zeros(np.shape(span_arr))
    height_arr = np.zeros(np.shape(span_arr))
    tau_arr = np.zeros(np.shape(span_arr))
    for ii in range(np.size(span_arr)):
        shear_arr[ii] = shear_func(span_arr[ii])
        z_bar, top_distance, bot_distance = find_neutral_axis(af_file_path, span_arr[ii], spar_loc)
        height_top = z_bar + top_distance
        height_bot = z_bar - bot_distance
        height_arr[ii] = height_top + height_bot
        tau_arr[ii] = max(abs(calc_rect_beam_shear(shear_arr[ii], base, height_arr[ii])))

    return tau_arr, span_arr


def find_neutral_axis(af_file_path, span_location, spar_chordwise_loc):
    # wing airfoil sections (base case)
    x_num = 1001
    x_loc_arr = np.linspace(0, 1, x_num)
    x_geom, z_geom = mses.ReadXfoilGeometry(af_file_path)
    z_up_arr, z_lo_arr = np.array(mses.MsesInterp(x_loc_arr, x_geom, z_geom))

    cc_area_base = np.trapz((z_up_arr - z_lo_arr), x_loc_arr)

    # neutral axis for each section
    sectional_chord, _ = NLF_0414_F_airfoil_chord_thickness(span_location)
    z_up_arr *= sectional_chord
    z_lo_arr *= sectional_chord
    z_bar = 0.5 * cc_area_base * sectional_chord * np.trapz((z_up_arr ** 2 - z_lo_arr ** 2), x_loc_arr)

    # top and bottom airfoil distance
    spar_loc_index_up = int(spar_chordwise_loc * np.size(z_up_arr))
    spar_loc_index_lo = int(spar_chordwise_loc * np.size(z_lo_arr))
    top_distance = z_up_arr[spar_loc_index_up] - z_bar
    bot_distance = z_bar - z_lo_arr[spar_loc_index_lo]

    return z_bar, top_distance, bot_distance


def NLF_0414_F_airfoil_chord_thickness(span_loc):
    """
    Calculates the sectional chord and thickness using linear interpolation
    :param span_loc: (m) span-wise location
    :return: sectional chord length (m), sectional thickness (m)
    """
    root_chord = 1.40546
    tip_chord = 1.12437
    max_span = 6.325
    t_c_ratio = 0.14166
    # if span_loc < 0 or span_loc > max_span:
    #    raise Exception("Span has to be from 0 to {:.3f} m".format(max_span))
    cur_chord = span_loc / max_span * (tip_chord - root_chord) + root_chord
    airfoil_thickness = t_c_ratio * cur_chord

    return cur_chord, airfoil_thickness


def calc_rect_beam_shear(shear_force, base, height, height_num=101):
    half_height = height / 2
    height_arr = np.linspace(-half_height, half_height, height_num)
    shear_arr = np.zeros(np.shape(height_arr))
    Ixx = rect_Ixx(height, base)
    for ii in range(np.size(height_arr)):
        Q = rect_static_moment_of_area(base, half_height, height_arr[ii])
        shear_arr[ii] = calc_shear_rect(shear_force, Q, Ixx, base)
    return shear_arr


def calc_shear_rect(shear_force, Q, Ixx, base):
    tau = shear_force * Q / Ixx / base
    return tau


def rect_Ixx(height, base):
    return (1 / 12) * base * height ** 3


def rect_static_moment_of_area(base, half_height, target_height):
    Q_at_target = (base / 2) * (half_height ** 2 - target_height ** 2)
    return Q_at_target



#### loading functions
def max_pos_shear(y):
    coeff_arr = [4.074, -11.92, 10.61, -4.196e3, 2.256e4]
    max_power = np.size(coeff_arr) - 1
    shear = 0

    for ii, coeff in enumerate(coeff_arr):
        power = max_power - ii
        shear += coeff * y ** power

    return shear


def max_neg_shear(y):
    coeff_arr = [-2.12, 3.008, 121.8, 803.6, -7.3e3]
    max_power = np.size(coeff_arr) - 1
    shear = 0

    for ii, coeff in enumerate(coeff_arr):
        power = max_power - ii
        shear += coeff * y ** power

    return shear

if __name__ == '__main__':
    max_span = 6.325  # m
    af_file_path = "./Data/NLF-0414F-REFINED.dat"
    tensile_strength = 1.6  # MPa, tensile strength of foam
    safety_factor = 1.5
    tensile_strength_plot = [(tensile_strength / 2 / safety_factor), (tensile_strength / 2 / safety_factor)]

    # use maximum positive shear (biggest magnitude)
    shear_func = max_pos_shear
    spar_loc = 0.25  # assuming main spar carries everything

    base_start = 1000  # mm
    base_end = 1500  # mm
    base_num = 4
    convert_factor = 1e-3
    base_arr = np.linspace(base_start * convert_factor, base_end * convert_factor, base_num)

    tau_arr = []
    span_arr = []
    for ii in range(np.size(base_arr)):
        base = base_arr[ii]
        tau_arr_current, span_arr_cur = find_rect_web_base_required(shear_func, base, spar_loc, max_span, af_file_path, num_span=101)
        tau_arr.append(tau_arr_current)
        span_arr.append(span_arr_cur)

    # line styles
    line_style_arr = ["solid", "dotted", "dashed", "dashdot", (0, (3, 5, 1, 5, 1, 5)), (0, (3, 1, 1, 1, 1, 1)),
                      (0, (3, 10, 1, 10, 1, 10))]

    # plots
    Pa_MPa = 1e6
    span_plot = [0, max_span]
    plt.figure()
    for ii in range(np.size(base_arr)):
        plt.plot(span_arr[ii], tau_arr[ii] / Pa_MPa,
                 label="Web Base of {:.2f} mm".format(base_arr[ii] / convert_factor),
                 linestyle= line_style_arr[ii])

    plt.plot(span_plot, tensile_strength_plot, label="Max Allowed, SF = {:.1f}".format(safety_factor))
    plt.grid()
    plt.title("Maximum Shear in Web Along Span")
    plt.xlabel("Span-wise location (m)")
    plt.ylabel("Maximum Shear Stress (MPa)")
    plt.legend(loc="best")
    plt.show()