import numpy


def landing_distance(gam, VS, W, S, rho, muB, CD, CL):
    '''
            Based on EAE 130B lecture slide 31 on April 15, 2021
            
            Inputs:
                    

            Outputs:
                    

            Notes:

            History:
                04.17.2021: Created. TVG
    '''
    g = 32.17 # ft.s^-2

    # Assume V = V approach = VS*1.23
    V = VS*1.23
    n = 1.2 # Assumed

    # Air distance
    SF = V**2/(g*(n-1)) * numpy.sin(gam)
    hF = V**2/(g*(n-1))*(1-numpy.cos(gam))
    SA = (50 - hF)/(numpy.tan(gam)) + SF

    # Free roll distance
    # Assume 3 seconds and VTD = VS
    VTD = VS

    tFR = 3
    SFR = tFR*VTD

    # Braking distance
    SB = W/(muB*g*rho*S) * 1/(CD/muB-CL) * numpy.log(1 + rho*S/(2*W)*(CD/muB - CL)*VTD**2)

    return SF, SA, SFR, SB

if __name__ == '__main__':
    CL = 1.5
    CD = 0.1/0.5 # dummy factor of 0.5 applied (i.e. rotors in unfeathered position)
    LD =  CL/CD
    gam = numpy.arctan(1/LD)
    
    VS = 27*3.28084
    W = 13000*0.224809
    rho = 1.225*0.00194032
    muB = 0.5 # hard dry surface

    S = 16*10.7639 #m^2

    SF, SA, SFR, SB = landing_distance(gam, VS, W, S, rho, muB, CD, CL)

    STOT = SF + SA + SFR + SB
    print("TOTAL LANDING DISTANCE: {} ft".format(STOT))
    