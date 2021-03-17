import numpy 
import matplotlib.pyplot as plt
import sys
sys.path.append('../Utilities')
sys.path.append('../AVL_Automation')
from pyAvl_Cf_Cm_FAER import pyAvl_Cf_Cm_FAER
import avlwrapper as avl

try:
    import formatfigures
    formatfigures.formatsubfigures()
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
    # Properties for Cessna 172 Skyhawk http://jsbsim.sourceforge.net/MassProps.html
    Ixx = 0
    Iyy = 0
    Izz = 0
    Ixz = 0

    cbar = 1.265
    S = 16
    bspan = 6.32456
    g = 9.81
    m = 13000/g
    X_cg = 3.43

    return Ixx, Iyy, Izz, Ixz, cbar, S, bspan, g, m, X_cg

Ixx, Iyy, Izz, Ixz, cbar, S, bspan, g, m, X_cg = acft_props()

## Fixed values:
b = 0
Vt = 62
df = 0
da = 0
de = 0
dr = 0

aircraft = avl.FileWrapper(acftpath)

session = avl.Session(geometry=aircraft)

# if 'gs_bin' in session.config.settings:
#     img = session.save_geometry_plot()[0]
#     avl.show_image(img)
# else:
#     session.show_geometry()

a = numpy.arange(-2,30,0.5)
CL = numpy.zeros((len(a),1))
CD = numpy.zeros((len(a),1))

for ii in range(len(a)):

    current_params = avl.Case(name='Run',
                                    alpha=a[ii], beta=b,
                                    roll_rate=0, pitch_rate=0, yaw_rate=0,
                                    velocity=Vt, density=rho, gravity=g, 
                                    mass=m, Ixx=Ixx, Iyy=Iyy, Izz=Izz, Izx=Ixz,
                                    flap=df, aileron=da, elevator=de, rudder=dr
                                    )

        

    session = avl.Session(geometry=aircraft, cases=[current_params])

        
    result = session.run_all_cases()

    CL[ii] = result['Run']['Totals']['CLtot']
    CD[ii] = result['Run']['Totals']['CDtot']
    print("Running alpha = " + str(a[ii]))

print(CL)
print(CD)

plt.figure()
plt.plot(CL,CD)

plt.figure()
plt.plot(a,CL)
plt.show()