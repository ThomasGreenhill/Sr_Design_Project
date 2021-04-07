"""
Estimates the total cost of the aircraft design
Based on lecture 04.06.2021

Note:
    capital_cost debugged

History:
    Created, XT. 04.06.2021
"""
from tabulate import tabulate


def capital_cost(W_empty, V_max, Q_5, FTA, C_eng, N_eng, C_avionics,
                 CPI=1.0, profit=True, profit_margin=0.1, passenger=True,
                 table=False, latex_format=False):
    """
    Estimates the cost (profit=False) or price (profit=True) of the airplane

    :param W_empty: float, (lb) empty weight of airplane
    :param V_max: float, (kt) maximum equivalent airspeed
    :param Q_5: int, lesser of production quantity or number to be produced in 5 years
    :param FTA: int, number of flight test airplanes
    :param C_eng: float, (most recent USD) cost per engine
    :param N_eng: int, number of engine per aircraft
    :param C_avionics: float, (most recent USD) cost per avionic system
    :param CPI: float, inflation ratio from Jan 2021 to most recent
    :param profit: bool, True to include profit, false to return only cost
    :param profit_margin: float, profit margin for calculating profit
    :param passenger: bool, Trye for passenger plane, false for cargo plane
    :param table: bool, True for printing the tabulated values
    :param latex_format: bool, True to convert the table to latex format
    :return: est_price: float, (most recent USD) estimated price for aircraft
    """

    # hourly costs in 2012
    hourly_cost = {  # USD in 2012
        'R_E': 115,
        'R_T': 118,
        'R_M': 98,
        'R_Q': 108,
    }

    # airframe engineering hours
    H_E = 4.86 * W_empty ** 0.777 * V_max ** 0.894 * Q_5 ** 0.163  # hrs

    # tooling hours
    H_T = 5.99 * W_empty ** 0.777 * V_max ** 0.696 * Q_5 ** 0.263  # hrs

    # manufacturing hours
    H_M = 7.37 * W_empty ** 0.82 * V_max ** 0.484 * Q_5 ** 0.641  # hrs

    # quality control hours
    if passenger:
        H_Q = 0.133 * H_M  # hrs for passenger airplane
    else:
        H_Q = 0.076 * H_M  # hrs for cargo airplane

    # development support cost
    C_D = 91.3 * W_empty ** 0.630 * V_max ** 1.3  # USD in 2012

    # flight test cost
    C_F = 2498 * W_empty ** 0.325 * V_max ** 0.822 * FTA ** 1.21  # USD in 2012

    # manufacturing materials cost
    C_M = 22.1 * W_empty ** 0.921 * V_max ** 0.621 * Q_5 ** 0.799  # USD in 2012

    # engine cost
    C_eng_total = C_eng * N_eng * Q_5

    # avionic cost
    C_avionics_total = C_avionics * Q_5

    # cost RTD&E + flyaway (adjusted for inflation)
    est_cost = (H_E * hourly_cost['R_E'] + H_T * hourly_cost['R_T']
                + H_M * hourly_cost['R_M'] + H_Q * hourly_cost['R_Q']
                + C_D + C_F + C_M) * CPI \
            + C_eng_total + C_avionics_total

    # include profit margin
    if profit is not True:
        profit_margin = 0.0
    est_price = est_cost * (1.0 + profit_margin)

    if table:
        data = [['Airframe Engineering', H_E, H_E * hourly_cost['R_E'] * CPI / 1e6],
                ['Tooling', H_T, H_T * hourly_cost['R_T'] * CPI / 1e6],
                ['Manufacturing', H_M, H_M * hourly_cost['R_M'] * CPI / 1e6],
                ['Quality Control', H_Q, H_Q * hourly_cost['R_Q'] * CPI / 1e6],
                ['Development', None, C_D * CPI / 1e6],
                ['Flight Test', None, C_F * CPI / 1e6],
                ['Manufacturing Material', None, C_M * CPI / 1e6],
                ['Engines', None, C_eng_total / 1e6],
                ['Avionics', None, C_avionics_total / 1e6],
                ['Total cost for {} airplanes (w/o profit)'.format(Q_5), None, est_cost / 1e6]]

        if profit:
            data.append(['Total price for {} airplanes (w/ profit)'.format(Q_5), None, est_price / 1e6])

        data.append(['Total cost per airplane (w/o profit)', None, est_cost / Q_5 / 1e6])

        if profit:
            data.append(['Total price per airplane (w/ profit)', None, est_price / Q_5 / 1e6])

        headers = ['Category', 'Time [hr]', r'Cost [10^6 USD]']

        if latex_format:
            table_out = tabulate(data, headers=headers, tablefmt="latex",
                                 numalign='right', floatfmt=(None, '.0f', '.1f'))
            print(table_out)
        else:
            table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                                 numalign='right', floatfmt=(None, '.0f', '.1f'))
            print(table_out)

    return est_price


if __name__ == '__main__':
    """
    capital_cost test case from 04.06.2021 lecture example 
    """
    # rate of inflation from Jan 2012 to Jan 2021
    # obtained from:
    # https://www.bls.gov/data/inflation_calculator.htm
    inflation = 15581398.10 / 10000000.00

    W_empty = 5867  # lb, empty weight
    V_max = 236  # KIAS, never exceed speed
    Q_5 = 275  # production rate over past 5 years
    FTA = 2  # test flight airplanes
    C_eng = 850000  # USD, cost per engine
    N_eng = 1  # one engine per aircraft
    C_avionics = 250000  # USD, cost for avionics
    CPI = 1.107  # 2012 - 2019
    profit_margin = 0.1

    price = capital_cost(W_empty, V_max, Q_5, FTA, C_eng, N_eng, C_avionics, CPI=CPI, profit=True,
                         profit_margin=profit_margin, passenger=False, table=True, latex_format=False)
    # print(price / 1e6 / Q_5)
    # The test case seems to ignore the manufacturing material cost
    # Other than that, the func is good
