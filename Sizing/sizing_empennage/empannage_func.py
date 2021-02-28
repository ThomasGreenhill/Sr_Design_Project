import sys
sys.path.append("../../Python_Codes/Class130.py")




vol_h = 0.655
vol_v = 0.0425

def horizontal_tail_area(S_wing, c_bar, b_span):
    """
    Sizes the tail areas based on the wing area, volumes, and moment arms

    Input:
            S_wing: (m^2) wing area
            c_bar: (m) wing mean chord length
            b_span: (m) wing span
            x_h: (m) horizontal tail moment arm
            x_v: (m) vertical tail moment arm

    Output:
            S_hs: (m^2) horizontal tail area estimate
            S_vs: (m^2) vertical tail area estimate
    """

