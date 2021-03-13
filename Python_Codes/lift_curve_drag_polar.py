import matplotlib.pyplot as plt
import numpy
import os

# v1.4 FS_data_modified.txt
filepath = '../Sizing/OpenVSP/v1.4_03_05.2021/Flight Stream/Output/FS_data_modified.txt'

with open(filepath, 'r') as fs_file:
    data_list = []
    for ii, line in enumerate(fs_file):
        if ii == 0:
            continue
        cur_str = line.split(',')
        cur_line = [0] * len(cur_str)
        for jj, item in enumerate(cur_str):
            cur1 = item.strip()
            cur2 = cur1.replace('+', '')
            cur_line[jj] = float(cur2)
        data_list.append(cur_line)  # alpha ,Beta ,Velocity ,Cx ,Cy ,Cz ,CL ,CDi ,CDo ,CMx ,CMy ,CMz

    alfs = [0] * len(data_list)
    CLs = [0] * len(data_list)
    CDis = [0] * len(data_list)
    CDos = [0] * len(data_list)
    for ii, cur_line in enumerate(data_list):
        alfs[ii] = data_list[ii][0]
        CLs[ii] = data_list[ii][6]
        CDis[ii] = data_list[ii][7]
        CDos[ii] = data_list[ii][8]

    CLa = (CLs[-1] - CLs[0]) / numpy.deg2rad(alfs[-1] - alfs[0])
    print('Lift curve slope is {:.2f}'.format(CLa))
    print('Theoretical lift curve slope is {:.2f}'.format(2 * numpy.pi))
    alfs_theo = [alfs[2], alfs[-1]]
    CLs_theo = [CLs[2], (2 * numpy.pi) * numpy.deg2rad(alfs[-1] - alfs[2])]

    # lift curve
    plt.figure()
    plt.plot(alfs, CLs, 'r-', label="Lift Curve")
    plt.plot(alfs_theo, CLs_theo, color='blue', linestyle='dotted', label="Lift Curve when AR = inf")
    plt.ylabel(r"Lift coefficient $C_L$")
    plt.grid()
    plt.xlabel(r"Angle of attack $\alpha$ (deg)")
    title = "Lift Curve"
    plt.title(title)
    plt.legend(loc="upper left")
    my_folder = 'Figures/Aerodynamics/v1.4'
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)
    fig_type = '.png'
    version = 'v1.4 '
    pathway = './' + my_folder + '/' + version + title + fig_type
    plt.savefig(pathway, bbox_inches='tight')

    CDs = [0] * len(CLs)
    for ii in range(len(CLs)):
        CDs[ii] = CDis[ii] + CDos[ii]
    # drag polar
    plt.figure()
    plt.plot(CLs, CDs, 'r-', label="Drag Polar")
    plt.ylabel(r"Drag coefficient $C_D$")
    plt.grid()
    plt.xlabel(r"Lift coefficient $C_L$")
    title = "Drag Polar"
    plt.title(title)
    plt.legend(loc="upper left")
    my_folder = 'Figures/Aerodynamics/v1.4'
    if not os.path.exists(my_folder):
        os.makedirs(my_folder)
    fig_type = '.png'
    version = 'v1.4 '
    pathway = './' + my_folder + '/' + version + title + fig_type
    plt.savefig(pathway, bbox_inches='tight')


