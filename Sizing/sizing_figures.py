
import numpy
import matplotlib.pyplot as plt
from sizing_process import sizing_process
#import sys
#sys.path.append("../Utilities")
#import formatfigures
#formatfigures.formatfigures()

# Initial input (as tested in sizing_process.py)


# Efficiencies:
eta_mech = 0.9
eta_p = 0.85

# Velocities:
V_hover_climb = 2.54    #m/s (equivalent to 500 ft/min)
V_hover_descent = -1.52 #m/s (equivalent to 300 ft/min descent)
V_climb = 44            #m/s (equivalent to 85.53 knots)
V_cruise = 62           #m/s (equivalent to 120.52 knots)

# Rotor Stuff:
f = 0.1 # "adjustment for downwash of fuselage"
M = 0.8 # measure of merit

# Reference Areas:
S_disk = 6      #m^2 (ROUGH APPROXIMATION, no actual aircraft to compare to)
S_wing = 16.2   #m^2 (taken from Cessna 172)
S_wetted_fuse = 24.3 #m^2 (taken from Cessna 182RG)

# Air Properties:
rho = 1.05 # Assumed as a kind of "average" over the flight trajectory

# Geometric and Drag Properties:
e = 0.75
AR = 9
CD0 = 0.02 # Assumed, slightly smaller than C182RG CD0 with landing gear retracted

# Forward flight climb angle
gam_climb = numpy.arctan(1/20) # Based on mission requirements

# Distribution between battery and H2 fuel
distr = 0 # fully H2, no battery

# Battery info
rho_battery = 260 #Wh/kg for high performance battery
battery_reserve = 0.2 # 20% battery reserve


# Distances:
dist_climb = ((4 + 2) * 1609.34 + 44 * 4 * 60)          # m
dist_cruise = (7 + 15 + 30) * 1609.34                   # m

# Times:
time_climb = dist_climb / 44
time_hover_climb = 60 * 2    # s, included hovering when landing aborted
time_cruise = dist_cruise / 44 + 2600   # included Sac to Davis
time_hover_descent = 120

# Payload:
payload = 3*100 #kg



###########################################
num = 101
# TOGW vs. S_ref, reference area is the wing area
S_ref_list = numpy.linspace(10, 20, num)
TOGW_S_ref = [0] * num

for i in range(num):
    TOGW_S_ref[i], _, _ = sizing_process(time_hover_climb, time_climb, time_cruise, time_hover_descent,
                eta_mech, eta_p, V_hover_climb,
                V_hover_descent, V_climb, V_cruise,
                f, M, rho, e, AR, CD0, gam_climb, distr,
                S_disk, S_ref_list[i], S_wetted_fuse,
                rho_battery, battery_reserve, payload)

# Plot
plt.figure(1)
plt.plot(S_ref_list, TOGW_S_ref)
plt.ylabel("TOGW (N)")
plt.xlabel("Wing reference area (m^2)")

# TOGW vs. S_disk
S_disk_list = numpy.linspace(1, 15, num)
TOGW_S_disk = [0] * num
power_loading_list = [0] * num
disk_loading_list = [0] * num

for i in range(num):
    TOGW_S_disk[i], power_loading_list[i], disk_loading_list[i] = sizing_process(time_hover_climb, time_climb, time_cruise, time_hover_descent,
                eta_mech, eta_p, V_hover_climb,
                V_hover_descent, V_climb, V_cruise,
                f, M, rho, e, AR, CD0, gam_climb, distr,
                S_disk_list[i], S_wing, S_wetted_fuse,
                rho_battery, battery_reserve, payload)

# Plot
plt.figure(2)
plt.plot(S_disk_list, TOGW_S_disk)
plt.ylabel("TOGW (N)")
plt.xlabel("Disk area (m^2)")

# Power loading vs. disk loading
power_loading_list_new = [0] * num
disk_loading_list_new = [0] * num
for i in range(num):
    power_loading_list_new[i] = power_loading_list[i] * 167.64
    disk_loading_list_new[i] = disk_loading_list[i] * 0.0208854

disk_loading_limit = numpy.linspace(min(disk_loading_list_new), max(disk_loading_list_new), num)
power_loading_limit = [0] * num
for i in range(num):
    power_loading_limit[i] = 53.3 / numpy.sqrt(disk_loading_limit[i])

plt.figure(3)
plt.plot(disk_loading_list_new, power_loading_list_new)
plt.plot(disk_loading_limit, power_loading_limit)
plt.title("Power loading vs. disk loading in imperial units")
plt.grid()
plt.ylabel("Power loading (lbf/hp)")
plt.xlabel("Disk loading (lbf/ft^2)")
plt.show()









'''
print("Running the test of \"sizing_process\" function")
TOGW = sizing_process(time_hover_climb, time_climb, time_cruise, time_hover_descent,
                eta_mech, eta_p, V_hover_climb, 
                V_hover_descent, V_climb, V_cruise, 
                f, M, rho, e, AR, CD0, gam_climb, distr,
                S_disk, S_wing, S_wetted_fuse, 
                rho_battery, battery_reserve)
print("The converged TOGW is " + str(TOGW) + " N")
'''