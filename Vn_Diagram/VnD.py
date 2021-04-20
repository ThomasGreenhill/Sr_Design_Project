## Set-up

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
savedir = os.path.abspath(os.path.dirname(__file__))


###################### Turning Diagram ######################
from VnDF import Cal_Vs
from VnDF import SLLF
from VnDF import SLtr
from VnDF import ALLF
from VnDF import ALtr

#### Parameters
n_max =  ## Put Value HERE
n_min =  ## Put Value HERE
W =  ## Put Value HERE
S =  ## Put Value HERE
rho =  ## Put Value HERE
CL_max =  ## Put Value HERE
CL_min =  ## Put Value HERE
unit =  ## Put Value HERE

#### Calculation
Vmax =  200; V = np.linspace(0,Vmax,400) # Vmax can be taken as V_D  ## Put Value HERE for Vmax
Vs = Cal_Vs(W,S,rho,CL_max)
VA = np.sqrt(n_max)*Vs
n_SL = SLLF(V, n_max)
n_AL = ALLF(V,Vs)
Rmin_SL = SLtr(V, n_max, unit)
Rmin_AL = ALtr(V, Vs, unit)

#### Make plots
g, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False, figsize=(10,4))
########## Subplot 1
ax1.plot(V, n_SL, 'r-', V, n_AL, 'b--')
ax1.set_ylabel(r'Load Factor $n$') 
ax1.vlines(x = Vs, ymin=-0.1, ymax=4, colors='k', linestyles='--')
ax1.vlines(x = VA, ymin=-0.1, ymax=4, colors='k', linestyles='--')
ax1.set_xlim([0, 200]); ax1.set_ylim([0, 4])
########## Subplot 2
ax2.plot(V, Rmin_SL, 'r-', V, Rmin_AL, 'b--')
ax2.set_ylabel(r'Turn Radius $R$') 
ax2.vlines(x = Vs, ymin=-0.1, ymax=2000, colors='k', linestyles='--')
ax2.vlines(x = VA, ymin=-0.1, ymax=2000, colors='k', linestyles='--')
ax2.set_xlim([0, 200]); ax2.set_ylim([0, 2000])
######### Notations
g.text(0.5, 0.02, r'Airspeed $V$', ha='center')
g.text(Vs/Vmax+0.025, 0.06, r'$V_s$', ha='center') # The location of the notation can be adjusted 
g.text(VA/Vmax+0.010, 0.06, r'$V_A$', ha='center') # The location of the notation can be adjusted 
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig('%s/Figure_TD.png'%(savedir))
plt.show()
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
plt.figure(figsize=(9, 3))
plt.plot(Vsnn, n_positive, 'k', Vsnn, n_negative, 'k')
plt.plot(xr,yr,'r-')
plt.axis([0, 200, -2, 2])
plt.vlines(x = VA, ymin=-2, ymax=2, colors='k', linestyles='--')
plt.vlines(x = Vsp, ymin=-2, ymax=2, colors='k', linestyles='--')
plt.vlines(x = Vsn, ymin=-2, ymax=2, colors='k', linestyles='--')
plt.title('Generic V-n maneuver diagram')
plt.text(VA, -2.25, r'$V_A$', ha='center') # The location of the notation can be adjusted
plt.text(Vsp, -2.25, r'$V_{s_{1}}$', ha='center') # The location of the notation can be adjusted
plt.text(Vsn, -2.25, r'$V_{s_{-1}}$', ha='center') # The location of the notation can be adjusted
plt.text(Vmax*0.9, -2.25, r'Equivalent Airspeed $V_e$', ha='center') # The location of the notation can be adjusted
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig('%s/Figure_MD.png'%(savedir))
plt.show()
################################################################## 

###################### Gust Diagram ######################  
#### Continue to use V in section 1
from VnDF import Calc_Vgust
c_av = ## Put Value HERE
CLa = ## Put Value HERE
VC = ## Put Value HERE
VD = ## Put Value HERE
VB = ## Put Value HERE
n_GD = []; V_GD = [VB,VC,VD]; condition = ['B','C','D']
for Vr,c in zip(V_GD,condition):
    n_GD.append(Calc_Vgust(Vr,W,S,rho,c_av,CLa,c))
n_GD.insert(0,1); V_GD.insert(0,0)
#### Make plots
plt.figure(figsize=(9, 3))
plt.plot(V_GD,n_GD,'k') # for positive Ude
plt.plot(V_GD,2*np.ones(len(n_GD))-n_GD,'k') # for negative Ude
plt.axis([0, 200, -1, 3])
plt.vlines(x = VB, ymin=-1, ymax=3, colors='k', linestyles='--')
plt.vlines(x = VC, ymin=-1, ymax=3, colors='k', linestyles='--')
plt.vlines(x = VD, ymin=-1, ymax=3, colors='k', linestyles='--')
plt.text(VB, -1.25, r'$V_B$', ha='center') # The location of the notation can be adjusted
plt.text(VC, -1.25, r'$V_C$', ha='center') # The location of the notation can be adjusted
plt.text(VD, -1.25, r'$V_D$', ha='center') # The location of the notation can be adjusted
plt.title('Generic V-n gust diagram')
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig('%s/Figure_GD.png'%(savedir))
plt.show()
##########################################################

###################### Composite V-n Diagram ######################  
plt.figure(figsize=(12, 4))
#### From PART B
plt.plot(Vsnn, n_positive, 'k', Vsnn, n_negative, 'k')
plt.plot(xr,yr,'r-')
plt.vlines(x = VA, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.vlines(x = Vsp, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.vlines(x = Vsn, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.title('Generic V-n maneuver diagram')
plt.text(VA, -2.25, r'$V_A$', ha='center') # The location of the notation can be adjusted
plt.text(Vsp, -2.25, r'$V_{s_{1}}$', ha='center') # The location of the notation can be adjusted
plt.text(Vsn, -2.25, r'$V_{s_{-1}}$', ha='center') # The location of the notation can be adjusted
#### From PART C
plt.plot(V_GD,n_GD,'k') # for positive Ude
plt.plot(V_GD,2*np.ones(len(n_GD))-n_GD,'k') # for negative Ude
plt.vlines(x = VB, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.vlines(x = VC, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.vlines(x = VD, ymin=-2, ymax=4, colors='k', linestyles='--')
plt.text(VB, -2.25, r'$V_B$', ha='center') # The location of the notation can be adjusted
plt.text(VC, -2.25, r'$V_C$', ha='center') # The location of the notation can be adjusted
plt.text(VD, -2.25, r'$V_D$', ha='center') # The location of the notation can be adjusted
plt.axis([0, 200, -2, 4])
plt.title('Composite V-n gust diagram')
plt.text(Vmax*0.9, -2.25, r'Equivalent Airspeed $V_e$', ha='center') # The location of the notation can be adjusted
plt.gca().axes.get_xaxis().set_visible(False)
plt.savefig('%s/Figure_CD.png'%(savedir))
plt.show()


###################################################################