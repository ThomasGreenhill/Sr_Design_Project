import numpy as np
import sys
import math
import matplotlib.pyplot as plt

sys.path.append("../../Utilities")
import mses
import min_Ixx
from scipy.optimize import fsolve


def spar_rectangular_cc_thickness(Ixx_arr, span_arr, spar_locations, af_file_path, base=0.15):
    """
    Calculates the sectional required spar thickness (4 total)
    :param Ixx_arr: Ixx array from previous calculation
    :param span_arr: span-wise array corresponding to Ixx array
    :param spar_locations: locations denoted by ratio of chord for spars
    :param af_file_path: path to airfoil file
    :param base: base of the rectangular cc (assume all 4 spars have same cc), base is based on root chord, will adjust
    :return: an array of required single spar thickness (4 in total), (m)
    """
    # span wise locations
    chord_arr, _ = NLF_0414_F_airfoil_chord_thickness(span_arr)
    root_chord, _ = NLF_0414_F_airfoil_chord_thickness(span_arr[0])

    # wing airfoil sections (base case)
    x_num = 1001
    x_loc_arr = np.linspace(0, 1, x_num)
    x_geom, z_geom = mses.ReadXfoilGeometry(af_file_path)
    z_up_arr, z_lo_arr = np.array(mses.MsesInterp(x_loc_arr, x_geom, z_geom))

    cc_area_base = np.trapz((z_up_arr - z_lo_arr), x_loc_arr)

    # neutral axis for each section
    z_bar_arr = 0.5 * cc_area_base * chord_arr * np.trapz((z_up_arr ** 2 - z_lo_arr ** 2), x_loc_arr)

    # height for each spar
    z_up_loc = np.zeros(np.shape(spar_locations))
    z_lo_loc = np.zeros(np.shape(spar_locations))
    for ii, spar in enumerate(spar_locations):
        z_up_loc[ii] = z_up_arr[int(x_num * spar)]
        z_lo_loc[ii] = z_lo_arr[int(x_num * spar)]

    z_up_along_span = []
    z_lo_along_span = []
    for ii in range(np.size(spar_locations)):
        height_up = z_up_loc[ii] * chord_arr
        height_lo = z_lo_loc[ii] * chord_arr
        z_up_along_span.append(height_up - z_bar_arr)
        z_lo_along_span.append(height_lo - z_bar_arr)

    # Solving for thicknesses of square cc
    thickness_required = np.zeros(np.shape(span_arr))
    for span_section in range(np.size(span_arr)):
        distance = 0
        for spar in range(np.size(spar_locations)):
            distance = distance + z_up_along_span[spar][span_section] ** 2 + z_lo_along_span[spar][span_section] ** 2
        cubic_coeffs = [base * chord_arr[span_section] / root_chord / 3, 0, distance, -Ixx_arr[span_section]]
        cubic_func = lambda x: cubic_coeffs[0] * x**3 + cubic_coeffs[1] * x**2 + cubic_coeffs[2] * x + cubic_coeffs[3]
        thickness_required[span_section] = fsolve(cubic_func, 1)

    return thickness_required

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


if __name__ == "__main__":
    spar_locations = [0.25, 0.75]  # ratio of local chord
    af_file_path = "./Data/NLF-0414F-REFINED.dat"
    max_span = 6.325  # m

    # yield strengths from https://zoltek.com/products/px35/prepreg/
    yield_tensile = 1.850e9  # Pa
    yield_compress = 1.320e9  # Pa
    safety_factor = 1.5

    # Ixx at each section
    save = False
    plot_fig = False
    num_span = 11
    moment_func_multiple = [min_Ixx.moment_func_max_positive, min_Ixx.moment_func_max_negative]
    func_legends = ["Most positive moment", "Most negative moment"]
    Ixx_arr, span_arr = min_Ixx.get_Ixx_along_span(moment_func_multiple, func_legends, safety_factor,
                                                           yield_tensile, yield_compress, max_span, af_file_path,
                                                           num_span=num_span, plot_fig=plot_fig, save=save,
                                                           save_parent_path=None, save_type=".png")

    rect_base = np.linspace(0.1, 0.4, 5)  # base length for rectangular cross sections
    print(rect_base)
    thickness_arr = []
    for rr in range(np.size(rect_base)):
        thickness_required = spar_rectangular_cc_thickness(Ixx_arr[0], span_arr, spar_locations, af_file_path,
                                                       base=rect_base[rr])
        thickness_arr.append(thickness_required)

    # plot
    plt.figure()
    for rr in range(np.size(rect_base)):
        plt.plot(span_arr, thickness_arr[rr] * 1e3, label="Base of {:.0f} mm".format(rect_base[rr] * 1e3))
    plt.title("Thickness of a single spar (4 in total) required along span")
    plt.xlabel("Span-wise location (m)")
    plt.ylabel("Minimum thickness required (mm)")
    plt.grid()
    plt.legend()
    plt.show()