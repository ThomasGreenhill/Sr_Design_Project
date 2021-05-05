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

try:
    import formatfigures
    formatfigures.formatfigures()
    latex = True
except:
    print("Not using latex formatting")
    latex = False

# Default transition location, don't change here

# To set transition location, set Xtr = [upper loc, lower loc]
# You don't need to set Xtr at all, unless you want to

# SELECT AIRFOIL AND PARAMETERS

# foils = ['23012', 'P51D Ref', 'NLF 0115 Ref', 'NLF 0414F Ref', 'HS NLF 213 Ref']
# alfs = numpy.linspace(-3,25,200)
# NACA = [True, False, False, False, False]
# Re = 5.8e6

foils = ['NLF 0414F (+4)', 'NLF 0414F (+0)', 'NLF 0414F (-4)']
alfs = numpy.linspace(-3,8,200)
NACA = [False, False, False, False, False]
Re = 5.8e6

# foils = ['NLF 0414F Ref']
# alfs = numpy.linspace(-3,18,100)
# NACA = [False]
# Re = 5.8e6
Xtr = [0.05, 0.05] # Can specify Xtr if desired


# Choose to plot Cl or Cd
# Type = 'Cl-a'
# Type = 'Cd-a'
Type = 'Cd-Cl'

# Removes existing files in /Data so it doesn't get confused
if os.path.isdir('./Data'):
    shutil.rmtree('./Data')

plt.figure(figsize=(14,11))

# XFoil/PyXfoil Stuff
print(foils)
for ii in range(1,3):
    if ii == 1:
        icing = True
        Xtr = [0.05, 0.05]
        style = '-'
    else:
        icing = False
        Xtr = 0
        style = '--'

    for foil,N in zip(foils,NACA):
        # Run Xfoil
        if not N:
            GeomFile = './foils_ref/'+foil+'.dat'
            print('Running XFoil for geometry file located at: '+GeomFile)
        else:
            GeomFile = foil
            print('Running XFoil for NACA '+GeomFile)
        o = pyxfoil.GetPolar(foil=GeomFile, naca=N, alfs=alfs, Re=Re, Xtr=Xtr, 
                            SaveCP=False, quiet=True)
        
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
        lab = lab + ', Forced $x_{tr}$=0.05 ' if icing else lab + ', No Forced Transition'
        # lab = lab[0:-4] if lab[-3:]=='Ref' else lab
        if Type == 'Cl-a':
            plt.plot(d.alpha,d.Cl,style,label=lab)
        elif Type == 'Cd-a':
            plt.plot(d.alpha,d.Cd,style,label=lab)
        elif Type == 'Cd-Cl':
            plt.plot(d.Cl,d.Cd,style,label=lab)
    
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
    plt.title('$C_d$ vs $C_l$, $Re$ = {:4.2G} With and Without Forced Transition'.format(Re) )
    plt.ylabel(r'$C_d$')
    plt.xlabel(r'$C_l$')
    plt.xlim((-0.1, 0.8))
    plt.ylim((0.002, 0.0105))

    
plt.legend(loc=(0.2, 0.5))
plt.savefig('./airfoils_icing.png', bbox_inches='tight')
plt.show()