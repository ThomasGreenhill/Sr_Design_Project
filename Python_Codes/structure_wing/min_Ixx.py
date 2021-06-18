"""
Functions to find the minimum Ixx given the airfoil geometry

Note:
    1.Neutral axis of airfoil calculation is based on paper called
        "Area and Bending Inertia of Airfoil Sections".
        which is included in the reference in the group Google drive.

History:
    05.25.2021, Created, XT.
    05.26.2021, Checked, XT.
"""

import numpy as np
import sys
import math
import matplotlib.pyplot as plt

sys.path.append("../../Utilities")
import mses


def get_Ixx_along_span(moment_func_multiple, func_legends, safety_factor, yield_tensile, yield_compress, span,
                       af_file_path, num_span=101, plot_fig=True, save=True, save_parent_path=None, save_type=".png"):

    Ixx_arr_required = []
    span_arr = np.linspace(0, span, num_span)

    for num_func in range(np.size(moment_func_multiple)):
        moment_func = moment_func_multiple[num_func]
        Ixx_arr_new = find_Ixx_required(moment_func, safety_factor, yield_tensile, yield_compress,
                                         span, af_file_path, num_span=num_span)
        Ixx_arr_required.append(Ixx_arr_new)

    if plot_fig:
        if np.size(func_legends) is not np.size(moment_func_multiple):
            raise Exception("Please provide the same amount of func_legends as the moment_func_multiple")
        else:
            for num_func in range(np.size(moment_func_multiple)):
                if type(func_legends[num_func]) is not str:
                    raise TypeError("Elements in func_legends must be string")

        # line styles
        line_style_arr = ["solid", "dotted", "dashed", "dashdot", (0, (3, 5, 1, 5, 1, 5)), (0, (3, 1, 1, 1, 1, 1)),
                          (0, (3, 10, 1, 10, 1, 10))]

        plt.figure()
        for num_func in range(np.size(moment_func_multiple)):
            plt.plot(span_arr, 1e12 * Ixx_arr_required[num_func],
                     label=func_legends[num_func],
                     linestyle=line_style_arr[num_func+2])
        plt.grid()
        ttl = "Minimum required Ixx along span"
        plt.title(ttl)
        plt.xlabel("Span-wise location (m)")
        plt.ylabel("Minimum Ixx (mm^4)")
        plt.legend()
        plt.show()
        if save:
            if type(save_parent_path) is not str or save_parent_path is None:
                raise Exception("Please provide a valid save_parent_path for the saved figure")
            if type(save_type) is not str:
                raise TypeError("Type of variable 'save_type' must be a valid string")
            plt.savefig(str(save_parent_path) + "/" + ttl + save_type, dpi=300, bbox_inches='tight')

    return Ixx_arr_required, span_arr


def get_min_Ixx(moment_func, safety_factor, max_span, af_file_path, yield_tensile, yield_compress, num_span=101):
    """
    Finds the minimum Ixx through a combination of rought estimation and precise determination
    :param moment_func: function for moment calculate
    :param safety_factor: value for safety factor > 1
    :param max_span: maximum span-wise distance
    :param num_span: number of span-wise location of interest
    :param af_file_path: string, file path to airfoil
    :param yield_tensile: tensile yield strength
    :param yield_compress: compression yield strength
    :return: (m^4) minimum Ixx value
    """
    keep_going = True
    num_Ixx = 2
    Ixx_start = 1e-6
    Ixx_end = 1e-5

    # roughly find minimal Ixx
    print("Working on rough Ixx range estimation...")
    while keep_going:
        Ixx_arr = np.linspace(Ixx_start, Ixx_end, num_Ixx)

        top, bot = determine_yield(Ixx_arr, moment_func, safety_factor, max_span, af_file_path, yield_tensile,
                                   yield_compress)

        if top and bot:  # if bot arrays are not empty
            keep_going = False
        else:
            Ixx_start = Ixx_end
            Ixx_end *= 2

    # determine a more precise minimum Ixx
    print("Working on precise minimum Ixx estimation...")
    scaling_factor = 1001
    Ixx_num_precise = int(math.ceil(Ixx_end - Ixx_start) * scaling_factor)
    Ixx_arr_precise = np.linspace(Ixx_start, Ixx_end, Ixx_num_precise)
    top_precise, bot_precise = determine_yield(Ixx_arr_precise, moment_func, safety_factor, max_span, af_file_path,
                                               yield_tensile, yield_compress, num_span=num_span)

    if top_precise and bot_precise:  # both arrays are not empty
        Ixx_min_index = max([min(top_precise), min(bot_precise)])
        Ixx_min = Ixx_arr_precise[Ixx_min_index]
        print("The minimum Ixx is found to be {:.4e} m^4".format(Ixx_min))
    else:
        raise Exception("Unexpected Error: top_precise or bot_precise is still empty after rough estimation")

    return Ixx_min


def determine_yield(Ixx_arr, moment_func, safety_factor, max_span, af_file_path, yield_tensile, yield_compress, num_span=11):
    """
    Determine if yield occurs in a given range of Ixx
    :param Ixx_arr: array of Ixx
    :param moment_func: function for moment calculate
    :param safety_factor: value for safety factor > 1
    :param num_span: number of span-wise locations of interest
    :param max_span: maximum span-wise distance
    :param af_file_path: string, file path to airfoil
    :param yield_tensile: tensile yield strength
    :param yield_compress: compression yield strength
    :return: array of index for safe Ixx's on top and bottom
    """
    top_yield_arr = [False for ii in range(len(Ixx_arr))]
    bot_yield_arr = [False for ii in range(len(Ixx_arr))]

    for cur_index, Ixx in enumerate(Ixx_arr):
        sigma_top_arr, sigma_bot_arr = find_bending_stresses(moment_func, Ixx, max_span, af_file_path, num_span=101)
        max_sigma_top = max(abs(sigma_top_arr))
        max_sigma_bot = max(abs(sigma_bot_arr))
        sigma_top_sum = sum(sigma_top_arr)
        sigma_bot_sum = sum(sigma_bot_arr)

        # for top
        if sigma_top_sum >= 0:
            if max_sigma_top >= (yield_tensile / safety_factor):
                top_yield_arr[cur_index] = True
        else:
            if max_sigma_top >= (yield_compress / safety_factor):
                top_yield_arr[cur_index] = True

        # for bottom
        if sigma_bot_sum >= 0:
            if max_sigma_bot >= (yield_tensile / safety_factor):
                bot_yield_arr[cur_index] = True
        else:
            if max_sigma_bot >= (yield_compress / safety_factor):
                bot_yield_arr[cur_index] = True

    # Ixx determination
    top_safe_index = [ii for ii, material_yield in enumerate(top_yield_arr) if not material_yield]
    bot_safe_index = [ii for ii, material_yield in enumerate(bot_yield_arr) if not material_yield]

    return top_safe_index, bot_safe_index


def find_bending_stresses(moment_func, Ixx, span, af_file_path, num_span=101):
    """
    Finds the bending stresses at the top most and bottom most points given the airfoil geometry
    :param moment_func: function to calculate moment along span
    :param Ixx: (m^4) area moment of inertia along x axis
    :param span: (m) maximum span
    :param af_file_path: string, path to airfoil file
    :param num_span: number of points of interest along span
    :return: sectional top normal stresses (Pa), sectional bot normal stresses (Pa)
    """
    span_locations = np.linspace(0, span, num_span)
    moment_arr = np.array(moment_func(span_locations))
    chord_length_arr, _ = np.array(NLF_0414_F_airfoil_chord_thickness(span_locations))

    # wing airfoil sections (base case)
    x_num = 1001
    x_loc_arr = np.linspace(0, 1, x_num)
    x_geom, z_geom = mses.ReadXfoilGeometry(af_file_path)
    z_up_arr, z_lo_arr = np.array(mses.MsesInterp(x_loc_arr, x_geom, z_geom))
    cc_area_base = np.trapz((z_up_arr - z_lo_arr), x_loc_arr)
    z_up_max = max(z_up_arr)
    z_lo_min = min(z_lo_arr)

    # neutral axis for each section
    z_bar_arr = 0.5 * cc_area_base * chord_length_arr * np.trapz((z_up_arr ** 2 - z_lo_arr ** 2), x_loc_arr)

    # locations from neutral axis
    z_top_arr = np.array(chord_length_arr * z_up_max - z_bar_arr)
    z_bot_arr = np.array(z_bar_arr - chord_length_arr * z_lo_min)

    # evaluate stresses at each section
    sigma_top_arr = moment_arr * z_top_arr / Ixx
    sigma_bot_arr = moment_arr * z_bot_arr / Ixx

    return sigma_top_arr, sigma_bot_arr


def find_Ixx_required(moment_func, safety_factor, yield_tensile, yield_compress, span, af_file_path, num_span=101):
    """

    :param moment_func: function to calculate moment along span
    :param safety_factor: factor of safety
    :param yield_tensile: (Pa) tensile yield strength
    :param yield_compress: (Pa) compressive yield strength
    :param span: (m) maximum span-wise distance for half wing
    :param num_span: number of points along span
    :param af_file_path: file path to airfoil data
    :return: array of minimum Ixx required along section
    """
    span_locations = np.linspace(0, span, num_span)
    moment_arr = np.array(moment_func(span_locations))
    chord_length_arr, _ = np.array(NLF_0414_F_airfoil_chord_thickness(span_locations))

    # wing airfoil sections (base case)
    x_num = 1001
    x_loc_arr = np.linspace(0, 1, x_num)
    x_geom, z_geom = mses.ReadXfoilGeometry(af_file_path)
    z_up_arr, z_lo_arr = np.array(mses.MsesInterp(x_loc_arr, x_geom, z_geom))
    cc_area_base = np.trapz((z_up_arr - z_lo_arr), x_loc_arr)
    z_up_max = max(z_up_arr)
    z_lo_min = min(z_lo_arr)

    # neutral axis for each section
    z_bar_arr = 0.5 * cc_area_base * chord_length_arr * np.trapz((z_up_arr ** 2 - z_lo_arr ** 2), x_loc_arr)

    # locations from neutral axis
    z_top_arr = np.array(chord_length_arr * z_up_max - z_bar_arr)
    z_bot_arr = np.array(z_bar_arr - chord_length_arr * z_lo_min)

    # evaluate Ixx at each section
    Ixx_arr = np.zeros(np.shape(span_locations))
    for ii in range(len(Ixx_arr)):
        if moment_arr[ii] >= 0:  # top is tension, bot is compression
            yield_top = yield_tensile / safety_factor
            yield_bot = yield_compress / safety_factor
        else:  # top is compression, bot is tension
            yield_top = yield_compress / safety_factor
            yield_bot = yield_tensile / safety_factor
        Ixx_top = abs(moment_arr[ii] * z_top_arr[ii] / yield_top)
        Ixx_bot = abs(moment_arr[ii] * z_bot_arr[ii] / yield_bot)
        Ixx_arr[ii] = max([Ixx_top, Ixx_bot])

    return Ixx_arr


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


def moment_func_max_positive(location):
    """
    Calculate max positive moment at a given span-wise location based on curve fit
    :param location: (m) span-wise location
    :return: (Nm) resulting moment, adjusted for coordinate system
    """
    coeff_arr = [0.8148, -2.98, 3.5367, -2.098e3, 2.256e4, -63133.86387]
    max_power = len(coeff_arr) - 1
    moment = 0

    for power, coeff in enumerate(coeff_arr):
        cur_power = max_power - power
        moment += coeff * location ** cur_power

    return moment


def moment_func_max_negative(location):
    """
    Calculate max negative moment at a given span-wise location based on curve fit
    :param location: (m) span-wise location
    :return: (Nm) resulting moment, adjusted for coordinate system
    """
    coeff_arr = [-0.424, 0.752, 40.6, 401.8, -7.3e3, 22913.54387]
    max_power = len(coeff_arr) - 1
    moment = 0

    for power, coeff in enumerate(coeff_arr):
        cur_power = max_power - power
        moment += coeff * location ** cur_power

    return moment


if __name__ == '__main__':
    max_span = 6.325  # m

    # yield strengths from https://zoltek.com/products/px35/prepreg/
    yield_tensile = 1.850e9  # Pa
    yield_compress = 1.320e9  # Pa
    af_file_path = "./Data/NLF-0414F-REFINED.dat"
    safety_factor = 1.5

    # most positive moment
    print("For most positive moment:")
    moment_func = moment_func_max_positive
    get_min_Ixx(moment_func, safety_factor, max_span, af_file_path, yield_tensile, yield_compress)

    # most negative moment
    print("\n")
    print("For most negative moment")
    moment_func = moment_func_max_negative
    get_min_Ixx(moment_func, safety_factor, max_span, af_file_path, yield_tensile, yield_compress)


    ######
    # Ixx at each section
    save = False
    moment_func_multiple = [moment_func_max_positive, moment_func_max_negative]
    func_legends = ["Most positive moment", "Most negative moment"]
    Ixx_arr_pos, span_arr_pos = get_Ixx_along_span(moment_func_multiple, func_legends, safety_factor, yield_tensile, yield_compress,
                                           max_span, af_file_path, num_span=101, plot_fig=True, save=save,
                                           save_parent_path=None, save_type=".png")
