import numpy as np
import matplotlib.pyplot as plt


def max_shear_along_span(shear_force_func, thickness_arr, root_base, span, span_num=101):
    span_arr = np.linspace(0, span, span_num)
    span_arr_interp_purpose = np.linspace(0, span, np.size(thickness_arr))
    max_shear_arr = np.zeros(np.shape(span_arr))
    adjust_height = 0.001  # m, adjust height to avoid singularity
    for ii in range(np.size(span_arr)):
        shear_force = shear_force_func(span_arr[ii])
        base = get_cc_base(root_base, span_arr[ii], span)
        if span_num == np.size(thickness_arr):
            height = thickness_arr[0][ii] + adjust_height
        else:
            height = np.interp(span_arr[ii], span_arr_interp_purpose, thickness_arr) + adjust_height
        cur_shear_arr = calc_rect_beam_shear(shear_force, base, height, height_num=101)
        max_shear_arr[ii] = max(abs(cur_shear_arr))
    return max_shear_arr, span_arr


def get_cc_base(root_base, span_location, max_span):
    root_chord = 1.40546  # m
    tip_chord = 1.12437  # m

    tip_base = (tip_chord / root_chord) * root_base
    base_slope = (tip_base - root_base) / max_span
    cur_base = root_base + base_slope * span_location
    return cur_base


def calc_rect_beam_shear(shear_force, base, height, height_num=101):
    half_height = height / 2
    shear_force /= 2  # upper and lower flanges have same dimensions
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
    import spar_thickness
    import min_Ixx

    af_file_path = "./Data/NLF-0414F-REFINED.dat"
    max_span = 6.325  # m
    num_span = 101

    # yield strengths from https://zoltek.com/products/px35/prepreg/
    yield_tensile = 1.850e9  # Pa
    yield_compress = 1.320e9  # Pa
    safety_factor = 1.5

    # Ixx at each section
    save = False
    plot_fig = False
    moment_func_multiple = [min_Ixx.moment_func_max_positive, min_Ixx.moment_func_max_negative]
    func_legends = ["Most positive moment", "Most negative moment"]
    Ixx_arr, span_arr = min_Ixx.get_Ixx_along_span(moment_func_multiple, func_legends, safety_factor,
                                                   yield_tensile, yield_compress, max_span, af_file_path,
                                                   num_span=num_span, plot_fig=plot_fig, save=save,
                                                   save_parent_path=None, save_type=".png")

    # thickness required
    spar_locations = [0.25, 0.75]  # ratio of local chord
    Ixx_aft_ratio = 0.25
    #rect_base = np.linspace(0.1, 0.4, 5)  # base length for rectangular cross sections
    rect_base = 0.1
    thickness_main = []
    thickness_aft = []
    required_main, required_aft = spar_thickness.spar_rectangular_cc_thickness(Ixx_arr[0], span_arr, spar_locations,
                                                                                   af_file_path,
                                                                                   Ixx_aft_ratio=Ixx_aft_ratio,
                                                                                   base=rect_base)
    thickness_main.append(required_main)
    thickness_aft.append(required_aft)

    #### from this script
    span = max_span
    root_base = 2  # m, remember to change

    # max positive
    shear_force_func = max_pos_shear
    thickness_arr = thickness_main
    max_pos_shear_arr, span_arr = max_shear_along_span(shear_force_func, thickness_arr,
                                                       root_base, span, span_num=num_span)

    # max negative
    shear_force_func = max_neg_shear
    max_neg_shear_arr, _ = max_shear_along_span(shear_force_func, thickness_arr,
                                                root_base, span, span_num=num_span)

    # plotting
    Pa_Mpa = 1 / 1e6
    plt.figure()
    plt.plot(span_arr, max_pos_shear_arr * Pa_Mpa, label="Max Positive Load")
    plt.plot(span_arr, max_neg_shear_arr * Pa_Mpa, label="Max Negative Load")
    plt.grid()
    plt.xlabel("Span (m)")
    plt.ylabel("Absolute Shear (MPa)")
    plt.title("Span Sectional Maximum Shear Stress")
    plt.legend(loc="best")
    plt.show()
