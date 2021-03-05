import numpy
import math
import matplotlib.pyplot as plt
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from Class130 import AtmData, Propeller
from prop_design_TVG import prop_design

"""
Plots a 3D figure of propeller, written by TVG in Matlab.

Input:
        r_list_in: list of r from 0 to 1
        c_list_in: (m) list of chord length 
        beta_list_in: (deg) list of beta angle
        Propeller: Needs radius, numB
        in_line: line vector reserved for swept propeller

Output:
        {None}

Calls:
        {None}
        
Notes:
        1. Translated to Python based on TVG's plotblade3D matlab script
        2. Parameters can be modified to integrate into Propeller class entirely

History:
        03.04.2021, XT. Translated from TVG's work from Matlab
        03.04.2021, XT. Debugged
"""

def plot_propeller_3D(r_list_in, c_list_in, beta_list_in, Propeller, in_line, show=True, save=False, path=None, is_rad=True):
    # return

    def get_Rx(beta_in, is_rad):
        """
        Gets rotational matrix around x axis
        :param beta: (deg) pitch angle
        :param is_rad: True for radian, False for deg, for beta angles
        :return: Rx: rotational matrix Rx
        """
        if not is_rad:
            beta = numpy.deg2rad(beta_in)  # Converts from deg to rad
        else:
            beta = beta_in
        Rx = numpy.array([[1, 0, 0],
              [0, numpy.cos(beta), numpy.sin(beta)],
              [0, -numpy.sin(beta), numpy.cos(beta)]])
        return Rx

    R = Propeller.radius
    numB = Propeller.numB

    # Allocating spaces
    LIST_SIZE = 0
    for item in r_list_in:
        LIST_SIZE = LIST_SIZE + 1 if item >= 0.15 * R else LIST_SIZE

    # Takes only r >= 0.15R
    r_list = []
    beta_list = []
    c_list = []
    line_list = []
    for i in range(len(r_list_in)):
        if r_list_in[i] >= 0.15 * R:
            r_list.append(r_list_in[i])
            beta_list.append(beta_list_in[i])
            c_list.append(c_list_in[i])
            line_list.append(in_line[i])

    # Assigning to numpy.array
    r = numpy.array(r_list, dtype='float64')
    beta = numpy.array(beta_list, dtype='float64')
    c = numpy.array(c_list, dtype='float64')
    line = numpy.array(line_list, dtype='float64')

    x = numpy.concatenate([r, numpy.flip(r)])
    y = numpy.concatenate([(c / 2 + line), numpy.flip(line - c / 2)])
    z = numpy.zeros(LIST_SIZE * 2, dtype='float64')
    bb = numpy.concatenate([beta, numpy.flip(beta)])

    vec = numpy.vstack([x, y, z])
    rot_vec = numpy.zeros(vec.shape)

    for i in range(x.size):
        Rx = get_Rx(bb[i], is_rad)
        rot_vec[:, i] = numpy.dot(Rx, vec[:, i])

    # Plot
    fig = plt.figure()
    ax = Axes3D(fig)
    fig.set_label("Propeller 3D Geometry Plot")
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)
    ax.set_zlabel('z', fontsize=10)
    ax.axes.set_xlim3d(left=-1.2, right=1.2)
    ax.axes.set_ylim3d(bottom=-1.2, top=1.2)
    ax.axes.set_zlim3d(bottom=-1.2, top=1.2)

    for blades in range(numB):
        theta = 2 * numpy.pi / numB * (blades + 1)
        x_rot = x * numpy.cos(theta) - y * numpy.sin(theta)
        y_rot = x * numpy.sin(theta) - y * numpy.cos(theta)
        verts = [list(zip(x_rot, y_rot, rot_vec[2, :]))]
        ax.add_collection3d(Poly3DCollection(verts))

    if show:
        plt.show()
    if save:
        if path is None:
            raise FileNotFoundError("Please provide saving directory: path={}")
        plt.savefig(path, bbox_inches='tight')


if __name__ == '__main__':

    def m0_fn(Ma):
        if Ma <= 0.9:
            return (2 * math.pi) / numpy.sqrt(1 - Ma ** 2)
        else:
            return (2 * math.pi) / numpy.sqrt(1 - 0.9 ** 2)


    def Cd_fn(Cl):
        return 0.0095 + 0.0040 * (Cl - 0.2) ** 2


    nn = 101
    h = 0  # m
    v_inf = 70  # m/s
    is_SI = True
    atm = AtmData(v_inf, h, is_SI)
    k = 1.4
    R = 287
    atm.expand(k, R)

    numB = 3
    radius = 1.78 / 2
    RPM = 2400
    Cl = 0.4
    alp0 = numpy.radians(-2)
    prop = Propeller(radius, numB, RPM, CP=0, CT=0, CQ=0, Cl=Cl, alp0=alp0)

    T_req = 13000 / 8  # N (TOGW/(L/D))
    r_vec, c_vec, beta_vec, P_design, T_design, Q_design, eta_P, theta_vec = prop_design(atm, prop, T_req, m0_fn, Cd_fn)

    in_line = [0] * len(r_vec)
    plot_propeller_3D(r_vec, c_vec, beta_vec, prop, in_line)