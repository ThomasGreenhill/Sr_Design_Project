import sys
import copy
import numpy
import matplotlib.pyplot as plt

sys.path.append("../../Python_Codes")
import Class130


def empannage_sizing(vol_h, vol_v, x_h, x_v, Wing):
    # return S_h, S_v
    """
    Sizes the tail areas based on the wing area, volumes, and moment arms

    Input:
            vol_h: horizontal stabilizer volume coefficient (According to Roskan)
            vol_v: vertical tail volume coefficient (According to Roskam)
            x_h: (m) horizontal stabilizer moment arm
            x_v: (m) vertical tail moment arm
            Wing: Needs area, span, c_bar

    Output:
            S_hs: (m^2) horizontal stabilizer area estimate
            S_vs: (m^2) vertical tail area estimate
    """
    wing = copy.deepcopy(Wing)
    S_h = vol_h * wing.area * wing.c_bar / x_h
    S_v = vol_v * wing.area * wing.span / x_v

    return S_h, S_v


if __name__ == '__main__':
    # Parameters        # v1.5, 03.05.2021
    vol_h = 0.655
    vol_v = 0.0425
    area = 8 * 2
    span = 6.325
    c_bar = 1.265
    c_root_w = 1.405
    c_root_h = 1.049
    c_root_v = 1.110
    # Locations
    x_w_front = 2.8
    x_h_front = 7.75
    x_v_front = 7.75

    wing = Class130.Wing(area=area, span=span, c_bar=c_bar)
    factor = 1 / 4  # assume aerodynamic center at quarter root chord
    x_loc_wing = x_w_front + c_root_w * factor
    x_loc_h = x_h_front + c_root_h * factor
    x_loc_v = x_v_front + c_root_v * factor
    x_h = x_loc_h - x_loc_wing
    x_v = x_loc_v - x_loc_wing

    S_h, S_v = empannage_sizing(vol_h, vol_v, x_h, x_v, wing)
    print("Based on the current design:")
    print("The moment arms: x_h = {:.2f} m, x_v = {:.2f} m".format(x_h, x_v))
    print("S_h: {:.4f} m^2, each is {:.4f} m^2".format(S_h, S_h / 2))
    print("S_v: {:.4f} m^2".format(S_v))

    # Empennage sizing plots
    num = 101
    x_arr = numpy.linspace(3, 8, num)
    S_h_arr = numpy.zeros(num)
    S_v_arr = numpy.zeros(num)
    for i in range(num):
        S_h_arr[i], S_v_arr[i] = empannage_sizing(vol_h, vol_v, x_arr[i], x_arr[i], wing)

    plt.figure()
    plt.title("Empennage Sizes versus. Moment Arm length")
    plt.grid()
    plt.plot(x_arr, S_h_arr / 2, 'r-', label='Horizontal Tail (One-sided)')
    plt.plot(x_arr, S_v_arr, 'b-', label='Vertical Tail')
    plt.xlabel('Moment Arm from Wing Root Quarter Chord (m)')
    plt.ylabel('Platform Area Estimation')
    plt.legend()
    plt.show()
