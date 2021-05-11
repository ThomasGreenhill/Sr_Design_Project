


import numpy as np


def global_hydrogen_production(year):

    p1 = -4.68e-5
    p2 = 2.85e-1
    p3 = -5.79e2
    p4 = 3.91e5

    production = p1 * year ** 3 + p2 * year ** 2 + p3 * year + p4  # Mt/year

    return production


def investment_cost(year):

    # CPI and convertion
    CPI2014 = 1.56917654  # from 2014 to 2021
    Euro_2_USD = 1.21
    k = CPI2014

    # PEM
    a1 = 2.2998e60
    b1 = -0.06534
    cost_PEM = k * a1 * np.exp(b1 * year)  # Euro/KW
    cost_PEM = Euro_2_USD * cost_PEM  # USD/kW

    # ALkaline
    a2 = 2.422e42
    b2 = -0.04734

    cost_alkaline = k * a2 * np.exp(b2 * year)  # Euro/KW
    cost_alkaline = Euro_2_USD * cost_alkaline  # USD/KW

    return cost_PEM, cost_alkaline