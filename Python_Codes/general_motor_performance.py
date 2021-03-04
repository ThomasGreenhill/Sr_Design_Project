# Quick plotting utility to show the normalized performance of 

import numpy
import matplotlib.pyplot as plt
import sys
sys.path.append("../Utilities")

import scipy.interpolate as sci

try:
    import formatfigures
    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

Emrax188_HV_CC = numpy.array([[0, 0],
                                         [1000, 5000],
                                         [2000, 10500],
                                         [3000, 16000],
                                         [4000, 22000],
                                         [5000, 26000],
                                         [6000, 28000]])

x = Emrax188_HV_CC[:,0]*4/6
y = Emrax188_HV_CC[:,1]/Emrax188_HV_CC[6,1]

xx = numpy.linspace(x.min(),x.max(),100)
yy = sci.CubicSpline(x,y)

plt.plot(xx, yy(xx))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Power")
plt.title("Normalized Power vs. Angular Rate for General 3-Phase Motor")
plt.savefig('./Figures/motor_performance.png', bbox_inches='tight')
plt.show()