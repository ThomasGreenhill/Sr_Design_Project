# -*- coding: utf-8 -*-

from CG_calc import MassObj
from CG_calc import FindCG
from CG_calc import Findmassmoment
import math

def ListAdd(L1, L2):
    s = [x + y for x, y in zip(L1, L2)]
    return s

def RelHorzTailCG_X(Area):
    AR        = 4.5
    Span      = math.sqrt(AR*Area)/2
    AveChord  = Area/2/Span
    RootChord = 4/3*AveChord
    CGX       = RootChord*0.5-0.5*AveChord+0.3*AveChord
    return CGX

def HorzTailAvgChord(Area):
    AR        = 4.5
    Span      = math.sqrt(AR*Area)/2
    AveChord  = Area/2/Span
    return AveChord

def RelVertTailCG_X(Area):
    AR        = 2.26*2
    Span      = math.sqrt(AR*Area*2)/2
    AveChord  = Area/Span
    RootChord = AveChord*2/(1.6)
    CGX       = RootChord-AveChord+0.3*AveChord
    return CGX

def VertTail_XAC(Area): # This is relative to root LE
    AR        = 2.26*2
    Span      = math.sqrt(AR*Area*2)/2
    AveChord  = Area/Span
    Taper     = 0.6
    RootChord = AveChord*2/(1+Taper)
    TipChord  = RootChord*Taper
    YAC       = Span*2/6*((1+2*Taper)/(1+Taper))
    XAC       = YAC*((RootChord-TipChord)/Span)+0.25*AveChord
    return XAC
    
# ================================================#
#####                Constants                #####
# ================================================#

S = 16
c = 1.26491
b = 12.649
V_h = 0.655
V_v = 0.0425

# ================================================#
##### Main Wing Position and Motor Positions  #####
# ================================================#
# Nose tip relative to origin: x = 2.0
# NOTE: Ignoring y and z locations for now...

WingRootLoc = [5, 0, 2+0.59] # Location of Wing Root LE
HTRootLoc = 9.75
VTRootLoc = 9.75

CML = [2.4, 1.3, 2-0.15]         # Canard motor location
CMCL = [2.4-0.0762, 1.3, 2-0.15] # Canard motor controller location
CRL = [2.8, 1.3, 2-0.15]         # Canard rotor location

IMRL = [1.448, 1.62, 0] # Inboard motor location relative to WingRootLoc
MMRL = [1.503, 3.77, 0] # Middle   "                                   "
OMRL = [1.559, 5.915, 0] # Outboard "                                   "

IMCRL = [1.448-0.0762, 1.62, 0] # Inboard motor controller location relative to WingRootLoc
MMCRL = [1.503-0.0762, 3.77, 0] # Middle   "                                              "
OMCRL = [1.559-0.0762, 5.915, 0] # Outboard "                                              "

IRRL = [1.448+0.4, 1.62, 0] # Inboard rotor location relative to WingRootLoc
MRRL = [1.503+0.4, 3.77, 0] # Middle   "                                   "
ORRL = [1.559+0.4, 5.915, 0] # Outboard "                                   "

# ================================================#
#####     Calculate Main Wing CG Location     #####
# ================================================#

CGDist     = 0.395 # CG distance from LE (From Roskam II Ch. 10)
RootChord  = 1.40546
TipChord   = 1.12437
AveChord   = (RootChord+TipChord)/2
Span       = 6.32456 # For one half wing!
SweepAngle = 2*math.pi/180 # rad
SweepLoc   = 0.8 # proportion of AveChord from LE
MidSweepX  = SweepLoc*RootChord + Span*math.sin(SweepAngle)
WingRelCGX = MidSweepX -0.8*AveChord + CGDist*AveChord
WingRelCGY = 0 # Leaving 0 for now
WingRelCGZ = 0 # Leaving 0 for now
WingRelCG  = [WingRelCGX, WingRelCGY, WingRelCGZ]
Taper      = 0.8
WingRelYAC = b/6*((1+2*Taper)/(1+Taper))
WingRelXAC = WingRelYAC*((0.8*RootChord + Span*math.sin(SweepAngle) - 0.8*TipChord)/Span)+0.25*AveChord

# ================================================#
#####           Create all MassObjs           #####
# ================================================#

# Fuselage
Fuselage = MassObj(152.3*0.7, 5.51, 0, 0.7)

# Main Wing
MainWing = MassObj(240*0.7,*ListAdd(WingRootLoc, WingRelCG))

# Empennage (initial guess, will be refined)
HorzTailArea = 4.6
VertTailArea = 2.098
HorzTail = MassObj(46*0.8, HTRootLoc+RelHorzTailCG_X(HorzTailArea), 0, 2.15)
VertTail = MassObj(20.98*0.8, VTRootLoc+RelVertTailCG_X(VertTailArea), 0, 2.5)
Empennage = [HorzTail, VertTail]

# Canard
Canard = MassObj(8.45*0.7, 3.32675, 0, 2-0.15)

# Motors
CanardMotor   = MassObj(12*2, *CML)
InboardMotor  = MassObj(12*2, *ListAdd(WingRootLoc, IMRL))
MiddleMotor   = MassObj(12*2, *ListAdd(WingRootLoc, MMRL))
OutboardMotor = MassObj(12*2, *ListAdd(WingRootLoc, OMRL))
MotorList = [CanardMotor, InboardMotor, MiddleMotor, OutboardMotor]

# Motor Controllers
CanardMotorCon   = MassObj(8*2, *CMCL)
InboardMotorCon  = MassObj(8*2, *ListAdd(WingRootLoc, IMCRL))
MiddleMotorCon   = MassObj(8*2, *ListAdd(WingRootLoc, MMCRL))
OutboardMotorCon = MassObj(8*2, *ListAdd(WingRootLoc, OMCRL))
MotorConList = [CanardMotorCon, InboardMotorCon, MiddleMotorCon, OutboardMotorCon]

# Rotors
CanardRotor   = MassObj(2, *CRL)
InboardRotor  = MassObj(2, *ListAdd(WingRootLoc, IRRL))
MiddleRotor   = MassObj(2, *ListAdd(WingRootLoc, MRRL))
OutboardRotor = MassObj(2, *ListAdd(WingRootLoc, ORRL))
RotorList = [CanardRotor, InboardRotor, MiddleRotor, OutboardRotor]

# Passengers+Seats
FrontPax  = MassObj(81.65, 4.205, 0, 2-0.03)
FrontSeat = MassObj(6.804, 4.205, 0, 2-0.3)
RearPax1  = MassObj(81.65, 5.1874, 0.3, 2-0.09)
RearPax2  = MassObj(81.65, 5.1874, 0.3, 2-0.09)
RearSeats = MassObj(6.804*2, 5.1874, 0, 2-0.36)
Pax   = [FrontPax, RearPax1, RearPax2]
Seats = [FrontSeat, RearSeats]

# Landing Gear
FrontGear = MassObj(0.057*1300*0.15, 4, 0, 1.5)
RearGears = MassObj(0.057*1300*0.85, 6.5, 0.25, 1.5)
LandingGear = [FrontGear, RearGears]

# Luggage
Luggage = MassObj(25, 2.5, 0, 2)

# Fixed Equipment
FixedEquip = MassObj(1300*0.05, 5, 0, 2.3)

# Fuel Cells
FuelCell = MassObj(385*0.75, 6, 0, 2-0.23)
FuelCells = [FuelCell]

# Fuel Tank and Fuel
FuelTank = MassObj(5*9, 6, 0, 2+0.3)
FuelMass = MassObj(5, FuelTank.x, 0, 2.3)
FuelTotal = [FuelTank, FuelMass]

# Battery
Battery = MassObj(35000/470, 4.5, 0, 2-0.58)

objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
        Canard, *LandingGear, *Pax, *Seats, Luggage, FixedEquip, *FuelCells,\
        *FuelTotal, Battery]
CG_pos = FindCG(objs)

print("Calculating CG, empennage sizing and mass moment of inertia based on GTOW:") ## Changed by Yihui, 03/18/2021
print("--------------------------------------------------")

# Iterate process to account for changing Empennage CG's
for i in range(10):
    # Iterate on j to get Empennage CG's for this i'th iteration
    for j in range(10):
        x_h = HTRootLoc + HorzTailAvgChord(HorzTailArea)*0.25 - CG_pos[1]
        x_v = VTRootLoc + VertTail_XAC(VertTailArea) - CG_pos[1]
        HorzTailArea = V_h*S*c/x_h
        VertTailArea = V_v*S*b/x_v
    HorzTail = MassObj(10*HorzTailArea*0.7, HTRootLoc+RelHorzTailCG_X(HorzTailArea), 0, 2.15)
    VertTail = MassObj(10*VertTailArea*0.7, VTRootLoc+RelVertTailCG_X(VertTailArea), 0, 2.5)
    Empennage = [HorzTail, VertTail]
    objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
            Canard, *LandingGear, *Pax, *Seats, Luggage, FixedEquip, *FuelCells,\
            *FuelTotal, Battery]
    CG_pos = FindCG(objs)
Im = Findmassmoment(objs) ## Changed by Yihui, 03/18/2021
    
print("Total Mass: {:4f} kg".format(CG_pos[0]))
print("Horizontal Tail Area: {:.4f}".format(HorzTailArea))
print("Vertical Tail Area: {:.4f}".format(VertTailArea))
print("xCOM: {:4f} m".format(CG_pos[1]))
print("xCOL approximate: {:.4f} m".format(FindCG(RotorList)[1]))
print("xCOL as proportion of chord past wing root LE: {:.4f}".format((FindCG(RotorList)[1]-WingRootLoc[0])/AveChord))
print("xCOM as proportion of chord past wing root LE: {:.4f}".format((CG_pos[1]-WingRootLoc[0])/AveChord))
print("Mass Moment of Inertia about x: {:.4f} kg-m^2".format(Im[0])) ## Changed by Yihui, 03/18/2021
print("Mass Moment of Inertia about y: {:.4f} kg-m^2".format(Im[1])) ## Changed by Yihui, 03/18/2021
print("Mass Moment of Inertia about z: {:.4f} kg-m^2".format(Im[2])) ## Changed by Yihui, 03/18/2021

print("\nCalculating CG based on empy weight:")
print("------------------------------------")
objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
        Canard, *LandingGear, *Seats, FixedEquip, *FuelCells, FuelTank, Battery]
CG_pos = FindCG(objs)
print("Total Mass: {:4f} kg".format(CG_pos[0]))
print("xCOM: {:4f} m".format(CG_pos[1]))
print("xCOM as proportion of chord past wing root LE: {:.4f}".format((CG_pos[1]-WingRootLoc[0])/AveChord))

print("\nCalculating CG based on operating empty weight:")
print("------------------------------------")
objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
        Canard, *LandingGear, *Seats, FixedEquip, *FuelCells, FuelTank, Battery, FrontPax]
CG_pos = FindCG(objs)
print("Total Mass: {:4f} kg".format(CG_pos[0]))
print("xCOM: {:4f} m".format(CG_pos[1]))
print("xCOM as proportion of chord past wing root LE: {:.4f}".format((CG_pos[1]-WingRootLoc[0])/AveChord))

print("\nCalculating CG based on operating empty weight plus fuel:")
print("------------------------------------")
objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
        Canard, *LandingGear, *Seats, FixedEquip, *FuelCells, *FuelTotal, Battery, FrontPax]
CG_pos = FindCG(objs)
print("Total Mass: {:4f} kg".format(CG_pos[0]))
print("xCOM: {:4f} m".format(CG_pos[1]))
print("xCOM as proportion of chord past wing root LE: {:.4f}".format((CG_pos[1]-WingRootLoc[0])/AveChord))

print("\nCalculating CG based on operating empty weight plus passengers and luggage:")
print("------------------------------------")
objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage,\
        Canard, *LandingGear, *Seats, FixedEquip, *FuelCells, FuelTank, Battery, *Pax, Luggage]
CG_pos = FindCG(objs)
print("Total Mass: {:4f} kg".format(CG_pos[0]))
print("xCOM: {:4f} m".format(CG_pos[1]))
print("xCOM as proportion of chord past wing root LE: {:.4f}".format((CG_pos[1]-WingRootLoc[0])/AveChord))
