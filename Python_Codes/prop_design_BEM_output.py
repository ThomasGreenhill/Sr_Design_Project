import numpy as np
import math
from prop_design_TVG import prop_design
from Class130 import AtmData, Propeller
from scipy import interpolate
import matplotlib.pyplot as plt


# History: 02.14.2021: Created by XT using climb design conditions 02.15.2021: Modified by TVG using cruise design
# conditions for cross-checking against project 2 results. Passed check 02.28.2021: Modified by TVG to refelect
# changes in prop_design_TVG.py


# Check script
def m0_fn(Ma):
    if Ma <= 0.9:
        return (2 * math.pi) / np.sqrt(1 - Ma ** 2)
    else:
        return (2 * math.pi) / np.sqrt(1 - 0.9 ** 2)


def Cd_fn(Cl):
    return 0.0095 + 0.0040 * (Cl - 0.2) ** 2


def vec_to_str(vec):
    # generate a one line string for a vector
    str_out = ""
    for ii in range(len(vec)):
        str_out = str_out + "{:.8f}".format(vec[ii])
        if ii < len(vec) - 1:
            str_out += ", "
        else:
            str_out += "\n"
    return str_out


def reduce_point(vec_list, numPoint=50):
    """
    :param vec_list: (array-like) list of vectors to be reduced by interpolation, all based on the first element of list
    :param numPoint: (int) number of points intended for the final output
    :return: vec_list_out: (array-like) list of reduced vectors
    """
    # input examination
    if vec_list is None:
        raise Exception("vec_list input failed")
    length = np.size(vec_list[0])
    if np.size(vec_list) > 1:
        for ii in range(1, len(vec_list)):
            if length != np.size(vec_list[ii]):
                raise Exception("vec_list elements have different dimensions")

    # interpolation
    x_new = np.linspace(vec_list[0][0], vec_list[0][-1], numPoint)
    vec_list_out = [x_new]
    if np.size(vec_list) > 1:
        for ii in range(1, len(vec_list)):
            tck = interpolate.splrep(vec_list[0], vec_list[ii], s=0)
            vec_new = interpolate.splev(x_new, tck, der=0)
            vec_list_out.append(vec_new)

    return vec_list_out


def write_col_vec(vec_list, file):
    """
    Writes multiple vectors in column form line by line
    :param vec_list: (array-like) list of vectors
    :param file: file pointer to store
    :return: None
    """
    if type(vec_list) is not list and type(vec_list) is not tuple:
        raise TypeError("1st parameter must be a list of tuple")

    length = np.size(vec_list[0])
    for num in range(len(vec_list)):
        if np.size(vec_list[num]) != length:
            raise ValueError("Sizes of vectors in 1st parameter do not match")

    for row in range(length):
        cur_line_vec = []
        for col in range(len(vec_list)):
            cur_line_vec.append(vec_list[col][row])

        file.write(vec_to_str(cur_line_vec))

    return


# Variable pitch analysis
# Design a propeller
diameter = 1.78
radius = diameter / 2
LD = 15  # Assumed
is_SI = True

# 3 Blades
numB = 3

# Design condition
T_req = 13000 / 8 * 1.2 * 0.601  # N (TOGW/(L/D))
Cl = 0.4
alp0 = np.radians(-2)

v_design = 30
atm = AtmData(v_design, 0, is_SI)
atm.expand(1.4, 287)

Design_RPM = 3000

prop = Propeller(radius, numB, Design_RPM, eta_P=0, CP=0, CT=0, CQ=0, Cl=Cl)
output = prop_design(atm, prop, T_req, m0_fn, Cd_fn, num=401)
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = output

# Point reduction and interpolation

# Adjustment
num_len = len(prop.bet)
beta_75_index = int(num_len * 0.75)
x = np.linspace(0, 1, num_len)
x_need = x[x >= 0.15]
c_need = prop.chord[x >= 0.15]
AF = 10 ** 5 / 16 * np.trapz(c_need / diameter * x_need ** 3, x_need)  # activity factor
CL_design = 4 * np.trapz(Cl * x_need ** 3, x_need)
print('====================== Propeller Design Parameters ======================')
print("Beta angle at 75% is {:.5f} degree".format(np.rad2deg(prop.bet[beta_75_index])))
print("Activity factor is {:.2f}, which corresponds to {:.2f} in openVSP (Source checked)".format(AF, AF * 2))
print("CL_design is {:.2f}".format(CL_design))

# Essential parameters
chord_R = prop.chord / radius
twist = np.rad2deg(prop.bet)

# point reduction
numPoint = 101
vec_in = [x, chord_R, twist]
x_reduced, chord_R, twist = reduce_point(vec_in, numPoint=numPoint)
x_reduced = abs(x_reduced)
chord_R = abs(chord_R)

# Other parameters needed to write file
feather_angle = 0  # rad, feather angle
pre_cone_angle = 0  # rad, pre-cone angle
center = (0.8, 1.3, -0.15)  # center location
normal = (-1.0, 0.0, 0.0)  # normal vector

rake = np.zeros(np.shape(x_reduced))
skew = np.zeros(np.shape(x_reduced))
sweep = np.zeros(np.shape(x_reduced))
t_c = np.zeros(np.shape(x_reduced))
axial = np.zeros(np.shape(x_reduced))
tangential = np.zeros(np.shape(x_reduced))
CLi = CL_design * np.ones(np.shape(x_reduced))

# Combining into one single list
vec_list_to_print = [x_reduced, chord_R, twist, rake, skew, sweep, t_c, CLi, axial, tangential]

# Write to file
parent_path = "../OpenVSP_X/v2.1/BEM Files/"
file_name = "prop_design.bem"
file_path = parent_path + file_name
mode = "w"
with open(file_path, mode) as file:
    file.write("...BEM Propeller...\n")
    file.write("Num_Sections: {}\n".format(numPoint))
    file.write("Num_Blades: {}\n".format(numB))
    file.write("Diameter: {:.8f}\n".format(diameter))
    file.write("Beta 3/4 (deg): {:.8f}\n".format(np.rad2deg(prop.bet[beta_75_index])))
    file.write("Feather (deg): {:.8f}\n".format(np.rad2deg(feather_angle)))
    file.write("Pre_Cone (deg): {:.8f}\n".format(np.rad2deg(pre_cone_angle)))
    file.write("Center: {:.8f}, {:.8f}, {:.8f}\n".format(center[0], center[1], center[2]))
    file.write("Normal: {:.8f}, {:.8f}, {:.8f}\n".format(normal[0], normal[1], normal[2]))
    file.write("\n")
    file.write("Radius/R, Chord/R, Twist (deg), Rake/R, Skew/R, Sweep, t/c, CLi, Axial, Tangential\n")
    write_col_vec(vec_list_to_print, file)


if __name__ == '__main__':
    # Exporting the required curves into .bem file for openVSP import

    pass
