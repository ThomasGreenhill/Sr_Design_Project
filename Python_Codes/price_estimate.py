"""
Estimates the total cost of the aircraft design
Based on lecture 04.06.2021

Note:
    1. capital_cost debugged
    2. not checked with authorized data (not yet found)
    3. CPI calculated from https://www.bls.gov/data/inflation_calculator.htm

History:
    Created, XT. 04.06.2021
    Debugged, XT. 04.06.2021
    Checked and got reasonable values, XT. 04.17.2021
"""
from tabulate import tabulate
import numpy as np


def price_estimate(oper_hrs, fuel_per_hour, crew_per_hour, oper_yrs, W_empty, V_max, Q_5, FTA, C_eng, N_eng, C_avionics,
                   CPIs=(1.1604, 1.0611), profit=True, profit_margin=0.1, passenger=True,
                   table=False, latex_format=False):
    """
    Estimates the total cost/price throughout the lift cycle of an average aircraft

    (func: oper_cost & fuel_cost)
    :param CPIs:
    :param oper_hrs: float, (hr) average operating hours per year
    :param fuel_per_hour: float, (USD/hr) average fuel cost per hour
    :param crew_per_hour: float, (USD/hr) average crew cost per hour

    (func: price_estimate (main))
    :param oper_yrs: float, average operating years for aircraft

    (func: capital_cost)
    :param W_empty: float, (lb) empty weight of airplane
    :param V_max: float, (kt) maximum equivalent airspeed
    :param Q_5: int, lesser of production quantity or number to be produced in 5 years
    :param FTA: int, number of flight test airplanes
    :param C_eng: float, (most recent USD) cost per engine
    :param N_eng: int, number of engine per aircraft
    :param C_avionics: float, (most recent USD) cost per avionic system
    :param CPI: float, [CPI_2012, CPI_2018] inflation ratio from Jan 2012 and Jan 2018 to most recent
    :param profit: bool, True to include profit, false to return only cost
    :param profit_margin: float, profit margin for calculating profit
    :param passenger: bool, Trye for passenger plane, false for cargo plane
    :param table: bool, True for printing the tabulated values
    :param latex_format: bool, True to convert the table to latex format
    :return price_total: float, (most recent USD) total cost/price in most recent USD for an aircraft life
    :return price_capital: float, (most recent USD) capital price
    :return price_operating: float, (most recent USD) operating price with fuel
    """

    if np.size(CPIs) != 2:
        raise ValueError("Please provide a list or tuple of size two for CPIs = (CPI_from_2012, CPI_from_2018)")
    try:
        CPI_2012 = float(CPIs[0])
        CPI_2018 = float(CPIs[1])
    except ValueError:
        print("Element in CPIs is not number")

    price_capital = capital_cost(W_empty, V_max, Q_5, FTA, C_eng, N_eng, C_avionics,
                                 CPI=CPI_2012, profit=profit, profit_margin=profit_margin, passenger=passenger,
                                 table=table, latex_format=latex_format)

    price_oper = operating_cost(oper_hrs, fuel_per_hour, crew_per_hour, CPI=CPI_2018,
                                profit=profit, profit_margin=profit_margin)
    price_total = price_capital + price_oper * oper_yrs * Q_5

    return price_total, price_capital, price_oper * oper_yrs * Q_5


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
        data = [['Airframe Engineering', H_E, H_E * hourly_cost['R_E'] * CPI / 1e3],
                ['Tooling', H_T, H_T * hourly_cost['R_T'] * CPI / 1e3],
                ['Manufacturing', H_M, H_M * hourly_cost['R_M'] * CPI / 1e3],
                ['Quality Control', H_Q, H_Q * hourly_cost['R_Q'] * CPI / 1e3],
                ['Development', None, C_D * CPI / 1e3],
                ['Flight Test', None, C_F * CPI / 1e3],
                ['Manufacturing Material', None, C_M * CPI / 1e3],
                ['Engines', None, C_eng_total / 1e3],
                ['Avionics', None, C_avionics_total / 1e3],
                ['Total cost for {} airplanes (w/o profit)'.format(Q_5), None, est_cost / 1e3]]

        if profit:
            data.append(['Total price for {} airplanes (w/ profit)'.format(Q_5), None, est_price / 1e3])

        data.append(['Total cost per airplane (w/o profit)', None, est_cost / Q_5 / 1e3])

        if profit:
            data.append(['Total price per airplane (w/ profit)', None, est_price / Q_5 / 1e3])

        headers = ['Category', 'Time [hr]', r'Cost [10^3 USD]']

        if latex_format:
            table_out = tabulate(data, headers=headers, tablefmt="latex",
                                 numalign='right', floatfmt=(None, '.0f', '.0f'))
            print(table_out)
        else:
            table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                                 numalign='right', floatfmt=(None, '.0f', '.0f'))
            print(table_out)

    return est_price


def operating_cost(oper_hrs, fuel_cost_per_hour, crew_cost_per_hour, CPI=1,
                   profit=True, profit_margin=0.1):
    """
    Estimates the operating cost per year (excluding fuel) for a single aircraft
    Info from: https://www.faa.gov/regulations_policies/policy_guidance/benefit_cost/
               Section 4.2, Table 4-10
    Category of Jiffy Jerboa: Turboprop, multi-engine, part 23

    :param oper_hrs: float, (hr) average operating hours per year
    :param CPI: float, the inflation from 2018 USD to most recent USD
    :return annual_oper_cost: float, (most recent USD) operation cost per year (excluding fuel)
    """

    data_set = {  # based on 2018 USD
        'total per hour': 2164 - 561 - 268,  # fuel, crew subtracted
        'average annual hours': 456
    }

    average_annual_cost_other = data_set['total per hour'] * data_set['average annual hours']

    annual_oper_cost = average_annual_cost_other + (fuel_cost_per_hour + crew_cost_per_hour) * oper_hrs

    if profit is True:
        profit_margin = profit_margin
    else:
        profit_margin = 0.0

    return annual_oper_cost * (1.0 + profit_margin)

if __name__ == '__main__':
    # price estimation for Jiffy Jerboa
    # set values
    W_empty = 2495.50  # lb, operating empty weight
    V_max = 127  # KIAS, never exceed speed, adopted from Cessna 172 (127 KTAS)
    N_eng = 8  # eight engine per aircraft
    CPI_2012 = 1.160364414  # CPI from Jan 2012 to Feb 2021
    CPI_2018 = 1.061109385  # CPI from Jan 2018 to Feb 2021
    CPIs = [CPI_2012, CPI_2018]

    # adjustable values
    Q_5 = 80 * 15  # production rate over past 5 years
    FTA = 5  # test flight airplanes

    C_avionics = 20000 + 2000  # USD, cost for avionics, adopted from SkyView HDX system for Cessna models
    C_fuel_cell = 12555  # online brief research
    C_motor = 3000 * N_eng  # from EMRAX quote, already being conservative
    C_eng = C_fuel_cell + C_motor

    profit_margin = 0.127
    oper_hrs = 6 * 365  # 6 hr/day, just an rough estimate
    oper_yrs = 15  # assumed based on typical Cessna 172 lasting 30000 hrs

    H2_specific_energy = 120e6  # J / kg
    # HD100_net_power = 100e3  # W
    average_power_required = 1e5  # W, assumed by forward climb, can change later
    H2_efficiency = 0.57 * 0.92  # fuel cell eff * motor eff, assumed from specs
    m_dot_H2 = average_power_required / (H2_specific_energy * H2_efficiency)  # kg / s
    m_H2_per_hr = m_dot_H2 * 3600  # Kg / s to kg / hr
    fuel_price_per_kg = 16.51  # 16.51 USD per kg
    fuel_per_hr = fuel_price_per_kg * m_H2_per_hr  # USD / hr

    crew_per_hr = 63  # USD/hr, for one pilot in flight
    
    price_out = price_estimate(oper_hrs, fuel_per_hr, crew_per_hr, oper_yrs, W_empty, V_max, Q_5, FTA, C_eng, N_eng,
                               C_avionics, CPIs=CPIs, profit=True,
                               profit_margin=profit_margin, passenger=True, table=True, latex_format=False)

    print('Fuel price is {:.2f} USD per hour'.format(fuel_per_hr))
    print('For Jiffy Jerboa (in USD 2021)')
    print('----------------------------')
    print('Total price: {:.2e}'.format(price_out[0]))
    print('Price per aircraft {:.2e}'.format(price_out[0] / Q_5))
    print('Capital price per aircraft: {:.2e}'.format(price_out[1] / Q_5))
    print('Operating price (fuel included) per aircraft: {:.2e}'.format(price_out[2] / Q_5))
    print('Total price per flight hour: {:.2e}'.format(price_out[0] / Q_5 / (oper_hrs * oper_yrs)))
    print('Operating price (fuel included) per flight hour: {:.2e}'.format(price_out[2] / Q_5 / (oper_hrs * oper_yrs)))
    print('----------------------------')

    """
    # capital_cost test case from 04.06.2021 lecture example 
    
    # rate of inflation from Jan 2012 to Jan 2021
    # obtained from:
    # https://www.bls.gov/data/inflation_calculator.htm
    inflation_2012 = 11603644.14 / 10000000.00  # from 2012 to 2021
    inflation_2018 = 10611093.85 / 10000000.00  # from 2018 to 2021

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
    # The test case has quality control hours set for cargo airplanes
    # Other than that, the func is good
    """


    """
    # operating_cost test
    
    oper_hrs = 456
    oper_cost = operating_cost(oper_hrs, CPI=1)

    
    # price_estimate (main) test
    
    oper_yrs = 10
    CPIs = (1.1604, 1.0611)
    fuel_per_hr = 20
    price_out = price_estimate(oper_hrs, fuel_per_hr, oper_yrs, W_empty, V_max, Q_5, FTA, C_eng, N_eng,
                                 C_avionics, CPIs=CPIs, profit=True,
                                 profit_margin=profit_margin, passenger=False, table=True, latex_format=False)
    print(price_out[0] / 1e6)
    """
