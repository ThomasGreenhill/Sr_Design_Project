# Quick plotting utility to show the normalized performance of electric motor
# TVG 03.07.2021

import scipy.interpolate as sci
import numpy
import matplotlib.pyplot as plt
import sys
sys.path.append("../Utilities")


try:
    import formatfigures
    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

Emrax188_HV_CC = numpy.array([[0, 0, 45],
                              [1000, 5000, 49],
                              [2000, 10500, 52],
                              [3000, 16000, 52.5],
                              [4000, 22000, 52],
                              [5000, 26000, 50],
                              [6000, 28000, 48]])


def cubicinterp(x, y, z):
    xx = numpy.linspace(x.min(), x.max(), 100)
    yy = sci.CubicSpline(x, y)
    zz = sci.CubicSpline(x, z)

    return xx, yy, zz


x = Emrax188_HV_CC[:, 0]
y = Emrax188_HV_CC[:, 1]/Emrax188_HV_CC[6, 1]
z = Emrax188_HV_CC[:, 2]/max(Emrax188_HV_CC[:, 2])
xx1, yy1, zz1 = cubicinterp(x, y, z)

plt.figure(figsize=(14, 12))
plt.subplot(2, 1, 1)
plt.plot(xx1, yy1(xx1))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Power")

plt.title("Normalized Torque vs. Angular Rate for General 3-Phase Motor \n Based on EMRAX 188C Motor")

plt.subplot(2, 1, 2)
plt.plot(xx1, zz1(xx1))
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Torque")
plt.ylim((0, 1.05))


plt.tight_layout()
plt.savefig('./Figures/motor_performance_general.png', bbox_inches='tight')

# Comparison between different motors
HPDM_250 = numpy.array([[0, 0, 120],
                        [4000, 50000, 120],
                        [8000, 100000, 120],
                        [12000, 150000, 120],
                        [16000, 190000, 115],
                        [20000, 205000, 100]])

x = HPDM_250[:, 0]/max(HPDM_250[:, 0])*max(Emrax188_HV_CC[:, 0])
y = HPDM_250[:, 1]/max(HPDM_250[:, 1])
z = HPDM_250[:, 2]/max(HPDM_250[:, 2])
xx2, yy2, zz2 = cubicinterp(x, y, z)

MAGNIX_250 = numpy.array([[0, 0, 1100],
                          [1000, 96.66, 1400],
                          [2000, 193.33, 1400],
                          [3000, 290, 1400]])

x = MAGNIX_250[:, 0]/max(MAGNIX_250[:, 0])*max(Emrax188_HV_CC[:, 0])
y = MAGNIX_250[:, 1]/max(MAGNIX_250[:, 1])
z = MAGNIX_250[:, 2]/max(MAGNIX_250[:, 2])
xx3, yy3, zz3 = cubicinterp(x, y, z)

plt.figure(figsize=(14, 12))
plt.subplot(2, 1, 1)
plt.plot(xx1, yy1(xx1), label='EMRAX')
plt.plot(xx2, yy2(xx2), "--", label='H3X')
plt.plot(xx3, yy3(xx3), "-.", label='MAGNIX')
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Power")
plt.legend()

plt.title("Comparison of Normalized Torque vs. Angular Rate for Different Motors")

plt.subplot(2, 1, 2)
plt.plot(xx1, zz1(xx1), label='EMRAX')
plt.plot(xx2, zz2(xx2), "--", label='H3X')
plt.plot(xx3, zz3(xx3), "-.", label='MAGNIX')
plt.xlabel("Angular Rate (RPM) ")
plt.ylabel("Normalized Torque")
plt.ylim((0, 1.05))
plt.legend()

plt.tight_layout()
plt.savefig('./Figures/motor_performance_comparison.png', bbox_inches='tight')

plt.show()
