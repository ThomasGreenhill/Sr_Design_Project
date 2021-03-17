# Code to plot the power during each phase of flight and battery energy
# TVG 03.07.2021

import matplotlib.pyplot as plt
import sys
sys.path.append("../Utilities")
import numpy

try:
    import formatfigures
    formatfigures.formatsubfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False


p_hc = 44128
p_fc1 = 11e3
p_cr1 = 7e3
p_fc2 = 15e3
p_cr2 = 7e3
p_fc3 = 145e2
p_mcr = 7e3
p_fd = 0
p_hd = 35873
p_hcal = 44128
p_crdiv = 7e3
p_hdal = 35873

RPM_hc = 2500
RPM_fc1 = 800
RPM_cr1 = 500
RPM_fc2 = 1100
RPM_cr2 = 500
RPM_fc3 = 1000
RPM_mcr = 500
RPM_fd = 0
RPM_hd = 2500
RPM_hcal = 2500
RPM_crdiv = 500
RPM_hdal = 2500

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

eta_m = 0.75
p_vec = numpy.array([p_hc, p_hc, p_fc1, p_fc1, p_cr1, p_cr1, p_fc2, p_fc2, p_cr2, p_cr2, p_fc3, p_fc3, p_mcr, p_mcr, p_fd, p_fd, p_hd, p_hd, p_hcal, p_hcal, p_crdiv, p_crdiv, p_hdal, p_hdal])
# p_vec = [item*(8/eta_m) for item in p_vec]

# Total power require from power system:
p_vec *= 8/eta_m

RPM_vec = numpy.array([RPM_hc, RPM_hc, RPM_fc1, RPM_fc1, RPM_cr1, RPM_cr1, RPM_fc2, RPM_fc2, RPM_cr2, RPM_cr2, RPM_fc3, RPM_fc3, RPM_mcr, RPM_mcr, RPM_fd, RPM_fd, RPM_hd, RPM_hd, RPM_hcal, RPM_hcal, RPM_crdiv, RPM_crdiv, RPM_hdal, RPM_hdal])

# Plot power and RPM vs Time
plt.figure()
plt.subplot(2,1,1)
plt.plot(t_vec,p_vec)
plt.plot((t_vec[17], t_vec[17]),(min(p_vec)-10000,1.2*max(p_vec)),'k--',label="Divert")
plt.ylim((min(p_vec)-10000,1.2*max(p_vec)))
plt.axvline(x=0, color='k')
plt.axhline(y=0, color='k')
plt.gca().set_title("Power Consumption of Entire Aircraft Throughout Mission (Normal Operation)")
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.legend()

plt.subplot(2,1,2)
plt.plot(t_vec,RPM_vec)
plt.plot((t_vec[17], t_vec[17]),(min(RPM_vec)-100,1.2*max(RPM_vec)),'k--',label="Divert")
plt.ylim((min(RPM_vec)-100,1.2*max(RPM_vec)))
plt.gca().set_title("Propeller/Motor RPM Throughout Mission (Normal Operation)")
plt.xlabel("Time (s)")
plt.ylabel("RPM")
plt.axvline(x=0, color='k')
plt.axhline(y=0, color='k')
plt.legend()
plt.tight_layout(rect=(0, 0, 1, 0.92))
plt.suptitle("Power Consumption of Aircraft (assuming $\eta_{{mech}}$ = {}), \n and Propeller/Motor RPM Throughout Mission".format(eta_m), fontsize=24)
plt.savefig('./Figures/power_consumption.png', bbox_inches='tight')


# Plot battery energy consumption vs time
try:
    import formatfigures
    formatfigures.formatfigures()
    latex = True
except:
    pass
    print("Not using latex formatting")
    latex = False

e_ini = 30e3
p_h2 = 100e3
p_batt_vec = p_vec-p_h2
t_temp = numpy.linspace(min(t_vec),max(t_vec),1001)
p_batt_vec = numpy.interp(t_temp,t_vec,p_batt_vec)
t_vec = t_temp
e_max = 35e3

# Plot the battery power 
plt.figure(figsize=(16,9))
plt.plot(t_vec,p_batt_vec)
plt.plot((2148.06, 2148.06),(min(p_batt_vec)-10000,1.2*max(p_batt_vec)),'k--',label="Divert")
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.ylim((min(p_batt_vec)-10000,1.2*max(p_batt_vec)))
plt.gca().set_title("Power Consumption of Battery Throughout Mission (Normal Operation)")
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.legend()
plt.savefig('./Figures/battery_power_consumption.png', bbox_inches='tight')

print("Max Discharge Rate C: {}".format(max(p_batt_vec)/e_max))
print("Max Charge Rate C: {}".format(min(p_batt_vec)/e_max))

e_batt_vec = numpy.zeros(numpy.size(p_batt_vec))
for ii in range(0,len(p_batt_vec)):
    e_batt_vec[ii] = e_ini-numpy.trapz(p_batt_vec[0:ii], t_vec[0:ii]/3600)
plt.figure(figsize=(16,9))
plt.fill_between(t_vec/3600, e_batt_vec, 0.2*e_max*numpy.ones(numpy.size(t_vec)), color=(67/255, 217/255, 0),alpha=0.7,label="Battery Charge Available")
plt.fill_between(t_vec/3600, e_batt_vec, e_max*numpy.ones(numpy.size(e_batt_vec)),color=(0.2,0.2,0.2),alpha=0.5)
plt.plot(t_vec/3600, e_max*numpy.ones(numpy.size(e_batt_vec)), 'k',label = "Full Charge")
plt.fill_between(t_vec/3600, 0.2*e_max*numpy.ones(numpy.size(t_vec)),color=(1,0,0),alpha=0.7,label="Battery Reserve")
plt.plot((2148.06/3600, 2148.06/3600),(0,1.4*max(e_batt_vec)),'k--',label="Divert")
plt.ylim((0,1.4*max(e_batt_vec)))
plt.ylabel("Battery Energy (Wh)")
plt.xlabel("Time (h)")
plt.title("Battery Energy Over Mission")

plt.legend(loc='upper center')
plt.savefig('./Figures/battery_energy.png', bbox_inches='tight')
plt.show()

