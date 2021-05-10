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


def price_estimate(oper_hrs, fuel_per_hour, crew_per_hour, oper_yrs, W_empty, V_ne, Q_5, FTA, C_eng, N_eng, C_avionics,
                   average_speed=None, CPIs=(1.1604, 1.0611), profit=True, profit_margin=0.1, passenger=True,
                   table=False, latex_format=False):
    """
    Estimates the total cost/price throughout the lift cycle of an average aircraft

    (func: oper_cost & fuel_cost)
    :param CPIs:
    :param oper_hrs: float, (hr) average operating hours per year
    :param fuel_per_hour: float, (USD/hr) average fuel cost per hour
    :param crew_per_hour: float, (USD/hr) average crew cost per hour
    :param average_speed: float, (mph) average speed of aircraft (only needed for table)

    (func: price_estimate (main))
    :param oper_yrs: float, average operating years for aircraft

    (func: capital_cost)
    :param W_empty: float, (lb) empty weight of airplane
    :param V_ne: float, (kt) maximum equivalent airspeed
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

    tabulate_major_info(table, latex_format, W_empty, profit, oper_yrs, oper_hrs, V_ne, Q_5, FTA, average_speed)

    price_capital = capital_cost(W_empty, V_ne, Q_5, FTA, C_eng, N_eng, C_avionics,
                                 CPI=CPI_2012, profit=profit, profit_margin=profit_margin, passenger=passenger,
                                 table=table, latex_format=latex_format)

    price_oper, price_oper_bundle = operating_cost(oper_hrs, fuel_per_hour, crew_per_hour, average_speed=average_speed,
                                                   CPI=CPI_2018, profit=profit, profit_margin=profit_margin,
                                                   table=table,
                                                   latex_format=latex_format)

    price_total = price_capital + price_oper * oper_yrs * Q_5

    tabulate_total_cost(table, latex_format, price_total, price_capital, price_oper,
                        Q_5, oper_yrs, oper_hrs, average_speed, crew_per_hour)

    return price_total, price_capital, price_oper * oper_yrs * Q_5


def capital_cost(W_empty, V_ne, Q_5, FTA, C_eng, N_eng, C_avionics,
                 CPI=1.0, profit=True, profit_margin=0.1, passenger=True,
                 table=False, latex_format=False):
    """
    Estimates the cost (profit=False) or price (profit=True) of the airplane

    :param W_empty: float, (lb) empty weight of airplane
    :param V_ne: float, (kt) maximum equivalent airspeed
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
    H_E = 4.86 * W_empty ** 0.777 * V_ne ** 0.894 * Q_5 ** 0.163  # hrs

    # tooling hours
    H_T = 5.99 * W_empty ** 0.777 * V_ne ** 0.696 * Q_5 ** 0.263  # hrs

    # manufacturing hours
    H_M = 7.37 * W_empty ** 0.82 * V_ne ** 0.484 * Q_5 ** 0.641  # hrs

    # quality control hours
    if passenger:
        H_Q = 0.133 * H_M  # hrs for passenger airplane
    else:
        H_Q = 0.076 * H_M  # hrs for cargo airplane

    # development support cost
    C_D = 91.3 * W_empty ** 0.630 * V_ne ** 1.3  # USD in 2012

    # flight test cost
    C_F = 2498 * W_empty ** 0.325 * V_ne ** 0.822 * FTA ** 1.21  # USD in 2012

    # manufacturing materials cost
    C_M = 22.1 * W_empty ** 0.921 * V_ne ** 0.621 * Q_5 ** 0.799  # USD in 2012

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

    # print tabulated data
    adjust_num_cost = 1e6
    adjust_num_hrs = 1e3
    if table:
        data = [['Airframe Engineering', H_E / adjust_num_hrs, H_E * hourly_cost['R_E'] * CPI / adjust_num_cost],
                ['Tooling', H_T / adjust_num_hrs, H_T * hourly_cost['R_T'] * CPI / adjust_num_cost],
                ['Manufacturing', H_M / adjust_num_hrs, H_M * hourly_cost['R_M'] * CPI / adjust_num_cost],
                ['Quality Control', H_Q / adjust_num_hrs, H_Q * hourly_cost['R_Q'] * CPI / adjust_num_cost],
                ['Development', None, C_D * CPI / adjust_num_cost],
                ['Flight Test', None, C_F * CPI / adjust_num_cost],
                ['Manufacturing Material', None, C_M * CPI / adjust_num_cost],
                ['Engines', None, C_eng_total / adjust_num_cost],
                ['Avionics', None, C_avionics_total / adjust_num_cost],
                ['Total cost for {} airplanes (w/o profit)'.format(Q_5), None, est_cost / adjust_num_cost]]

        if profit:
            data.append(['Total price for {} airplanes (w/ profit)'.format(Q_5), None, est_price / adjust_num_cost])

        data.append(['Total cost per airplane (w/o profit)', None, est_cost / Q_5 / adjust_num_cost])

        if profit:
            data.append(['Total price per airplane (w/ profit)', None, est_price / Q_5 / adjust_num_cost])

        headers = ['Category', r'Time [10^3 hr]', r'Cost [Million USD]']

        if latex_format:
            table_out = tabulate(data, headers=headers, tablefmt="latex",
                                 numalign='right', floatfmt=(None, '.1f', '.1f'))
            print(table_out)
        else:
            table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                                 numalign='right', floatfmt=(None, '.1f', '.1f'))
            print(table_out)

    return est_price


def operating_cost(oper_hrs, fuel_cost_per_hour, crew_cost_per_hour, average_speed=None, CPI=1,
                   profit=True, profit_margin=0.1, table=False, latex_format=False):
    """
    Estimates the operating cost per year (excluding fuel) for a single aircraft
    Info from: https://www.faa.gov/regulations_policies/policy_guidance/benefit_cost/
               Section 4.2, Table 4-10
    Category of Jiffy Jerboa: Turboprop, multi-engine, part 23

    :param oper_hrs: float, (hr) average operating hours per year
    :param fuel_cost_per_hour: float, (most recent USD) hourly fuel cost
    :param crew_cost_per_hour: flaot, (most recent USD) hourly crew cost
    "param average_speed: float, (mph) average airspeed, only needed in table
    :param CPI: float, the inflation from 2018 USD to most recent USD
    :param profit: bool, True to include profit
    :param profit_margin: float, profit margin as a ratio
    :param table: bool, True to print tabulated data
    :param latex_format: bool, True to output in latex format
    :return annual_oper_cost: float, (most recent USD) operation cost per year (excluding fuel)
    """

    data_set = {  # based on 2018 USD
        'crew': 268,  # crew cost per flight hour
        'maintenance': 731,  # maintenance cost per flight hour
        'annual fixed cost without depreciation': 102687,  # annual fixed cost without depreciation
        'annual depreciation': 155238,  # annual depreciation price
        'average annual hours': 456  # average annual hours
    }

    if profit is True:
        profit_margin = profit_margin
    else:
        profit_margin = 0.0

    # all costs below are annual costs
    crew_cost = crew_cost_per_hour * oper_hrs * (1 + profit_margin)

    fuel_cost = fuel_cost_per_hour * oper_hrs * (1 + profit_margin)

    maintenance_cost = data_set['maintenance'] * data_set['average annual hours'] * (1 + profit_margin) * CPI

    fixed_cost = data_set['annual fixed cost without depreciation'] * CPI * (1 + profit_margin)

    depreciation_cost = data_set['annual depreciation'] * CPI * (1 + profit_margin)

    annual_oper_cost = crew_cost + fuel_cost + maintenance_cost + fixed_cost + depreciation_cost

    annual_oper_cost_no_crew = fuel_cost + maintenance_cost + fixed_cost + depreciation_cost

    annual_oper_cost_bundle = \
        ((crew_cost, fuel_cost, maintenance_cost, fixed_cost, depreciation_cost, annual_oper_cost),
         ('Crew', 'Fuel', 'Maintenance', 'Fixed', 'Depreciation', 'Total'))

    # print tabulated data
    if table:
        cost_bundle, name_bundle = annual_oper_cost_bundle
        round_digit = 1
        data = []

        if profit:
            data.append(['Profit Margin', '{:.2f}%'.format(profit_margin * 100)])
            data.append([' ', ' '])

        data.append(['Annual Operating Cost:', ' '])

        annual_adjust_num = 1e3
        for ii in range(len(cost_bundle)):
            data.append([name_bundle[ii], '{:.1f} Thousand USD'.format(round(cost_bundle[ii] / annual_adjust_num, round_digit))])

        data.append([' ', ' '])

        # per flight hour
        data.append(['Operating cost per flight hour:', ' '])

        for ii in range(len(cost_bundle)):
            data.append([name_bundle[ii], round(cost_bundle[ii] / oper_hrs, round_digit)])

        data.append([' ', ' '])

        # per mile per seat (with pilot)
        available_seat = 2  # total available seats in flight
        data.append(['Operating cost per mile per seat (with pilot)', ' '])

        if average_speed is None:
            raise Exception("Please provide an average speed in mph.")

        for ii in range(len(cost_bundle)):
            data.append([name_bundle[ii],
                         round(cost_bundle[ii] / oper_hrs / average_speed / available_seat, round_digit)])

        # per mile per seat (autonomous flight, without pilot)
        available_seat = 3  # total available seats in flight
        data.append(['Operating cost per mile per seat (autonomous)', ' '])

        if average_speed is None:
            raise Exception("Please provide an average speed in mph.")

        for ii in range(1, len(cost_bundle) - 1):
            data.append([name_bundle[ii],
                         round(cost_bundle[ii] / oper_hrs / average_speed / available_seat, round_digit)])

        data.append([name_bundle[-1],
                     round(annual_oper_cost_no_crew / oper_hrs / average_speed / available_seat, round_digit)])

        headers = ['Category', r'Cost [USD]']

        if latex_format:
            table_out = tabulate(data, headers=headers, tablefmt="latex",
                                 numalign='right', floatfmt=(None, '.0f', '.0f'))
            print(table_out)
        else:
            table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                                 numalign='right', floatfmt=(None, '.0f', '.0f'))
            print(table_out)

    return annual_oper_cost, annual_oper_cost_bundle


def tabulate_major_info(table, latex_format, W_empty, profit, oper_yrs, oper_hrs, V_ne, Q_5, FTA, average_speed):
    """
    Function to quickly capture the major information of design and price estimation

    :param table: bool, True to print the table
    :param latex_format: bool, True to output latex format
    :param W_empty: float, (lb) aircraft empty weight
    :param profit: bool, True to include profit
    :param oper_yrs: int, years of operation
    :param oper_hrs: int, annual hour of operation
    :param V_ne: float, (KIAS) never-exceed speed
    :param Q_5: int, production rate in 5 years
    :param FTA: int, number of flight test aircrafts
    :param average_speed: float, (mph) average aircraft speed
    :return: None
    """
    if table is False:
        return

    data = [['Aircraft Empty Weight', '{:.0f} lb'.format(W_empty)],
            ['Number of engine per aircraft', '{:d}'.format(N_eng)]]

    if profit is True:
        data.append(['Profit Margin', '{:.1f}%'.format(profit_margin * 100)])

    data.append(['Operating Years', oper_yrs])
    data.append(['Operating Hour per Year', oper_hrs])
    data.append(['Never-exceed Velocity', '{:.0f} KIAS'.format(V_ne)])
    data.append(['5-year Production Rate', Q_5])
    data.append(['Number of Test Airplanes', FTA])
    data.append(['Average Speed', '{:.0f} mph'.format(average_speed)])

    headers = ['Parameter', 'Value']

    if latex_format:
        table_out = tabulate(data, headers=headers, tablefmt="latex",
                             numalign='right', floatfmt=(None, '.0f', '.0f'))
        print(table_out)
    else:
        table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                             numalign='right', floatfmt=(None, '.0f', '.0f'))
        print(table_out)

    return


def tabulate_total_cost(table, latex_format, price_total, price_capital, price_oper,
                        Q_5, oper_yrs, oper_hrs, average_speed, crew_per_hour):
    if table is False:
        return

    data = []

    # cost per seat per mile
    # per mile per seat (with pilot)
    available_seat = 2  # total available seats in flight
    data.append(['Operating cost per mile per seat (with pilot)', ' '])
    data.append(['Total Cost per Mile',
                 '{:.2f}'.format(price_total / Q_5 / oper_yrs / oper_hrs / average_speed)])
    data.append(['Total Available Seats', available_seat])
    data.append(['Capital Cost per Mile per Seat',
                 '{:.2f}'.format(price_capital / Q_5 / oper_yrs / oper_hrs / average_speed / available_seat)])
    data.append(['Operating Cost per Mile per Seat',
                 '{:.2f}'.format(price_oper / oper_hrs / average_speed / available_seat)])
    data.append(['Total Cost per Mile per Seat',
                 '{:.2f}'.format(price_total / Q_5 / oper_yrs / oper_hrs / average_speed / available_seat)])

    data.append([' ', ' '])
    # cost per seat per mile
    # per mile per seat (autonomous, without pilot)
    available_seat = 3  # total available seats in flight
    data.append(['Operating cost per mile per seat (autonomous, without pilot)', ' '])
    data.append(['Total Cost per Mile',
                 '{:.2f}'.format((price_total / Q_5 / oper_yrs / oper_hrs - crew_per_hour)
                                 / average_speed)])
    data.append(['Total Available Seats', available_seat])
    data.append(['Capital Cost per Mile per Seat',
                 '{:.2f}'.format(price_capital / Q_5 / oper_yrs / oper_hrs / average_speed / available_seat)])
    data.append(['Operating Cost per Mile per Seat',
                 '{:.2f}'.format((price_oper / oper_hrs - crew_per_hour) / average_speed / available_seat)])
    data.append(['Total Cost per Mile per Seat',
                 '{:.2f}'.format((price_total / Q_5 / oper_yrs / oper_hrs - crew_per_hour)
                                 / average_speed / available_seat)])

    headers = ['Category', 'USD']

    if latex_format:
        table_out = tabulate(data, headers=headers, tablefmt="latex",
                             numalign='right', floatfmt=(None, '.0f', '.0f'))
        print(table_out)
    else:
        table_out = tabulate(data, headers=headers, tablefmt="fancy_grid",
                             numalign='right', floatfmt=(None, '.0f', '.0f'))
        print(table_out)

    return


if __name__ == '__main__':
    # price estimation for Jiffy Jerboa
    # set values
    W_empty = 2495.50  # lb, operating empty weight
    V_d = 134.1  # KIAs, structural limit speed
    V_ne = 0.9 * V_d  # KIAS, never exceed speed, adopted from Cessna 172 (127 KTAS)
    N_eng = 8  # eight engine per aircraft
    CPI_2012 = 1.160364414  # CPI from Jan 2012 to Feb 2021
    CPI_2018 = 1.061109385  # CPI from Jan 2018 to Feb 2021
    CPIs = [CPI_2012, CPI_2018]

    # adjustable values
    Q_5 = 500  # production rate over past 5 years
    FTA = 5  # test flight airplanes

    C_avionics = 50000  # USD, cost for avionics, adopted from SkyView HDX system for Cessna models
    C_fuel_cell = 20000  # online brief research
    C_battery = 20000  # battery
    C_motor = 3000 * N_eng  # estimated cost of motor, tilting mechanism, etc...
    C_eng = C_fuel_cell + C_battery + C_motor

    profit_margin = 0.1
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

    average_speed = 120  # average speed is 120 miles per hour

    price_out = price_estimate(oper_hrs, fuel_per_hr, crew_per_hr, oper_yrs, W_empty, V_ne, Q_5, FTA, C_eng, N_eng,
                               C_avionics, average_speed=average_speed, CPIs=CPIs, profit=True,
                               profit_margin=profit_margin, passenger=True, table=True, latex_format=True)
    """
    print('Fuel price is {:.2f} USD per hour'.format(fuel_per_hr))
    print('For Jiffy Jerboa (in USD 2021)')
    print('----------------------------')
    print('Total price: {:.2e}'.format(price_out[0]))
    print('Price per aircraft {:.2e}'.format(price_out[0] / Q_5))
    print('Capital price per aircraft: {:.2e}'.format(price_out[1] / Q_5))
    print('Operating price (fuel included) per aircraft: {:.2e}'.format(price_out[2] / Q_5))
    print('Total price per flight hour: {:.0f} USD'.format(price_out[0] / Q_5 / (oper_hrs * oper_yrs)))
    print('Operating price (fuel included) per flight hour: {:.0f} USD'.format(
        price_out[2] / Q_5 / (oper_hrs * oper_yrs)))
    print('Price per mile is {:.2f} USD'.format((price_out[0] / Q_5 / (oper_hrs * oper_yrs)) / average_speed))
    print('----------------------------')
    """
