# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys

sys.path.append("../Utilities/")

try:
    import formatfigures
    formatfigures.formatsubfigures()
    formatfigures.formatfigures()
    latex = True
except:
    print("Not using latex formatting")
    latex = False

WE    = [0.6143, 1050.29]
OWE   = [0.5247, 1131.94]
OWE_F = [0.5258, 1136.94]
OWE_P = [0.4307, 1320.24]
GTOW  = [0.4321, 1325.24]

plt.plot(WE[0],    WE[1],    'o', markersize=9, label='Empty')
plt.plot(OWE[0],   OWE[1],   's', markersize=9, label='Operating Weight Empty (OWE)')
plt.plot(OWE_F[0], OWE_F[1], 'd', markersize=9, label='OWE + Fuel')
plt.plot(OWE_P[0], OWE_P[1], '^', markersize=9, label='OWE + Pax/Bags')
plt.plot(GTOW[0],  GTOW[1],  'v', markersize=9, label='Gross Takeoff Weight')
plt.title('C.G. Excursion Diagram')
plt.xlabel('C.G. Location as fraction of $\\bar{c}$ past Wing Root L.E.')
plt.ylabel('Weight (kg)')
plt.yticks(ticks=[1000, WE[1], 1100, OWE[1], 1200, 1300, GTOW[1], 1400],\
           labels=['1000', '$W_E$', '1100', '$OWE$', '1200', '1300', '$W_{TO}$', '1400'])
plt.xlim(0.4, 0.65)
plt.ylim(980, 1400)
plt.legend()
plt.show()