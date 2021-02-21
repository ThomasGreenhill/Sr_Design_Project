
import numpy
import matplotlib.pyplot as plt
from sizing_process import sizing_process
import os
import sys
sys.path.append("../Trade_Studies")
import Class130
sys.path.append("../Utilities")
import formatfigures

try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False


def sizing_figures(Sizing, S_wing_LO, S_wing_HI, S_disk_LO, S_disk_HI, num):

    '''
    Script to plot and save the required figures for the sizing purpose

    Input:
        Sizing: Class of all sizing parameters, see Class130 for reference
        S_wing_LO: (m^2) smallest wing area
        S_wing_HI: (m^2) largest wing area
        S_disk_LO: (m^2) smallest disk area
        S_disk_HI: (m^2) largest disk area
        num: number of points

    Output:
        {None} \\ All figures saved in folder

    Calls:
        sizing_process.py

    Note:
        1. ***Thrust-to-weight ratio needs to be updated with the propulsion design from Yihui and Gloria
        2. ***Figures need to be decorated with latex
        3. The values align with progress report. If there is any change, please make sure to
           change the values in this script as well
        4. All figures are stored in the folder: sizing_figures

    History:
        02.17.2021: Created, XT
                        TOGW vs. wing area
                        TOGW vs. disk area
                        power loading vs. disk loading
        02.18.2021: Added figures, XT
                        power loading vs. wing loading
                        thrust-to-weight ratio vs. wing loading
                        TOGW vs. wing loading (subplot)
                        TOGW vs. disk loading (subplot)
        02.18.2021: Debugged, XT & TVG
        02.18.2021: Converted to function and debugged, XT

    '''

    ############## Making directory ##############
    my_folder = 'sizing_figures'
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)

    fig_type = '.png'   # saves as png

    print("Plotting figures...")
    sys.stdout = open(os.devnull, 'w')


    ############## Plotting figures ##############

    if latex: # Using latex format
        # TOGW vs. S_ref, reference area is the wing area
        S_ref_list = numpy.linspace(S_wing_LO, S_wing_HI, num)
        TOGW_S_ref = [0] * num
        power_loading_1 = [0] * num     # N/W
        wing_loading_1 = [0] * num      # kg/m^2
        P_list = [0] * num

        for i in range(num):
            TOGW_S_ref[i], power_loading_1[i], _, wing_loading_1[i], P_list[i] = sizing_process(Sizing.time_hover_climb, Sizing.time_climb, Sizing.time_cruise, Sizing.time_hover_descent,
                        Sizing.eta_mech, Sizing.eta_p, Sizing.V_hover_climb,
                        Sizing.V_hover_descent, Sizing.V_climb, Sizing.V_cruise,
                        Sizing.f, Sizing.M, Sizing.rho, Sizing.e, Sizing.AR, Sizing.CD0, Sizing.gam_climb, Sizing.distr,
                        Sizing.S_disk, S_ref_list[i], Sizing.S_wetted_fuse,
                        Sizing.rho_battery, Sizing.battery_reserve, Sizing.payload)

        S_ref_list_IM = [0] * num
        TOGW_S_ref_IM = [0] * num
        wing_loading_1_IM = [0] * num
        power_loading_1_IM = [0] * num
        for i in range(num):
            S_ref_list_IM[i] = S_ref_list[i] * 10.7639
            TOGW_S_ref_IM[i] = TOGW_S_ref[i] * 0.224809
            wing_loading_1_IM[i] = wing_loading_1[i] / 10.7639 * 2.20462   # lb/ft^2
            power_loading_1_IM[i] = power_loading_1[i] / 745.7 * 4.44822   # lb/hp


        ### TOGW vs S_wing (S_ref) & wing loading
        # Plot in Imperial Units
        fig1 = plt.figure(1)
        ax1 = fig1.add_subplot(111)
        ax2 = ax1.twiny()
        # ax1.yaxis.grid()
        # ax1.xaxis.grid()
        title = "TOGW vs. Wing Area and Wing Loading in Imperial Units"
        plt.title(title)
        ax1.plot(S_ref_list_IM, TOGW_S_ref_IM, 'b-', label="Wing area")
        ax1.set_xlabel("Wing reference area (ft$^2$)")
        ax2.plot(wing_loading_1_IM, TOGW_S_ref_IM, 'r-', label="Wing loading")
        ax2.set_xlabel("Wing loading (lb/ft$^2$)")
        ax1.set_ylabel("TOGW (lbf)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI units
        fig2 = plt.figure(2)
        ax1 = fig2.add_subplot(111)
        ax2 = ax1.twiny()
        # ax1.yaxis.grid()
        # ax1.xaxis.grid()
        title = "TOGW vs. Wing Area and Wing Loading in SI units"
        plt.title(title)
        ax1.plot(S_ref_list, TOGW_S_ref, 'b-', label="Wing area")
        ax1.set_xlabel("Wing reference area (m$^2$)")
        ax2.plot(wing_loading_1, TOGW_S_ref, 'r-', label="Wing loading")
        ax2.set_xlabel("Wing loading (kg/m$^2$)")
        ax1.set_ylabel("TOGW (N)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Power Loading vs. Wing Loading
        # Plot in Imperial Units
        plt.figure(3)
        plt.plot(wing_loading_1_IM, power_loading_1_IM, 'b-', label="Initial Sizing")
        plt.ylabel("Power loading (lbf/hp)")
        # plt.grid()
        plt.xlabel("Wing loading (lb/ft$^2$)")
        title = "Power Loading vs. Wing Loading in Imperial Units"
        plt.title(title)
        plt.legend(loc="upper left")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in Imperial Units
        plt.figure(4)
        plt.plot(wing_loading_1, power_loading_1, 'b-', label="Initial Sizing")
        plt.ylabel("Power loading (N/W)")
        # plt.grid()
        plt.xlabel("Wing loading (kg/m$^2$)")
        title = "Power Loading vs. Wing Loading in SI units"
        plt.title(title)
        plt.legend(loc="upper left")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### TOGW vs. S_disk & disk loading
        S_disk_list = numpy.linspace(S_disk_LO, S_disk_HI, num)
        TOGW_S_disk = [0] * num
        power_loading_list_SI = [0] * num
        disk_loading_list_SI = [0] * num
        wing_loading_2 = [0] * num
        power = [0] * num

        for i in range(num):
            TOGW_S_disk[i], power_loading_list_SI[i], disk_loading_list_SI[i], wing_loading_2[i], power[i] = sizing_process(Sizing.time_hover_climb, Sizing.time_climb, Sizing.time_cruise, Sizing.time_hover_descent,
                        Sizing.eta_mech, Sizing.eta_p, Sizing.V_hover_climb,
                        Sizing.V_hover_descent, Sizing.V_climb, Sizing.V_cruise,
                        Sizing.f, Sizing.M, Sizing.rho, Sizing.e, Sizing.AR, Sizing.CD0, Sizing.gam_climb, Sizing.distr,
                        S_disk_list[i], Sizing.S_wing, Sizing.S_wetted_fuse,
                        Sizing.rho_battery, Sizing.battery_reserve, Sizing.payload)

        S_disk_list_IM = [0] * num
        TOGW_S_disk_IM = [0] * num
        disk_loading_list_IM = [0] * num
        for i in range(num):
            S_disk_list_IM[i] = S_disk_list[i] * 10.7639
            TOGW_S_disk_IM[i] = TOGW_S_disk[i] * 0.224809
            disk_loading_list_IM[i] = disk_loading_list_SI[i] / 10.7639 * 0.224809

        # Plot in imperial unit
        fig5 = plt.figure(5)
        ax1 = fig5.add_subplot(111)
        ax2 = ax1.twiny()
        # ax1.xaxis.grid()
        # ax1.yaxis.grid()
        ax1.plot(S_disk_list_IM, TOGW_S_disk_IM, 'b-', label="Disk area")
        ax1.set_xlabel("Disk area (ft$^2$)")
        ax2.plot(disk_loading_list_IM, TOGW_S_disk_IM, 'r-', label="Disk loading")
        ax2.set_xlabel("Disk loading (lbf/ft$^2$)")
        title = "TOGW vs. Disk Area and Disk Loading in Imperial Units"
        plt.title(title)
        ax1.set_ylabel("TOGW (lbf)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI unit
        fig6 = plt.figure(6)
        ax1 = fig6.add_subplot(111)
        ax2 = ax1.twiny()
        # ax1.xaxis.grid()
        # ax1.yaxis.grid()
        ax1.plot(S_disk_list, TOGW_S_disk, 'b-', label="Disk area")
        ax1.set_xlabel("Disk area (m$^2$)")
        ax2.plot(disk_loading_list_SI, TOGW_S_disk, 'r-', label="Disk loading")
        ax2.set_xlabel("Disk loading (N/m$^2$)")
        title = "TOGW vs. Disk Area and Disk Loading in SI units"
        plt.title(title)
        ax1.set_ylabel("TOGW (N)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Thrust-to-weight ratio vs. wing loading
        V_num = 5
        rows, cols = (V_num, num)
        T_W = [[0 for i in range(cols)] for j in range(rows)]
        V = numpy.linspace(V_hover_climb, V_cruise, V_num)
        V_IM = numpy.linspace(V_hover_climb * 1.94384, V_cruise * 1.94384, V_num)
        for i in range(rows):
            for j in range(cols):
                T_W[i][j] = eta_p * power[j] / V[i] / TOGW_S_disk[j]

        wing_loading_2_IM = [0] * num
        for i in range(num):
            wing_loading_2_IM[i] = wing_loading_2[i] / 10.7639 * 2.20462    # lb/ft^2

        # Plot in Imperial units
        plt.figure(7)
        for i in range(rows):
            label_val = "$V_\infty$ = " + str(round(V_IM[i], 1)) + " knots"
            plt.semilogy(wing_loading_2_IM, T_W[i], label=label_val)
        title = "Thrust-to-Weight Ratio vs. Wing Loading in Imperial Units"
        plt.title(title)
        # plt.grid()
        plt.ylabel("Thrust-to-weight ratio")
        plt.xlabel("Wing loading (lb/ft$^2$)")
        plt.legend(loc="best")
        plt.legend()
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI units
        plt.figure(8)
        for i in range(rows):
            label_val = "$V_\infty$ = " + str(round(V[i], 1)) + " m/s"
            plt.semilogy(wing_loading_2, T_W[i], label=label_val)
        title = "Thrust-to-Weight Ratio vs. Wing Loading in SI units"
        plt.title(title)
        # plt.grid()
        plt.ylabel("Thrust-to-weight ratio")
        plt.xlabel("Wing loading (kg/m$^2$)")
        plt.legend(loc="best")
        plt.legend()
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Power loading vs. disk loading
        power_loading_list_IM = [0] * num
        disk_loading_list_IM = [0] * num
        for i in range(num):
            power_loading_list_IM[i] = (power_loading_list_SI[i] * 167.64)
            disk_loading_list_IM[i] = disk_loading_list_SI[i] * 0.0208854

        disk_loading_limit_IM = numpy.linspace(min(disk_loading_list_IM), max(disk_loading_list_IM), num)
        disk_loading_limit_SI = [0] * num
        power_loading_limit_IM = [0] * num
        power_loading_limit_SI = [0] * num
        for i in range(num):
            power_loading_limit_IM[i] = (53.3 / numpy.sqrt(disk_loading_limit_IM[i]))
            disk_loading_limit_SI[i] = disk_loading_limit_IM[i] / 0.092903 * 4.44822
            power_loading_limit_SI[i] = power_loading_limit_IM[i] / 745.7 * 4.44822

        # Plot in Imperial unit
        plt.figure(9)
        plt.plot(disk_loading_list_IM, power_loading_list_IM, 'b-', label="Initial Sizing")
        plt.plot(disk_loading_limit_IM, power_loading_limit_IM, 'r-', label="Theoretical Limit")
        title = "Power Loading vs. Disk Loading in Imperial Units"
        plt.title(title)
        # plt.grid()
        plt.ylabel("Power loading (lbf/hp)")
        plt.xlabel("Disk loading (lbf/ft$^2$)")
        plt.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI unit
        plt.figure(10)
        plt.plot(disk_loading_list_SI, power_loading_list_SI, 'b-', label="Initial Sizing")
        plt.plot(disk_loading_limit_SI, power_loading_limit_SI, 'r-', label="Theoretical Limit")
        title = "Power Loading vs. Disk Loading in SI units"
        plt.title(title)
        # plt.grid()
        plt.ylabel("Power loading (N/W)")
        plt.xlabel("Disk loading (N/m$^2$)")
        plt.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

    else: # Not using latex format
        # TOGW vs. S_ref, reference area is the wing area
        S_ref_list = numpy.linspace(S_wing_LO, S_wing_HI, num)
        TOGW_S_ref = [0] * num
        power_loading_1 = [0] * num     # N/W
        wing_loading_1 = [0] * num      # kg/m^2
        P_list = [0] * num

        for i in range(num):
            TOGW_S_ref[i], power_loading_1[i], _, wing_loading_1[i], P_list[i] = sizing_process(Sizing.time_hover_climb, Sizing.time_climb, Sizing.time_cruise, Sizing.time_hover_descent,
                        Sizing.eta_mech, Sizing.eta_p, Sizing.V_hover_climb,
                        Sizing.V_hover_descent, Sizing.V_climb, Sizing.V_cruise,
                        Sizing.f, Sizing.M, Sizing.rho, Sizing.e, Sizing.AR, Sizing.CD0, Sizing.gam_climb, Sizing.distr,
                        Sizing.S_disk, S_ref_list[i], Sizing.S_wetted_fuse,
                        Sizing.rho_battery, Sizing.battery_reserve, Sizing.payload)

        S_ref_list_IM = [0] * num
        TOGW_S_ref_IM = [0] * num
        wing_loading_1_IM = [0] * num
        power_loading_1_IM = [0] * num
        for i in range(num):
            S_ref_list_IM[i] = S_ref_list[i] * 10.7639
            TOGW_S_ref_IM[i] = TOGW_S_ref[i] * 0.224809
            wing_loading_1_IM[i] = wing_loading_1[i] / 10.7639 * 2.20462   # lb/ft^2
            power_loading_1_IM[i] = power_loading_1[i] / 745.7 * 4.44822   # lb/hp


        ### TOGW vs S_wing (S_ref) & wing loading
        # Plot in Imperial Units
        fig1 = plt.figure(1)
        ax1 = fig1.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.yaxis.grid()
        ax1.xaxis.grid()
        title = "TOGW vs. Wing Area & Wing Loading in Imperial Units"
        plt.title(title)
        ax1.plot(S_ref_list_IM, TOGW_S_ref_IM, 'b-', label="Wing area")
        ax1.set_xlabel("Wing reference area (ft^2)")
        ax2.plot(wing_loading_1_IM, TOGW_S_ref_IM, 'r-', label="Wing loading")
        ax2.set_xlabel("Wing loading (lb/ft^2)")
        plt.ylabel("TOGW (lbf)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI units
        fig2 = plt.figure(2)
        ax1 = fig2.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.yaxis.grid()
        ax1.xaxis.grid()
        title = "TOGW vs. Wing Area & Wing Loading in SI units"
        plt.title(title)
        ax1.plot(S_ref_list, TOGW_S_ref, 'b-', label="Wing area")
        ax1.set_xlabel("Wing reference area (m^2)")
        ax2.plot(wing_loading_1, TOGW_S_ref, 'r-', label="Wing loading")
        ax2.set_xlabel("Wing loading (kg/m^2)")
        plt.ylabel("TOGW (N)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Power Loading vs. Wing Loading
        # Plot in Imperial Units
        plt.figure(3)
        plt.plot(wing_loading_1_IM, power_loading_1_IM, 'b-', label="Initial Sizing")
        plt.ylabel("Power loading (lbf/hp)")
        plt.grid()
        plt.xlabel("Wing loading (lb/ft^2)")
        title = "Power Loading vs. Wing Loading in Imperial Units"
        plt.title(title)
        plt.legend(loc="upper left")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in Imperial Units
        plt.figure(4)
        plt.plot(wing_loading_1, power_loading_1, 'b-', label="Initial Sizing")
        plt.ylabel("Power loading (N/W)")
        plt.grid()
        plt.xlabel("Wing loading (kg/m^2)")
        title = "Power Loading vs. Wing Loading in SI units"
        plt.title(title)
        plt.legend(loc="upper left")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### TOGW vs. S_disk & disk loading
        S_disk_list = numpy.linspace(S_disk_LO, S_disk_HI, num)
        TOGW_S_disk = [0] * num
        power_loading_list_SI = [0] * num
        disk_loading_list_SI = [0] * num
        wing_loading_2 = [0] * num
        power = [0] * num

        for i in range(num):
            TOGW_S_disk[i], power_loading_list_SI[i], disk_loading_list_SI[i], wing_loading_2[i], power[i] = sizing_process(Sizing.time_hover_climb, Sizing.time_climb, Sizing.time_cruise, Sizing.time_hover_descent,
                        Sizing.eta_mech, Sizing.eta_p, Sizing.V_hover_climb,
                        Sizing.V_hover_descent, Sizing.V_climb, Sizing.V_cruise,
                        Sizing.f, Sizing.M, Sizing.rho, Sizing.e, Sizing.AR, Sizing.CD0, Sizing.gam_climb, Sizing.distr,
                        S_disk_list[i], Sizing.S_wing, Sizing.S_wetted_fuse,
                        Sizing.rho_battery, Sizing.battery_reserve, Sizing.payload)

        S_disk_list_IM = [0] * num
        TOGW_S_disk_IM = [0] * num
        disk_loading_list_IM = [0] * num
        for i in range(num):
            S_disk_list_IM[i] = S_disk_list[i] * 10.7639
            TOGW_S_disk_IM[i] = TOGW_S_disk[i] * 0.224809
            disk_loading_list_IM[i] = disk_loading_list_SI[i] / 10.7639 * 0.224809

        # Plot in imperial unit
        fig5 = plt.figure(5)
        ax1 = fig5.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.xaxis.grid()
        ax1.yaxis.grid()
        ax1.plot(S_disk_list_IM, TOGW_S_disk_IM, 'b-', label="Disk area")
        ax1.set_xlabel("Disk area (ft^2)")
        ax2.plot(disk_loading_list_IM, TOGW_S_disk_IM, 'r-', label="Disk loading")
        ax2.set_xlabel("Disk loading (lbf/ft^2)")
        title = "TOGW vs. disk area & disk loading in Imperial Units"
        plt.title(title)
        plt.ylabel("TOGW (lbf)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI unit
        fig6 = plt.figure(6)
        ax1 = fig6.add_subplot(111)
        ax2 = ax1.twiny()
        ax1.xaxis.grid()
        ax1.yaxis.grid()
        ax1.plot(S_disk_list, TOGW_S_disk, 'b-', label="Disk area")
        ax1.set_xlabel("Disk area (m^2)")
        ax2.plot(disk_loading_list_SI, TOGW_S_disk, 'r-', label="Disk loading")
        ax2.set_xlabel("Disk loading (N/m^2)")
        title = "TOGW vs. disk area & disk loading in SI units"
        plt.title(title)
        plt.ylabel("TOGW (N)")
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Thrust-to-weight ratio vs. wing loading
        V_num = 5
        rows, cols = (V_num, num)
        T_W = [[0 for i in range(cols)] for j in range(rows)]
        V = numpy.linspace(V_hover_climb, V_cruise, V_num)
        V_IM = numpy.linspace(V_hover_climb * 1.94384, V_cruise * 1.94384, V_num)
        for i in range(rows):
            for j in range(cols):
                T_W[i][j] = eta_p * power[j] / V[i] / TOGW_S_disk[j]

        wing_loading_2_IM = [0] * num
        for i in range(num):
            wing_loading_2_IM[i] = wing_loading_2[i] / 10.7639 * 2.20462    # lb/ft^2

        # Plot in Imperial units
        plt.figure(7)
        for i in range(rows):
            label_val = "V_inf = " + str(round(V_IM[i], 1)) + " knots"
            plt.semilogy(wing_loading_2_IM, T_W[i], label=label_val)
        title = "Thrust-to-weight ratio vs. wing loading in Imperial Units"
        plt.title(title)
        plt.grid()
        plt.ylabel("Thrust-to-weight ratio")
        plt.xlabel("Wing loading (lb/ft^2)")
        plt.legend(loc="best")
        plt.legend()
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI units
        plt.figure(8)
        for i in range(rows):
            label_val = "V_inf = " + str(round(V[i], 1)) + " m/s"
            plt.semilogy(wing_loading_2, T_W[i], label=label_val)
        title = "Thrust-to-weight ratio vs. wing loading in SI units"
        plt.title(title)
        plt.grid()
        plt.ylabel("Thrust-to-weight ratio")
        plt.xlabel("Wing loading (kg/m^2)")
        plt.legend(loc="best")
        plt.legend()
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')


        ### Power loading vs. disk loading
        power_loading_list_IM = [0] * num
        disk_loading_list_IM = [0] * num
        for i in range(num):
            power_loading_list_IM[i] = (power_loading_list_SI[i] * 167.64)
            disk_loading_list_IM[i] = disk_loading_list_SI[i] * 0.0208854

        disk_loading_limit_IM = numpy.linspace(min(disk_loading_list_IM), max(disk_loading_list_IM), num)
        disk_loading_limit_SI = [0] * num
        power_loading_limit_IM = [0] * num
        power_loading_limit_SI = [0] * num
        for i in range(num):
            power_loading_limit_IM[i] = (53.3 / numpy.sqrt(disk_loading_limit_IM[i]))
            disk_loading_limit_SI[i] = disk_loading_limit_IM[i] / 0.092903 * 4.44822
            power_loading_limit_SI[i] = power_loading_limit_IM[i] / 745.7 * 4.44822

        # Plot in Imperial unit
        plt.figure(9)
        plt.plot(disk_loading_list_IM, power_loading_list_IM, 'b-', label="Initial Sizing")
        plt.plot(disk_loading_limit_IM, power_loading_limit_IM, 'r-', label="Theoretical Limit")
        title = "Power loading vs. disk loading in Imperial Units"
        plt.title(title)
        plt.grid()
        plt.ylabel("Power loading (lbf/hp)")
        plt.xlabel("Disk loading (lbf/ft^2)")
        plt.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

        # Plot in SI unit
        plt.figure(10)
        plt.plo(disk_loading_list_SI, power_loading_list_SI, 'b-', label="Initial Sizing")
        plt.plot(disk_loading_limit_SI, power_loading_limit_SI, 'r-', label="Theoretical Limit")
        title = "Power loading vs. disk loading in SI units"
        plt.title(title)
        plt.grid()
        plt.ylabel("Power loading (N/W)")
        plt.xlabel("Disk loading (N/m^2)")
        plt.legend(loc="upper right")
        pathway = './' + my_folder + '/' + title + fig_type
        plt.savefig(pathway, bbox_inches='tight')

    ############## End ##############
    sys.stdout = sys.__stdout__
    print("All figures are successfully stored in the folder: \"" + my_folder + "\"")
    print("Ending program...")



if __name__ == "__main__":

    ############## Assumed values ##############
    # Efficiencies:
    eta_mech = 0.7
    eta_p = 0.8

    # Velocities:
    V_hover_climb = 2.54    #m/s (equivalent to 500 ft/min)
    V_hover_descent = 0 #m/s (equivalent to 300 ft/min descent)
    V_climb = 44            #m/s (equivalent to 85.53 knots)
    V_cruise = 62           #m/s (equivalent to 120.52 knots)

    # Rotor Stuff:
    f = 0.1 # "adjustment for downwash of fuselage"
    M = 0.6 # measure of merit

    S_disk = 20  # m^2 (ROUGH APPROXIMATION, no actual aircraft to compare to)
    S_wing = 26  # m^2 
    S_wetted_fuse = 24.3  # m^2

    # Air Properties:
    rho = 1.05 # Assumed as a kind of "average" over the flight trajectory

    # Geometric and Drag Properties:
    e = 0.75
    AR = 10
    CD0 = 0.02 # Assumed, slightly smaller than C182RG CD0 with landing gear retracted

    # Forward flight climb angle
    gam_climb = numpy.arctan(1/16) # Based on mission requirements

    # Distribution between battery and H2 fuel
    distr = 0 # fully H2, no battery

    # Battery info
    rho_battery = 260  # Wh/kg for high performance battery
    battery_reserve = 0.2 # 20% battery reserve

    climb_1 = 4 * 1609.34       # m
    climb_2 = 2 * 1609.34       # m
    climb_3_time = 4 * 60       # s
    cruise_1 = 7 * 1609.34      # m
    cruise_2 = 15 * 1609.34     # m
    cruise_3 = 30 * 1609.34     # m
    # Distances:
    dist_climb = ((climb_1 + climb_2) + V_climb * climb_3_time)     # m, horizontal dist of climb
    dist_cruise = (cruise_1 + cruise_2 + cruise_3)                  # m

    # Times:
    dist_sac_davis = 24462.03       # m
    time_climb = dist_climb / V_climb
    time_hover_climb = 60 * 2      # s, included hovering when landing aborted
    time_cruise = dist_cruise / V_cruise + dist_sac_davis / V_cruise   # s, included Sac to Davis
    time_hover_descent = 60 * 2

    # Payload mass
    payload = 300       # kg

    # Integrating the class
    initialSizing = Class130.Sizing(eta_mech, eta_p, V_hover_climb, V_hover_descent, V_climb, V_cruise,
     f, M, S_disk, S_wing, S_wetted_fuse, rho, e, AR, CD0, gam_climb, distr,
     rho_battery, battery_reserve, dist_climb, dist_cruise, payload,
     time_climb, time_hover_climb, time_cruise, time_hover_descent)

    # Setting boundaries
    S_wing_LO = 10
    S_wing_HI = 40
    S_disk_LO = 3
    S_dist_HI = 22
    num = 201

    # Calling function
    sizing_figures(initialSizing, S_wing_LO, S_wing_HI, S_disk_LO, S_dist_HI, num)