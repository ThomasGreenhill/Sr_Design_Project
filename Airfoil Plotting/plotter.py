# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 11:58:35 2021

@author: Michael
"""

# Imports
import pyxfoil
import os
import numpy
import matplotlib.pyplot as plt
import shutil
import sys

sys.path.append("../Utilities/")
import formatfigures

try:
    formatfigures.formatfigures()
    latex = True
except ValueError:
    print("Not using latex formatting")
    latex = False

##############################################################################

# Select airfoil and parameters
foils = ['NLF 0414F']
alfs = numpy.linspace(-3,20,100)
NACA = [False]
Re = 1e7

# Choose to plot Cl or Cd
# Type = 'Cl-a'
# Type = 'Cd-a'
Type = 'Cd-Cl'

# Removes existing files in /Data so it doesn't get confused
if os.path.isdir('./Data'):
    shutil.rmtree('./Data')

# XFoil/PyXfoil Stuff
for foil,N in zip(foils,NACA):
    # Run Xfoil
    if not N:
        GeomFile = './foils/'+foil+'.dat'
        print('Running XFoil for geometry file located at: '+GeomFile)
    else:
        GeomFile = foil
        print('Running XFoil for NACA '+GeomFile)
    o = pyxfoil.GetPolar(GeomFile, N, alfs, Re, SaveCP=False, quiet=True)
    
    # Select proper polar data file
    if not N:
        DataPath = './Data/'+foil+'/'
    else:
        DataPath = './Data/naca'+foil+'/'
    files = os.listdir(DataPath)
    PolarFile = [i for i in files if 'polar' in i]
    d = pyxfoil.ReadXfoilPolar(DataPath+PolarFile[0])
    
    # Plot
    lab = 'NACA ' + foil if N else foil
    if Type == 'Cl-a':
        plt.plot(d.alpha,d.Cl,label=lab)
    elif Type == 'Cd-a':
        plt.plot(d.alpha,d.Cd,label=lab)
    elif Type == 'Cd-Cl':
        plt.plot(d.Cl,d.Cd,label=lab)
        # plt.xlim((0, 0.8))
        # plt.ylim((0, 0.02))
    
# Plot Labelling
if Type == 'Cl-a':
    plt.title('$C_l$ vs $\\alpha$, $Re$ = {:4.2G}'.format(Re))
    plt.ylabel(r'$C_l$')
    plt.xlabel(r'$\alpha$'+' (degrees)')
elif Type == 'Cd-a':
    plt.title('$C_d$ vs $\\alpha$, $Re$ = {:4.2G}'.format(Re))
    plt.ylabel(r'$C_d$')
    plt.xlabel(r'$\alpha$'+' (degrees)')
elif Type == 'Cd-Cl':
    plt.title('$C_d$ vs $C_l$, $Re$ = {:4.2G}'.format(Re))
    plt.ylabel(r'$C_d$')
    plt.xlabel(r'$C_l$')

    
plt.legend()
plt.show()