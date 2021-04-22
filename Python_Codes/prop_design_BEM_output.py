import numpy as np
import math
from prop_design_TVG import prop_design
from Class130 import AtmData, Propeller
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
        str_out = str_out + str(vec[ii])
        if ii < len(vec) - 1:
            str_out += ", "
        else:
            str_out += "\n"
    return str_out


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
r, prop.chord, prop.bet, P_design, T_design, Q_design, eta_P, prop.theta = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

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

# Other parameters needed to write file
feather_angle = 0  # rad, feather angle
pre_cone_angle = 0  # rad, pre-cone angle
center = (0.0, 0.0, 0.0)  # center location
normal = (-1.0, 0.0, 0.0)  # normal vector

rake = np.zeros(np.shape(prop.chord))
skew = np.zeros(np.shape(prop.chord))
sweep = np.zeros(np.shape(prop.chord))
t_c = np.zeros(np.shape(prop.chord))
axial = np.zeros(np.shape(prop.chord))
tangential = np.zeros(np.shape(prop.chord))
CLi = CL_design * np.ones(np.shape(prop.chord))

# Write to file
parent_path = "../OpenVSP_X/v2.1/BEM Files/"
file_name = "prop_design.bem"
file_path = parent_path + file_name
mode = "w"
with open(file_path, mode) as file:
    file.write("...BEM Propeller...\n")
    file.write("Num_Sections: {}\n".format(num_len))
    file.write("Num_Blades: {}\n".format(numB))
    file.write("Diameter: {}\n".format(diameter))
    file.write("Beta 3/4 (deg): {}\n".format(np.rad2deg(prop.bet[beta_75_index])))
    file.write("Feather (deg): {}\n".format(np.rad2deg(feather_angle)))
    file.write("Pre_Cone (deg): {}\n".format(np.rad2deg(pre_cone_angle)))
    file.write("Center: {}, {}, {}\n".format(center[0], center[1], center[2]))
    file.write("Normal: {}, {}, {}\n".format(normal[0], normal[1], normal[2]))
    file.write("\n")
    file.write("Radius/R, Chord/R, Twist (deg), Rake/R, Skew/R, Sweep, t/c, CLi, Axial, Tangential\n")
    file.write(vec_to_str(x))  # Radius/R
    file.write(vec_to_str(prop.chord / radius))  # Chord/R
    file.write(vec_to_str(np.rad2deg(prop.bet)))  # twist angle in deg
    file.write(vec_to_str(rake))  # Rake/R, set to zeros
    file.write(vec_to_str(skew))  # Skew/R, set to zeros
    file.write(vec_to_str(sweep))  # Sweep, set to zeros
    file.write(vec_to_str(t_c))  # t/c, set to zeros
    file.write(vec_to_str(CLi))  # CLi
    file.write(vec_to_str(axial))  # Axial
    file.write(vec_to_str(tangential))  # Tangential







if __name__ == '__main__':
    # Exporting the required curves into .bem file for openVSP import

    pass
