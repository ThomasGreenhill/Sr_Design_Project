import numpy 
import matplotlib.pyplot as plt
import sys
sys.path.append('../Utilities')
sys.path.append('../AVL_Automation')
from pyAvl_Cf_Cm_FAER import pyAvl_Cf_Cm_FAER
import avlwrapper as avl
from matplotlib.offsetbox import AnchoredText

try:
    import formatfigures
    formatfigures.formatfigures()
    latex = True
except:
    print("Not using latex formatting")
    latex = False

acftpath = '../AVL/JIFFY_JERBOA.avl'

global r2d
r2d = 180/numpy.pi

global rho, T, heng
rho = 1.225
# Neglect engine thrust and angular momentum for now 
T = 0 
heng = 0

global Ixx, Iyy, Izz, Ixz, cbar, S, bspan, g, m, X_cg

def acft_props():
    Ixx = 2353
    Iyy = 2327
    Izz = 3974
    Ixz = 0 # Assumed

    cbar = 1.265
    S = 16
    bspan = 12.65
    g = 9.81
    m = 13000/g
    X_cg = 3.43

    return Ixx, Iyy, Izz, Ixz, cbar, S, bspan, g, m, X_cg

Ixx, Iyy, Izz, Ixz, cbar, S, bspan, g, m, X_cg = acft_props()

## Fixed values:
b = 0
df = 4
da = 0
de = 0
dr = 0
Wlb = 2922 #lbf
W = 13000 #N

# Plotting Function
def plotVM(x, stripshear, stripmoment, shearfit, p):
    fitstr = "$V_z = {:.4}y^4 + {:.4}y^3 + {:.4}y^2 + {:.4}y + {:.4}$".format(*p)
    print(fitstr)
    plt.figure(figsize=(12, 10))
    ax = plt.subplot(2,1,1)
    plt.plot(x, stripshear*qbar*S, 'k', label="Result from AVL")
    plt.plot(x, shearfit, '--r', label="4th Order Fit")
    plt.fill_between(x, stripshear*qbar*S, color=(0/255, 255/255, 9/255), alpha=0.7)
    anchored_text = AnchoredText(fitstr, loc=2)
    ax.add_artist(anchored_text)
    plt.xlabel("Strip Location Along Half-Span (m)")
    plt.ylabel("Shear $V_z$ (N)")
    # plt.legend()
    plt.title("Shear Diagram for Wing")
    plt.subplot(2,1,2)
    plt.fill_between(x, stripmoment*qbar*bspan*S, color=(255/255, 4/255, 30/255),alpha=0.8)
    plt.plot(x, stripmoment*qbar*bspan*S, 'k')
    plt.xlabel("Strip Location Along Half-Span (m)")
    plt.ylabel("Moment $M_x$ (N.m)")
    plt.title("Moment Diagram for Wing")
    plt.suptitle("Load Case: "+loadcasestr)
    plt.tight_layout(rect=(0, 0, 1, 0.95))

## Air at Sea level
rho = 1.225

aircraft = avl.FileWrapper(acftpath)
session = avl.Session(geometry=aircraft)

## Uncomment to plot the geometry
# img = session.save_geometry_plot()[0]
# avl.show_image(img)

#### LOAD CASE:
## Max Positive load factor at VNE
VNE = 0.9*174.1*0.514444 #m/s

# FAR PArt 23.337 (a)(1)
nmax = 2.1+(24000/(Wlb+10000))
if nmax >= 3.8:
    nmax = 3.8

CLmaxload = W*nmax/(0.5*rho*VNE**2*S)

# Calculate the equivalent pitch rate
r = 2*m/(rho*S*CLmaxload)
q = VNE/(r)
qcby2V = q*cbar/(2*VNE)

print("The lift coefficient for the maximum positive load is {CL:.4f}, at {g:.4f} gs".format(CL=CLmaxload, g=nmax))
print("The pitch rate for the maximum positive load is {PR:.4f}, at {g:.4f} gs".format(PR=qcby2V, g=nmax))

CL_param = avl.Parameter(name='alpha', setting='CL', value=CLmaxload) 
PM_param = avl.Parameter(name='pitch_rate', setting='qc/2V', value=qcby2V) 

current_params = avl.Case(name='Run', 
                                alpha=CL_param, beta=b,
                                roll_rate=0, pitch_rate=PM_param, yaw_rate=0,
                                velocity=VNE, density=rho, gravity=g, 
                                mass=m, Ixx=Ixx, Iyy=Iyy, Izz=Izz, Izx=Ixz,
                                flap=df, aileron=da, elevator=de, rudder=dr
                                )


# Run AVL
session = avl.Session(geometry=aircraft, cases=[current_params])
result = session.run_all_cases()

# Shear and Moment Diagrams
qbar = 0.5*rho*VNE**2
stripshear = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['Vz/(q*Sref)'])
stripmoment = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['Mx/(q*Bref*Sref)'])
x = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['2Y/Bref'])*bspan/2
loadcasestr = "Max Positive Load Factor (3.8 g) at VNE"
p = numpy.polyfit(x, stripshear*qbar*S, 4)
print(p)
shearfit = numpy.polyval(p, x)
plotVM(x, stripshear, stripmoment, shearfit, p)
plt.savefig("./Figures/maxload_VNE.jpg")


#### LOAD CASE:
## Max Negative load factor at VNE
# FAR PArt 23.337 (b)(1)
nmin = -0.4*nmax
CLminload = W*nmin/(0.5*rho*VNE**2*S)

# Calculate the equivalent pitch rate
r = 2*m/(rho*S*CLminload)
q = VNE/(r)
qcby2V = q*cbar/(2*VNE)

print("The lift coefficient for the maximum negative load is {CL:.4f}, at {g:.4f} gs".format(CL=CLminload, g=nmin))
print("The pitch rate for the maximum negative load is {PR:.4f}, at {g:.4f} gs".format(PR=qcby2V, g=nmin))

CL_param = avl.Parameter(name='alpha', setting='CL', value=CLminload) 
PM_param = avl.Parameter(name='pitch_rate', setting='qc/2V', value=qcby2V) 

current_params = avl.Case(name='Run', 
                                alpha=CL_param, beta=b,
                                roll_rate=0, pitch_rate=PM_param, yaw_rate=0,
                                velocity=VNE, density=rho, gravity=g, 
                                mass=m, Ixx=Ixx, Iyy=Iyy, Izz=Izz, Izx=Ixz,
                                flap=df, aileron=da, elevator=de, rudder=dr
                                )


# Run AVL
session = avl.Session(geometry=aircraft, cases=[current_params])
result = session.run_all_cases()

# Shear and Moment Diagrams
qbar = 0.5*rho*VNE**2
stripshear = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['Vz/(q*Sref)'])
stripmoment = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['Mx/(q*Bref*Sref)'])
x = numpy.array(result['Run']['StripShearMoments']['Main_Wing']['2Y/Bref'])*bspan/2
loadcasestr = "Max Negative Load Factor (-1.52 g) at VNE"
p = numpy.polyfit(x, stripshear*qbar*S, 4)
print(p)
shearfit = numpy.polyval(p, x)
plotVM(x, stripshear, stripmoment, shearfit, p)
plt.savefig("./Figures/minload_VNE.jpg")
plt.show()

