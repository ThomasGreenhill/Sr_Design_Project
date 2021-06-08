import numpy as np
import matplotlib.pyplot as plt


def max_shear_along_span(shear_force_func, root_base, root_height, span, span_num=101):
    span_arr = np.linspace(0, span, span_num)
    max_shear_arr = np.zeros(np.shape(span_arr))
    for ii in range(np.size(span_arr)):
        shear_force = shear_force_func(span_arr[ii])
        base, height = get_cc_base_height(root_base, root_height, span_arr[ii], span)
        cur_shear_arr = calc_rect_beam_shear(shear_force, base, height, height_num=101)
        max_shear_arr[ii] = max(abs(cur_shear_arr))
    return max_shear_arr, span_arr


def get_cc_base_height(root_base, root_height, span_location, max_span):
    root_chord = 1.5  # remember to change
    tip_chord = 1.2  # remember to change

    tip_base = (tip_chord / root_chord) * root_base
    tip_height = (tip_chord / root_chord) * root_height
    base_slope = (tip_base - root_base) / max_span
    height_slope = (tip_height - root_height) / max_span
    cur_base = root_base + base_slope * span_location
    cur_height = root_height + height_slope * span_location
    return cur_base, cur_height


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
    span = 6.28  # m, remember to change
    root_base = 2  # m, remember to change
    root_height = 1  # m, remember to change

    # max positive
    shear_force_func = max_pos_shear
    max_pos_shear_arr, span_arr = max_shear_along_span(shear_force_func,
                                                       root_base, root_height, span, span_num=201)

    # max negative
    shear_force_func = max_neg_shear
    max_neg_shear_arr, _ = max_shear_along_span(shear_force_func,
                                                root_base, root_height, span, span_num=201)

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
