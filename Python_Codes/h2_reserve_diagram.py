# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import sys
sys.path.append("../Utilities")
import numpy

try:
    import formatfigures
    formatfigures.formatsubfigures()
    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False
    
t_hc = 60
t_fc1 = 146.3
t_cr1 = 181.7
t_fc2 = 73.15
t_cr2 = 389.36
t_fc3 = 225.22
t_mcr = 752.76
t_fd = 259.57
t_hd = 60
t_hcal = 60
t_crdiv = 389.36
t_hdal = 60

ts = [t_fc1, t_cr1, t_fc2, t_cr2, t_fc3, t_mcr, t_fd, t_hd, t_hcal, t_crdiv, t_hdal]

t_vec = [0, t_hc, t_hc]

for t in ts:
    t_add = t_vec[len(t_vec)-1]+t
    t_vec.append(t_add)
    if len(t_vec) < 23:
        t_vec.append(t_add)

t_vec = numpy.array(t_vec)

e_total = 5
e_drain = 100e3/(120e6*0.57)
e_time  = e_total - t_vec*e_drain
e_reserve = 0.1*5

plt.figure(figsize=(16,9))
plt.fill_between(t_vec/3600, e_total*numpy.ones(numpy.size(t_vec)), e_time, color=(0.2,0.2,0.2), alpha=0.5)
plt.fill_between(t_vec/3600, e_reserve*numpy.ones(numpy.size(t_vec)), e_time,color=(67/255, 217/255, 0), alpha=0.7, label="Hydrogen Fuel Available")
plt.fill_between(t_vec/3600, e_reserve*numpy.ones(numpy.size(t_vec)),color=(1,0,0),alpha=0.7,label="Minimum Fuel")
plt.plot(t_vec/3600, e_total*numpy.ones(numpy.size(t_vec)), 'k',label = "Full Tank")

plt.plot((2148.06/3600, 2148.06/3600),(0,7),'k--',label="Divert")
plt.ylim((0,6.5))
plt.ylabel("Hydrogen Fuel (kg)")
plt.xlabel("Time (h)")
plt.title("Hydrogen Reserves Over Mission")

plt.legend(loc='upper center')
# plt.savefig('./Figures/battery_energy.png', bbox_inches='tight')
plt.show()