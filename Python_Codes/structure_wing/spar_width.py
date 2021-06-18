import numpy as np
import sys
import math
import matplotlib.pyplot as plt

sys.path.append("../../Utilities")
import mses
import min_Ixx
from scipy.optimize import fsolve


def find_flange_width_fixed_height(Ixx_arr, span_arr, height_const, spar_location, af_file_path):
    # Assuming rectangular cross sections
    Ixx_arr = np.transpose(Ixx_arr)
    base_arr = np.zeros(np.shape(Ixx_arr))
    for ii in range(np.size(Ixx_arr)):
        z_bar, top_distance, bot_distance = find_neutral_axis(af_file_path, span_arr[ii], spar_location)
        front_term = (1 / 6) * height_const**3 + height_const * (top_distance**2 + bot_distance**2)
        base_arr[ii] = Ixx_arr[ii] / front_term

    return base_arr


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


if __name__ == '__main__':
    import min_Ixx

    # main height
    height_start = 5  # mm, single spar thickness
    height_end = 7  # mm
    height_num = 5
    height_adjust = 1e-3
    height_const_main_arr = np.linspace(height_start * height_adjust, height_end * height_adjust, height_num)

    # aft height
    height_start = 2  # mm
    height_end = 4  # mm
    height_num = 5
    height_adjust = 1e-3
    height_const_aft_arr = np.linspace(height_start * height_adjust, height_end * height_adjust, height_num)

    # Ixx calculation
    max_span = 6.325  # m

    # yield strengths from https://zoltek.com/products/px35/prepreg/
    yield_tensile = 1.850e9  # Pa
    yield_compress = 1.320e9  # Pa
    af_file_path = "./Data/NLF-0414F-REFINED.dat"
    safety_factor = 1.5

    # Ixx at each section
    save = False
    moment_func_multiple = [min_Ixx.moment_func_max_positive]
    func_legends = ["Most positive moment"]

    Ixx_arr, span_arr = min_Ixx.get_Ixx_along_span(moment_func_multiple, func_legends, safety_factor,
                                                   yield_tensile,
                                                   yield_compress,
                                                   max_span, af_file_path, num_span=101, plot_fig=False,
                                                   save=save,
                                                   save_parent_path=None, save_type=".png")

    base_arr_main = []
    base_arr_aft = []
    main_ratio = 1  # 100% Ixx carried by main spar
    aft_ratio = 0.25  # 25% Ixx carried by aft spar
    spar_main = 0.25  # 25% chord-wise location
    spar_aft = 0.75  # 75% chord-wise location
    for ii in range(np.size(height_const_main_arr)):
        height_const = height_const_main_arr[ii]
        Ixx_main_arr = [item * main_ratio for item in Ixx_arr]
        base_arr_main_new = find_flange_width_fixed_height(Ixx_main_arr, span_arr, height_const, spar_main, af_file_path)
        base_arr_main.append(base_arr_main_new)
    for ii in range(np.size(height_const_aft_arr)):
        height_const = height_const_aft_arr[ii]
        Ixx_aft_arr = [item * aft_ratio for item in Ixx_arr]
        base_arr_aft_new = find_flange_width_fixed_height(Ixx_aft_arr, span_arr, height_const, spar_aft, af_file_path)
        base_arr_aft.append(base_arr_aft_new)

    # line styles
    line_style_arr = ["solid", "dotted", "dashed", "dashdot", (0, (3, 5, 1, 5, 1, 5)), (0, (3, 1, 1, 1, 1, 1)),
                      (0, (3, 10, 1, 10, 1, 10))]

    # Plot, main
    plt.figure()
    for ii in range(np.size(height_const_main_arr)):
        plt.plot(span_arr, base_arr_main[ii] * 1e3,
                 label="Fixed Single Flange Thickness of {:.2f} mm".format(height_const_main_arr[ii] * 1e3),
                 linestyle=line_style_arr[ii])
    plt.title("Width Distribution of Main Spar along Span")
    plt.xlabel("Span-wise Location (m)")
    plt.ylabel("Required Width (mm)")
    plt.legend(loc="best")
    plt.grid()
    plt.show()

    # Plot, aft
    plt.figure()
    for ii in range(np.size(height_const_aft_arr)):
        plt.plot(span_arr, base_arr_aft[ii] * 1e3,
                 label="Fixed Single Flange Thickness of {:.2f} mm".format(height_const_aft_arr[ii] * 1e3),
                 linestyle=line_style_arr[ii])
    plt.title("Width Distribution of Aft Spar along Span")
    plt.xlabel("Span-wise Location (m)")
    plt.ylabel("Required Width (mm)")
    plt.legend(loc="best")
    plt.grid()
    plt.show()