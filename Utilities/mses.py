"""AIRFOIL GEOMETRY MANIPULATION - MSES FORMATTING
Logan Halstrom
EAE 127
CREATED: 12 NOV 2015
MODIFIY: 4 OCT 2019


DESCRIPTION: Provides functions for manimulating MSES closed-curve data files.
Split an MSES file into separate upper and lower surfaces.
    Determine splitting location based on reversal of x-coordinate.
Merge separate surface data into single MSES data set.
Interpolate data to match new x vector

TO DO:
    Rework main to match new functions

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ReadXfoilGeometry(ifile):
    """Reads MSES two column xfoil output files, including geometry
    and cp distributions.
    ifile --> path to input file (string)
    """
    xgeom, ygeom = np.loadtxt(ifile, skiprows=1, unpack=True)
    return xgeom, ygeom

def FindLE_top(X):
    """Return index dividing upper and lower surface given MSES geometry.
    Search along upper surface until LE.
    MSES files start at rear of airfoil, and x diminishes until the leading
    edge, where it then increases back to the trailing edge.  This code finds
    the transition where x goes from decreasing to increasing.
    X --> MSES x coordinates
    """
    xold = X[0]
    for i, x in enumerate(X[1:]):
        if x >= xold:
            #If current x greater/equal to prev x, x is increasing (lower surf)
            return i #return index of Leading Edge (divides upper/lower surfs)
        else:
            #If current x less than prev x, x still diminishing (upper surf)
            xold = x

def FindLE_bot(X):
    """Return index dividing upper and lower surface given MSES geometry.
    Search along lower surface until LE.
    MSES files start at rear of airfoil, and x diminishes until the leading
    edge, where it then increases back to the trailing edge.  This code finds
    the transition where x goes from decreasing to increasing.
    X --> MSES x coordinates
    """
    Xreverse = X[::-1]
    xold = Xreverse[0]
    for i, x in enumerate(Xreverse[1:]):
        if x >= xold:
            #If current x greater/equal to prev x, x is increasing (on upper surf)
            return len(X) - 1 - i #return index of Leading Edge (divides upper/lower surfs)
        else:
            #If current x less than prev x, x still diminishing (still on lower surf)
            xold = x

def FindLE(X):
    """ Compatibility function for older versions of mses.py. Runs FindLE_top
    X --> MSES x coordinates
    """
    return FindLE_top(X)

def MsesSplit(x, y):
    """Split MSES format into upper and lower surfaces.
    Find LE from MSES x geometry coordinates,
    Split y at this index(s).
    If LE point is at y=0, include in both sets of data.
    Return y split into upper/lower surfaces, with LE overlapping
    x --> MSES x coordinates
    y --> Any other MSES parameter (e.g. x/c, z/c, Cp, etc)
    """
    #FIND LE FROM BOTH SIDES (DETECT SHARED LE POINT)
    #Get index of leading edge starting from upper surface TE
    iLE_top = FindLE_top(x)
    #Get index of leading edge starting from lower surface TE
    iLE_bot = FindLE_bot(x)
    #Split upper and lower surface, reverse order upper surface
    up = y[iLE_top::-1]
    lo = y[iLE_bot:]
    return up, lo

def MsesInterp(xout, xmses, ymses):
    """Split MSES format data into upper and lower surfaces.  Then
    interpolate data to match given xout vector.
    xout  --> desired x locations
    xmses --> original x MSES data
    ymses --> original x/c, z/c, Cp, etc MSES data
    """
    xup_mses, xlo_mses = MsesSplit(xmses, xmses)
    yup_mses, ylo_mses = MsesSplit(xmses, ymses)
    yup = np.interp(xout, xup_mses, yup_mses)
    ylo = np.interp(xout, xlo_mses, ylo_mses)
    return yup, ylo

def MsesMerge(xlo, xup, ylo, yup):
    """ Merge separate upper and lower surface data into single MSES set.
    If LE point is shared by both sides, drop LE from lower set to avoid overlap
    xlo, xup --> lower/upper surface x coordinates to merge
    ylo, yup --> lower/upper surface y OR surface Cp values to merge
    """
    #drop LE point of lower surface if coincident with upper surface
    if xlo[0] == xup[0] and ylo[0] == yup[0]:
    # if xlo[0] == xup[0] and ylo[0] == 0 and yup[0] == 0:
        xlo = xlo[1:]
        ylo = ylo[1:]
    n1 = len(xup)     #number of upper surface points
    n = n1 + len(xlo) #number of upper AND lower surface points
    x, y = np.zeros(n), np.zeros(n)
    #reverse direction of upper surface coordinates
    x[:n1], y[:n1] = xup[-1::-1], yup[-1::-1]
    #append lower surface coordinates as they are
    x[n1:], y[n1:] = xlo, ylo
    return x, y



def main(name, x, z):
    """Test code for MSES functions.  Load MSES geometry file, split, and
    re-merge.
    geom --> path to airfoil geometry file
    """

    import sys
    import matplotlib.gridspec as gridspec
    # import plotUtil as lplot
    params = {
        'axes.grid'      : True,  #grid on plot
    }
    import matplotlib
    matplotlib.rcParams.update(params) #update matplotlib defaults

    def PlotSplitFoil(ax, x, z, xup, zup, xlo, zlo):
        ax.plot(x, z,     label='OG MSES', linestyle=' ', marker='.', color='black', zorder=10)
        ax.plot(xup, zup, label='Upper',   linestyle=' ', marker='s', markersize=8)
        ax.plot(xlo, zlo, label='Lower',   linestyle=' ', marker='o', markersize=6)
        ax.plot([xup[0], xup[-1]], [zup[0], zup[-1]], label='chord line', color='black')


    def PlotSplitCp(ax, x, z, xup, zup, xlo, zlo):
        ax.plot(x, z,     label='OG MSES', linestyle=' ', marker='.', color='black', zorder=10)
        ax.plot(xup, zup, label='Upper',   linestyle=' ', marker='s', markersize=8)
        ax.plot(xlo, zlo, label='Lower',   linestyle=' ', marker='o', markersize=6)
        # ax.plot([xup[0], xup[-1]], [zup[0], zup[-1]], label='chord line', color='black')


    def PlotMsesSplitGeometry(x, z, xup, zup, xlo, zlo, name=''):
        #dashed lines should perfectly overlap black, no point overlap
        # fig1 = plt.figure(figsize=(12,4))

        #Make overall figure (2x2 subplot)
        fig, ax = plt.subplots(2, 2, figsize=(12,8))

        #make axis object for top subplot (spans 2 columns)
        ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)

        ax1.set_title('Split Geometry Should Overlap Original Mses\n{}'.format(name) )

        PlotSplitFoil(ax1, x, z, xup, zup, xlo, zlo)
        ax1.legend(loc='best')
        ax1.axis('equal')
        ax1.set_xlim([-0.05, 1.05])

        #LEADING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax2 = plt.subplot2grid((2,2), (1,0))

        ax2.set_title('Leading Edge: Upper/Lower Should Overlap At LE (Coincident)')

        PlotSplitFoil(ax2, x, z, xup, zup, xlo, zlo)
        ax2.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax2.set_xlim([-0.005, 0.01])
        ax2.set_ylim([-0.0125, 0.0125])


        #TRAILING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax3 = plt.subplot2grid((2,2), (1,1))

        ax3.set_title('Trailing Edge: Upper/Lower can be coincident or not')

        PlotSplitFoil(ax3, x, z, xup, zup, xlo, zlo)
        ax3.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax3.set_xlim([0.905, 1.01])
        ax3.set_ylim([-0.0125, 0.0125])


        plt.tight_layout()

    def PlotMsesSplitCp(x, Cp, xup, Cpup, xlo, Cplo, name=''):
        #Make overall figure (2x2 subplot)
        fig, ax = plt.subplots(2, 2, figsize=(12,8))

        #make axis object for top subplot (spans 2 columns)
        ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)

        ax1.set_title('Surface $C_P$: Original MSES vs Split Upper/Lower\n{}'.format(name) )



        PlotSplitCp(ax1, x, Cp, xup, Cpup, xlo, Cplo)
        ax1.legend(loc='best')
        ax1.set_xlim([-0.05, 1.05])
        ax1.invert_yaxis() #invert y-axis

        #LEADING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax2 = plt.subplot2grid((2,2), (1,0))

        ax2.set_title('Leading Edge')

        PlotSplitCp(ax2, x, Cp, xup, Cpup, xlo, Cplo)
        ax2.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax2.set_xlim([-0.005, 0.01])
        # ax2.set_ylim([-0.0125, 0.0125])
        ax2.invert_yaxis() #invert y-axis


        #TRAILING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax3 = plt.subplot2grid((2,2), (1,1))

        ax3.set_title('Trailing Edge')

        PlotSplitCp(ax3, x, Cp, xup, Cpup, xlo, Cplo)
        ax3.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax3.set_xlim([0.905, 1.01])
        # ax3.set_ylim([-0.0125, 0.0125])
        ax3.invert_yaxis() #invert y-axis

        plt.tight_layout()



    def PlotMsesMergeGeometry(x, z, xmerge, zmerge, name=''):
        #dashed lines should perfectly overlap black, no point overlap
        # fig1 = plt.figure(figsize=(12,4))

        #Make overall figure (2x2 subplot)
        fig, ax = plt.subplots(2, 2, figsize=(12,8))

        #make axis object for top subplot (spans 2 columns)
        ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)

        ax1.set_title('Merge Geometry Should Be Identical to Original Mses\n{}'.format(name) )

        ax1.plot(x, z, label='OG MSES', linestyle=' ', marker='.', color='black', zorder=10)
        ax1.plot(xmerge, zmerge, label='Merge', linestyle=' ', marker='o', )


        ax1.legend(loc='best')
        ax1.axis('equal')
        ax1.set_xlim([-0.05, 1.05])

        #LEADING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax2 = plt.subplot2grid((2,2), (1,0))

        ax2.set_title('Leading Edge')

        ax2.plot(x, z, label='OG MSES', linestyle=' ', marker='.', color='black', zorder=10)
        ax2.plot(xmerge, zmerge, label='Merge', linestyle=' ', marker='o', )
        ax2.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax2.set_xlim([-0.005, 0.01])
        ax2.set_ylim([-0.0125, 0.0125])


        #TRAILING EDGE PLOT
            #axis object for subplot in lower left grid cell
        ax3 = plt.subplot2grid((2,2), (1,1))

        ax3.set_title('Trailing Edge')

        ax3.plot(x, z, label='OG MSES', linestyle=' ', marker='.', color='black', zorder=10)
        ax3.plot(xmerge, zmerge, label='Merge', linestyle=' ', marker='o', )
        ax3.axhline(y=0, color='gray', linestyle='--')
        # ax2.legend(loc='best')
        ax3.set_xlim([0.905, 1.01])
        ax3.set_ylim([-0.0125, 0.0125])


        plt.tight_layout()

















    #FUNCTIONALITY TEST:
        #1. SPLIT GEOM SO LEADING EDGE IS ALWAYS SHARED
        #TEST WITH S1223, NACA NON SYM, NACA SYM?, PANEL DISC
        #INTERP GETS START/END FROM LE/TE, ONLY TAKES # OF POINTS, RETURNS XNEW
        #SPLIT INTERP SURFACE AND PRESSURE
        # MERGE GEOM SO THAT OVERLAPPING LEADING EDGE IS UNDUPLICATED






    lenmses = len(x)
    # print('Raw MSES x:', x)
    # print('Raw MSES z:', z)


    ####################################################################
    ### TEST SPLIT THEN MERGE GEOMETRY

    print('\nSPLIT MSES GEOMETRY')
    xup, xlo = MsesSplit(x, x)
    zup, zlo  = MsesSplit(x, z)

    # print(xup, xlo)
    # print(zup, zlo)

    # #check that split surface coordiantes are appropriate size
    # if len(xlo) != len(zlo):
    #     sys.exit('ERROR: SPLIT LOWER SURFACE COORDINATES DIFFERENT SIZES')
    # if len(xup) != len(zup):
    #     sys.exit('ERROR: SPLIT UPPER SURFACE COORDINATES DIFFERENT SIZES')

    # if len(xup) + len(xlo) != lenmses:
    #     sys.exit('ERROR: NUMBER OF POINTS IN UPPER/LOWER SURFACES NOT PRESERVED')
    # else:
    #     print('{} + {} = {}'.format(len(xup), len(xlo), lenmses ))



    #PLOT ORIGINAL MSES AND SPLIT GEOMETRY
    PlotMsesSplitGeometry(x, z, xup, zup, xlo, zlo, name)
    plt.show()


    xmerge, zmerge = MsesMerge(xlo, xup, zlo, zup)
    #check for duplicate LE
        #loop through all points except TE
        #if current point is in any of previous, its an unwanted duplicate
    prevxy = []
    for xx, yy in zip(xmerge[1:-1], zmerge[1:-1]):
        if (xx, yy) in prevxy:
            sys.exit('ERROR: OVERLAPPING LE POINTS IN MERGED GEOMETRY')
        else:
            prevxy.append( (xx, yy) )

    PlotMsesMergeGeometry(x, z, xmerge, zmerge, name)
    plt.show()
















    ####################################################################
    ### TEST SPLIT AND INTERPOLATE GEOMETRY


    print('\nSPLIT AND INTERPOLATE MSES GEOMETRY')
    xnew = np.linspace(0, 1, 1001)
    xup, xlo = MsesInterp(xnew, x, x)
    zup, zlo = MsesInterp(xnew, x, z)

    #PLOT ORIGINAL MSES AND SPLIT GEOMETRY

    #dashed lines should perfectly overlap black, no point overlap
    # fig1 = plt.figure(figsize=(12,4))

    #Make overall figure (2x2 subplot)
    fig, ax = plt.subplots(2, 2, figsize=(12,8))

    #make axis object for top subplot (spans 2 columns)
    ax1 = plt.subplot2grid((2,2), (0,0), colspan=2)

    ax1.set_title('Compare Original MSES with Split Iterpolated Upper/Lower')

    PlotSplitFoil(ax1, x, z, xup, zup, xlo, zlo)
    ax1.legend(loc='best')
    ax1.axis('equal')
    ax1.set_xlim([-0.05, 1.05])

    #LEADING EDGE PLOT
        #axis object for subplot in lower left grid cell
    ax2 = plt.subplot2grid((2,2), (1,0))

    ax2.set_title('Leading Edge')

    PlotSplitFoil(ax2, x, z, xup, zup, xlo, zlo)
    ax2.axhline(y=0, color='gray', linestyle='--')
    # ax2.legend(loc='best')
    ax2.set_xlim([-0.005, 0.01])
    ax2.set_ylim([-0.0125, 0.0125])


    #TRAILING EDGE PLOT
        #axis object for subplot in lower left grid cell
    ax3 = plt.subplot2grid((2,2), (1,1))

    ax3.set_title('Trailing Edge')

    PlotSplitFoil(ax3, x, z, xup, zup, xlo, zlo)
    ax3.axhline(y=0, color='gray', linestyle='--')
    # ax2.legend(loc='best')
    ax3.set_xlim([0.905, 1.01])
    ax3.set_ylim([-0.0125, 0.0125])


    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    foil = 'data/naca2412_geom.dat'
    name = 'naca2412'

    geom = 'Data/{}.dat'.format(name)
    x, z = ReadXfoilGeometry(geom)
    main(name, x, z)

    ####################################################################
    name = 's1223'
    geom = 'Data/{}.dat'.format(name)
    x, z = ReadXfoilGeometry(geom)
    main(name, x, z)


    ####################################################################
    import panelutil as pu

    name = 'naca0012 pointy LE'
    Npanel = 1001

    #LOAD AIRFOIL GEOMETRY
    xgeom, ygeom = ReadXfoilGeometry('Data/naca0012.dat'.format(name))
    #Discretize airfoil geometry
    xends, yends = pu.MakePanelEnds(xgeom, ygeom, Npanel, 'constantfoil')
    #make panels
    panels = pu.MakePanels(xends, yends)
    #Get control point locations of panels (MSES geometry)
    xc = [p.xc for p in panels]
    zc = [p.yc for p in panels]

    main(name, xc, zc)




    ####################################################################

    name = 'naca0020 flat LE'
    Npanel = 1000

    #LOAD AIRFOIL GEOMETRY
    xgeom, ygeom = ReadXfoilGeometry('Data/naca0012.dat'.format(name))
    #Discretize airfoil geometry
    xends, yends = pu.MakePanelEnds(xgeom, ygeom, Npanel, 'constantfoil')
    #make panels
    panels = pu.MakePanels(xends, yends)
    #Get control point locations of panels (MSES geometry)
    xc = [p.xc for p in panels]
    zc = [p.yc for p in panels]

    main(name, xc, zc)




