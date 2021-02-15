
import numpy
from Class130 import AtmData, Airfoil, Wing

def wing_dimension(W, AtmData, Airfoil, Wing):

    def lift_coeff(Cla, e, AR, a):
        return a * Cla / (1 + 57.3 * Cla / (numpy.pi * e * AR))

'''
    Computes the required chord and platform area for a wing based on a set
    of requirements

    Inputs:
            W: Aircraft weight
            AtmData.vel: Free-stream velocity (Class:AtmData)
            AtmData.dens: Air density (Class:AtmData)
            Airfoil.Cla: Airfoil lift curve slope -- typical value 0.11 (Class:Airfoil)
            Airfoil.Cl_max (Class:Airfoil)
            Wing.span = Wing span (Class:Wing)
            Wing.e = Wing span efficiency ratio (Class:Wing)

    Outputs:
        {none}

    Notes:


    History:
        02.09.2021: Created and debugged, TVG
        02.14.2021: Translated & integrated with Class130 by XTang
        Not Yet Debugged
'''
    q_inf = 0.5 * AtmData.dens * AtmData.vel ** 2
    c_new = 1
    S_new = Wing.span * c_new
    cor = 1
    iter_lim = 1e3
    tol = 1e-6
    iter = 1

    while iter < iter_lim and cor >= tol:
        a = 17

        S_old = S_new
        c_old = c_new

        AR = Wing.span / c_old
        CL_required = W / (S_old * q_inf)

        while (a * Airfoil.Cla) < Airfoil.Cl_max:
            CL_design = lift_coeff(Cla, e, AR, a)
            a += 0.1

        if CL_design < CL_required:
                c_new = c_old * (1 - (CL_design - CL_required) / (CL_required + CL_design))
        elif CL_design > CL_required:
                c_new = c_old * (1 - (CL_design - CL_required) / (CL_required + CL_design))
        else:
            break

        S_new = c_new * Wing.span

        cor = abs(S_new - S_old)
        iter += 1

    # Assign iterated chord_avg and area to Class
    Wing.c_bar = c_new
    Wing.area = S_new

    return c_new, S_new