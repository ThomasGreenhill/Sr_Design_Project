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

Emrax188_HV_CC_Q = numpy.array([[45],
                                    [49],
                                    [52],
                                    [52.5],
                                    [52],
                                    [50],
                                    [48]])


x = Emrax188_HV_CC[:,0]
y = Emrax188_HV_CC[:,1]/Emrax188_HV_CC[6,1]
z = Emrax188_HV_CC_Q[:,0]/max(Emrax188_HV_CC_Q)

xx = numpy.linspace(x.min(),x.max(),100)
yy = sci.CubicSpline(x,y)
zz = sci.CubicSpline(x,z)

plt.figure(figsize=(14, 12))
plt.subplot(2,1,1)
plt.plot(xx, yy(xx))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Power")

plt.title("Normalized Torque vs. Angular Rate for General 3-Phase Motor \n Based on EMRAX 188C Motor")

plt.subplot(2,1,2)
plt.plot(xx, zz(xx))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Torque")
plt.ylim((0,1.05))


plt.tight_layout()
plt.savefig('./Figures/motor_performance_general.png', bbox_inches='tight')
plt.show()