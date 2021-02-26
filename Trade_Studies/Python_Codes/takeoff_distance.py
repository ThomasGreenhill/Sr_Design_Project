
import numpy
from Class130 import AtmData, Wing

def takeoff_distance(W, T_avg, mu_r, AtmData, Wing):
'''
    Provides calculations for takeoff distance

    Inputs:
            W: Weight of aircraft
            T_avg: Average thrust
            mu_r: Rolling friction coefficient -- typical:
                    0.02 for dry concrete to 0.3 for very soft ground
            Wing.area: Wing reference area (Class:Wing)
            Wing.CL_max: Maximum lift coefficient (Class:Wing)
            Wing.CD_0: Zero lift drag coefficient (Class:Wing)
            Wing.span: Wing span (Class:Wing)
            Wing.e: Span efficiency factor (Class:Wing)
            AtmData.dens: Density of air (Class:AtmData)

    Outputs:
            SG: Takeoff ground roll distance

    Calls:
        {none}

    Notes:
        1. Stability derivatives should be dimensionalized!
        2.

    History:
        2.9.2021: Created file. TVG
        2.13.2021: Created function. GN
        2.14.2021: Translated & integrated to python by XTang
        Not Yet Debugged!
'''

    g: float = 9.81                # m/s^2
    if Wing.is_SI:      # SI units
        a = numpy.sqrt(AtmData.k * AtmData.R * AtmData.temp)
    else:               # British units
        a = numpy.sqrt(AtmData.k * AtmData.R * AtmData.temp * 32.174)


    K = 1/(numpy.pi * Wing.e * Wing.AR)

    v_stall = numpy.sqrt(2 * W / (AtmData.dens * Wing.area * Wing.CL_max))
    v_lof = 1.1 * v_stall           # Liftoff velocity
    v_avg = v_lof / numpy.sqrt(2)
    M_avg = v_avg / a

    CL_opt = mu_r / (2 * K)         # Optimal lift coefficient
    CD_avg = Wing.CD_0 + (K * CL_opt ** 2)

    q_avg = 0.5 * AtmData.dens * (v_avg ** 2)       # Average dynamic pressure
    D_avg = CD_avg * q_avg * Wing.area              # Average drag
    L_avg = CL_opt * q_avg * Wing.area              # Average lift

    a_avg = (g / W) * (T_avg - D_avg - (mu_r * (W - L_avg)) # Average acceleration
    SG = (v_lof ** 2) / (2 * a_avg)     # Ground role distance

    return SG
