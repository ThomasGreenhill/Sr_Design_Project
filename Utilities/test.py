import sys
import numpy
import csv
sys.path.append("../Python_Codes")
from Class130 import Airfoil
import mses

path = "./Data/p51d/p51d_geom.dat"
xgeom, ygeom = mses.ReadXfoilGeometry(path)
num = 501
x_list = numpy.linspace(0, 1, num)
yup = [0]*num
ylo = [0]*num
for i, xout in enumerate(x_list):
    yup[i], ylo[i] = mses.MsesInterp(xout, xgeom, ygeom)

x, y = mses.MsesMerge(x_list, x_list, ylo, yup)

with open('././Data/p51d/p51d.dat', 'w', newline='') as f:
    writer = csv.writer(f, delimiter = '\t')
    writer.writerows(zip(x,y))

quit()