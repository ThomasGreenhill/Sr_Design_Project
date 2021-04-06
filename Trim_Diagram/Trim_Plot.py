import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('../Utilities')
import formatfigures
formatfigures.formatfigures()
savedir = os.path.abspath(os.path.dirname(__file__))

alpha_eva = list(map(float, open("Trim_Data_1.txt", "r").read().split()))
Cmw = list(map(float, open("Trim_Data_2.txt", "r").read().split()))
Cmh = list(map(float, open("Trim_Data_3.txt", "r").read().split()))
Cmf = list(map(float, open("Trim_Data_4.txt", "r").read().split()))
Cm = list(map(float, open("Trim_Data_5.txt", "r").read().split()))

### Reference Line
R = 0*np.linspace(0,15,100)

### Plot
# plt.figure(figsize=(9,6),num=1)
plt.plot(alpha_eva,Cmw,label='Wing')
plt.plot(alpha_eva,Cmh,label='Tail')
plt.plot(alpha_eva,Cmf,label='Fuselage')
plt.plot(alpha_eva,Cm,label='Airplane')
plt.plot(np.linspace(0,15,100),R,'--k')
plt.xlabel(r'$\alpha (^\circ)$')
plt.ylabel(r'$C_{m_\mathrm{CG}}$')
plt.xlim(0,12)
plt.legend(loc="best")
plt.title('Component contributions to pitching moment about CG')
plt.savefig('./Trim_Diagram.png', bbox_inches='tight')
plt.show()