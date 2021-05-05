import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append('../Utilities')
import formatfigures
formatfigures.formatfigures()
savedir = os.path.abspath(os.path.dirname(__file__))

alpha_eva = np.array(list(map(float, open("Trim_Data_1.txt", "r").read().split())))
Cmw = np.array(list(map(float, open("Trim_Data_2.txt", "r").read().split())))
Cmh = np.array(list(map(float, open("Trim_Data_3.txt", "r").read().split())))
Cmf = np.array(list(map(float, open("Trim_Data_4.txt", "r").read().split())))
Cm = np.array(list(map(float, open("Trim_Data_5.txt", "r").read().split())))

### Reference Line
R = 0*np.linspace(0,15,100)

Cm0 = 0.05
Cma = -0.697963 * 1/(180/np.pi)
Cm = Cm0 + Cma * alpha_eva

Cmf = Cm - (Cmh + Cmw)

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
plt.title('Component Contributions to Pitching Moment About \n CG vs. Angle of Attack')
plt.savefig('./Trim_Diagram_alpha.png', bbox_inches='tight')

CL_eva = np.array(alpha_eva)/(2*np.pi)
plt.figure()
plt.plot(CL_eva,Cmw,label='Wing')
plt.plot(CL_eva,Cmh,label='Tail')
plt.plot(CL_eva,Cmf,label='Fuselage')
plt.plot(CL_eva,Cm,label='Airplane')
plt.plot(np.linspace(0,15,100),R,'--k')
plt.xlabel(r'$C_L$')
plt.ylabel(r'$C_{m_\mathrm{CG}}$')
plt.xlim(0,2)
plt.legend(loc="best")
plt.title('Component Contributions to Pitching Moment About \n CG vs. Lift Coefficient')
plt.savefig('./Trim_Diagram_CL.png', bbox_inches='tight')
plt.show()