## Set-up



import numpy as np

import matplotlib.pyplot as plt

import sys

import os
sys.path.append("../Utilities")

savedir = os.path.abspath(os.path.dirname(__file__))



try:

    import formatfigures

    formatfigures.formatsubfigures()

    latex = True

except:

    pass

    print("Not using latex formatting")

    latex = False





###################### Turning Diagram ######################

from VnDF import Cal_Vs

from VnDF import SLLF

from VnDF import SLtr

from VnDF import ALLF

from VnDF import ALtr



#### Parameters

W =  2922.5 #lbf = 13000 N

n_max =  2.1+(24000/(W+10000)) # formula provided by FAR part 23

n_min =  -0.4*n_max # formula provided by FAR part 23

S =  172.27 #ft^2

rho = 0.00237 #slug/ft^3

CL_max = 1.8 # Based on FS data

CL_min = -1.6 # Best guess

unit = 'e' # English units



#### Calculation

VC = 203.41 #ft/s = 62 m/s

VD = VC*1.3/0.9 # Best guess

Vmax =  VD; V = np.linspace(0,Vmax,400) # Vmax can be taken as V_D  ## Put Value HERE for Vmax

Vs = Cal_Vs(W,S,rho,CL_max)

VA = np.sqrt(n_max)*Vs

n_SL = SLLF(V, n_max)

n_AL = ALLF(V,Vs)

Rmin_SL = SLtr(V, n_max, unit)

Rmin_AL = ALtr(V, Vs, unit)



#### Make plots

g, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False, figsize=(10,8))

########## Subplot 1
ax1.set_title("Load Factor and Turn Radius vs. Airspeed with Aerodynamic and Structural Limits", y=1.1)

ax1.plot(V, n_SL, 'r-', label="Structural Limits")
ax1.plot(V, n_AL, 'b-.')

ax1.set_ylabel(r'Load Factor $n$') 

ax1.vlines(x = Vs, ymin=-0.1, ymax=n_max*1.2, colors='k', linestyles='--',label="Aerodynamic Limits")

ax1.vlines(x = VA, ymin=-0.1, ymax=n_max*1.2, colors='k', linestyles='--')

ax1.set_xlim([0.6*Vs, VA*1.2]); ax1.set_ylim([0, n_max*1.2])

########## Subplot 2

ax2.plot(V, Rmin_SL, 'r-', label="Structural Limits")
ax2.plot(V, Rmin_AL, 'b-.', )

ax2.set_ylabel(r'Turn Radius $R$ (ft)') 

ax2.vlines(x = Vs, ymin=-0.1, ymax=2000, colors='k', linestyles='--',label="Aerodynamic Limits")

ax2.vlines(x = VA, ymin=-0.1, ymax=2000, colors='k', linestyles='--')

ax2.set_xlim([0.6*Vs, VA*1.2]); ax2.set_ylim([0, 2000])
ax2.legend(loc='upper center')

######### Notations

g.text(0.5, 0.06, r'Airspeed $V$', ha='center')

g.text(Vs/(1.2*VA)+0.12-0.6*Vs/(1.2*VA), 0.89, str(round(Vs*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
g.text(Vs/(1.2*VA)+0.12-0.6*Vs/(1.2*VA), 0.06, r'$V_s$', ha='center') # The location of the notation can be adjusted 

g.text(VA/(1.2*VA)+0.14-0.6*Vs/(1.2*VA), 0.89, str(round(VA*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
g.text(VA/(1.2*VA)+0.14-0.6*Vs/(1.2*VA), 0.06, r'$V_A$', ha='center') # The location of the notation can be adjusted 

plt.gca().axes.get_xaxis().set_visible(False)


plt.savefig('%s/Figure_TD.png'%(savedir))


############################################################



###################### Maneuvering Diagram ###################### 

from VnDF import Vspn



#### Calculation

Vsp, Vsn = Vspn(W,S,rho,CL_max,CL_min)

Vsnn = np.linspace(0,Vmax,400)

n_positive = np.minimum((Vsnn/Vsp)**2,n_max)

n_negative = np.maximum(-(Vsnn/Vsn)**2,n_min)





#### Plot Preparation

xr = [Vsp, Vsp, Vsn, Vsn]; yr = [1, 0, 0, -1]

#### Make plots

plt.figure(figsize=(10,8))

plt.plot(Vsnn, n_positive, 'k', Vsnn, n_negative, 'k')

plt.plot(xr,yr,'r-')

plt.axis([0, Vmax, -1.2*n_max, 1.2*n_max])

plt.vlines(x = VA, ymin=-1.2*n_max, ymax=1.2*n_max, colors='k', linestyles='--')

plt.vlines(x = Vsp, ymin=-1.2*n_max, ymax=1.2*n_max, colors='k', linestyles='--')

plt.vlines(x = Vsn, ymin=-1.2*n_max, ymax=1.2*n_max, colors='k', linestyles='--')

plt.title('V-n Maneuver Diagram', y=1.04)

plt.text(VA, n_max+0.9, str(round(VA*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VA, -1.2*n_max-0.25, r'$V_A$', ha='center') # The location of the notation can be adjusted

plt.text(Vsp-8, n_max+0.9, str(round(Vsp*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(Vsp-3, -1.2*n_max-0.25, r'$V_{s_{1}}$', ha='center') # The location of the notation can be adjusted

plt.text(Vsn+10, n_max+0.9, str(round(Vsn*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(Vsn+5, -1.2*n_max-0.25, r'$V_{s_{-1}}$', ha='center') # The location of the notation can be adjusted

plt.text(Vmax*0.95, -1.2*n_max-0.25, r'Equivalent Airspeed $V_e$', ha='center') # The location of the notation can be adjusted

plt.ylabel(r'Load Factor $n$') 

plt.gca().axes.get_xaxis().set_visible(False)

plt.savefig('%s/Figure_MD.png'%(savedir))

# plt.show()

################################################################## 



###################### Gust Diagram ######################  

#### Continue to use V in section 1

from VnDF import Calc_Vgust

c_av = 4.15 #ft

CLa = 2*np.pi #per rad

mu = 2*W/S/(rho*c_av*2*np.pi*32.17)

Kg = 0.88*mu/(5.4+mu)

VS1 = 88.58 #ft/s = 27 m/s

Uref = 25 #ft/s (reference gust speed)

VB = 2.1*VS1*(1+Kg*Uref*VC*CLa/(498*W))**(0.5) # just need to be no less than the value of equation

n_GD = []; V_GD = [VB,VC,VD]; condition = ['B','C','D']

for Vr,c in zip(V_GD,condition):

    n_GD.append(Calc_Vgust(Vr,W,S,rho,c_av,CLa,c))

n_GD.insert(0,1); V_GD.insert(0,0)

#### Make plots

plt.figure(figsize=(10,8))

plt.plot(V_GD,n_GD,'k') # for positive Ude

plt.plot(V_GD,2*np.ones(len(n_GD))-n_GD,'k') # for negative Ude

plt.axis([0, 1.2*Vmax, -n_max+1, n_max+1])

plt.vlines(x = VB, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = VC, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = VD, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.text(VB-8, n_max+1.1, str(round(VB*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VB, -n_max+0.75, r'$V_B$', ha='center') # The location of the notation can be adjusted

plt.text(VC+8, n_max+1.1, str(round(VC*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VC, -n_max+0.75, r'$V_C$', ha='center') # The location of the notation can be adjusted

plt.text(VD, n_max+1.1, str(round(VD*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VD, -n_max+0.75, r'$V_D$', ha='center') # The location of the notation can be adjusted

plt.text(Vmax*0.95*1.2, -n_max+0.25, r'Equivalent Airspeed $V_e$', ha='center') # The location of the notation can be adjusted

plt.title('V-n Gust Diagram', y=1.04)

plt.ylabel(r'Load Factor $n$') 

plt.gca().axes.get_xaxis().set_visible(False)

plt.savefig('%s/Figure_GD.png'%(savedir))

# plt.show()

##########################################################



###################### Composite V-n Diagram ######################  

plt.figure(figsize=(10,8))

#### From PART B

plt.plot(Vsnn, n_positive, 'k', Vsnn, n_negative, 'k')

plt.plot(xr,yr,'r-')

plt.vlines(x = VA, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = Vsp, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = Vsn, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.title('Generic V-n maneuver diagram')

plt.text(VA-12, n_max+1.1, str(round(VA*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VA, -n_max+0.75, r'$V_A$', ha='center') # The location of the notation can be adjusted

plt.text(Vsp-10, n_max+1.1, str(round(Vsp*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(Vsp-3, -n_max+0.75, r'$V_{s_{1}}$', ha='center') # The location of the notation can be adjusted

plt.text(Vsn+12, n_max+1.1, str(round(Vsn*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(Vsn+5, -n_max+0.75, r'$V_{s_{-1}}$', ha='center') # The location of the notation can be adjusted

#### From PART C

plt.plot(V_GD,n_GD,'k') # for positive Ude

plt.plot(V_GD,2*np.ones(len(n_GD))-n_GD,'k') # for negative Ude

plt.vlines(x = VB, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = VC, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.vlines(x = VD, ymin=-n_max+1, ymax=n_max+1, colors='k', linestyles='--')

plt.text(VB, n_max+1.3, str(round(VB*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VB, -n_max+0.75, r'$V_B$', ha='center') # The location of the notation can be adjusted

plt.text(VC+8, n_max+1.1, str(round(VC*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VC, -n_max+0.75, r'$V_C$', ha='center') # The location of the notation can be adjusted

plt.text(VD, n_max+1.1, str(round(VD*0.592484,1))+" kn", ha='center') # The location of the notation can be adjusted
plt.text(VD, -n_max+0.75, r'$V_D$', ha='center') # The location of the notation can be adjusted

plt.axis([0, Vmax*1.2, -n_max+1, n_max+1])

plt.title('Composite V-n gust diagram',y=1.05)

plt.text(Vmax*0.95*1.3, -n_max+0.75, r'Equivalent Airspeed $V_e$', ha='center') # The location of the notation can be adjusted

plt.ylabel(r'Load Factor $n$') 

plt.gca().axes.get_xaxis().set_visible(False)

plt.savefig('%s/Figure_CD.png'%(savedir))

plt.show()





###################################################################