"""PYXFOIL DEMO: XFOIL AUTOMATION USING PYTHON
Logan Halstrom
EAE 127
UCD
CREATED:  06 OCT 2017
MODIFIED: 30 OCT 2018

DESCRIPTION: Use pyxfoil module to simulate airfoil performance with XFOIL
and process results

REQUIREMENTS: XFOIL must be downloaded from http://web.mit.edu/drela/Public/web/xfoil/
For Windows:
    1. Download XFOIL6.99.zip
    2. Decompress and move xfoil.exe to same folder as Python script
For Mac:
    1. Download Xfoil for Mac-OSX
    2. Open dmg, follow installation instructions

USAGE:
Windows: Save 'pyxfoil.py' and 'xfoil.exe' in same folder as script calling pyxfoil
Mac:     Save 'pyxfoil.py' in same folder as script calling pyxfoil
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Import pyxfoil from same folder as a module
import pyxfoil

# #Import pyxfoil from a different folder as a module
# import sys
# sys.path.append('../../../utils')
# import pyxfoil

########################################################################
#RUN XFOIL FOR NACA AIRFOIL (GEMOETRY FROM EQUATION, NOT FILE)

#Calculate surface pressure distributions of NACA 0012 at Re=0, AoA=0
#Save all force/moment coefficients to single polar file
#Also save airfoil geometry to file

#Inputs
foil = '0012' #NACA airfoil number
naca = True   #allows NACA number input rather than geometry text file
Re   = 0      #Reynolds Number (inviscid)
alfs = [0, 10]#Angles of Attack to simulated

#Run Xfoil,
    #save geometry, surface pressures, and polar (Cl vs alpha)
    #change quiet to 'False' to see raw Xfoil output
print("Running XFOIL/pyxfoil and saving data in 'Data/naca0012' folder...\n")
pyxfoil.GetPolar(foil, naca, alfs, Re, SaveCP=True, quiet=True)
# print('Xfoil run complete')
# input("Press any key to continue...")

########################################################################
#READ XFOIL SOLUTION FROM SAVED TEXT FILES

#read airfoil geometry data from file
    #(this file was created by the above 'pyxfoil.GetPolar' call)
geom = pyxfoil.ReadXfoilAirfoilGeom('Data/naca0012/naca0012.dat')
#Plot airfoil geometry
    #(NOTE: You must plot airfoil geometry from EQUATION, not file, for points in PJ1)
print('\nPlotting airfoil geometry from file saved by XFOIL/pyxfoil')
plt.figure()
plt.title('airfoil geom')
plt.plot(geom['x'], geom['z'])
plt.axis('equal')
plt.xlabel('x/c')
plt.ylabel('z/c')
plt.show()

#Read and print polar data
polar = pyxfoil.ReadXfoilPolar('Data/naca0012/naca0012_polar_Re0.00e+00a0.0-10.0.dat')
print('\nPolar from file saved by XFOIL/pyxfoil:')
print(polar)

print("\n\nNOTE: FOR READING SURFACE PRESSURE DISTRIBUTIONS, SEE 'msesdemo.py'")
print('------------------------------------------------------------------\n\n')

########################################################################
#RUN XFOIL USING GEOMETRY SAVED IN FILE

#You can also load an airfoil geometry from a text file
#Use this for airfoils that are not defined by an equation
#In this example, the NACA 0012 geometry saved to file in the previous part
#will be loaded from file, rather than specified by NACA number

#Inputs
foil = 'Data/naca0012/naca0012.dat' #path to airfoil geometry file
naca = False      #'False' option loads geometry from file path, not equation
Re   = 5e8        #Reynolds Number (viscous effects calculated)
alfs = [0, 5, 10] #Angles of Attack to simulate

#Run Xfoil with same command as before
print('Running XFOIL/pyxfoil a second time, loading geometry from file...\n')
pyxfoil.GetPolar(foil, naca, alfs, Re, SaveCP=True, quiet=True)

print("There are now two different polar files in the save directory:")
import glob
[print('    {}: {}'.format(i+1, g)) for i, g in enumerate(glob.glob("Data/naca0012/*polar*.dat"))]
print('The first is the inviscid polar from our first XFOIL run')
print('The second is the viscous polar from our latest XFOIL run')

'''
viscpolar = pyxfoil.ReadXfoilPolar('Data/naca0012/naca0012_polar_Re5.00e+08a0.0-10.0.dat')
print('\nViscous polar from file saved by XFOIL/pyxfoil the second time:')
print(viscpolar)

print('\n(Notice there are three entries in the table this time, rather than two')


print('\nPlotting airfoil lift curves from polar data from files saved by XFOIL/pyxfoil')
plt.figure()
plt.title('lift curves')
#plot inviscid data loaded in previous section
plt.plot(polar['alpha'], polar['Cl'], marker='o', label='inviscid')
#plot viscous data loaded in current section
plt.plot(viscpolar['alpha'], viscpolar['Cl'], marker='x', label='viscous')
plt.legend()
plt.xlabel('$\\alpha$')
plt.ylabel('$C_l$')
plt.show()
'''