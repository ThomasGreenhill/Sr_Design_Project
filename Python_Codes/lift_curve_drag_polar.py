import pandas as pd


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

    


#df = pd.read_csv(filepath, delimiter=',', skiprows=0)
#df1 = df.set_index('alpha', drop=False)
#print(df.head())
