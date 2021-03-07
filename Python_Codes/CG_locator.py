# -*- coding: utf-8 -*-

from CG_calc import MassObj
from CG_calc import FindCG
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

# NOTE: Ignoring y and z locations for now...

WingRootLoc = [4.8, 0, 0] # Location of Wing Root LE
HTRootLoc = 9.75
VTRootLoc = 9.75

CML = [2.4, 0, 0]         # Canard motor location
CMCL = [2.4-0.0762, 0, 0] # Canard motor controller location
CRL = [2.8, 0, 0]         # Canard rotor location

IMRL = [1.448, 0, 0] # Inboard motor location relative to WingRootLoc
MMRL = [1.503, 0, 0] # Middle   "                                   "
OMRL = [1.559, 0, 0] # Outboard "                                   "

IMCRL = [1.448-0.0762, 0, 0] # Inboard motor controller location relative to WingRootLoc
MMCRL = [1.503-0.0762, 0, 0] # Middle   "                                              "
OMCRL = [1.559-0.0762, 0, 0] # Outboard "                                              "

IRRL = [1.448+0.4, 0, 0] # Inboard rotor location relative to WingRootLoc
MRRL = [1.503+0.4, 0, 0] # Middle   "                                   "
ORRL = [1.559+0.4, 0, 0] # Outboard "                                   "

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
Fuselage = MassObj(152.3, 5.51, 0, 0)

# Main Wing
MainWing = MassObj(240,*ListAdd(WingRootLoc, WingRelCG))

# Empennage
HorzTailArea = 4.6
VertTailArea = 2.098
HorzTail = MassObj(46, HTRootLoc+RelHorzTailCG_X(HorzTailArea), 0, 0)
VertTail = MassObj(20.98, VTRootLoc+RelVertTailCG_X(VertTailArea), 0, 0)
Empennage = [HorzTail, VertTail]

# Canard
Canard = MassObj(8.45, 3.32675, 0, 0)

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
FrontPax = MassObj(88.45, 4.205, 0, 0)
RearPax1 = MassObj(88.45, 5.1874, 0, 0)
RearPax2 = MassObj(88.45, 5.1874, 0, 0)
PaxAndSeats = [FrontPax, RearPax1, RearPax2]

objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage, Canard, *PaxAndSeats]
CG_pos = FindCG(objs)

# Iterate process to account for changing Empennage CG's
for i in range(10):
    # Iterate on j to get Empennage CG's for this i'th iteration
    for j in range(10):
        x_h = HTRootLoc + HorzTailAvgChord(HorzTailArea)*0.25 - CG_pos[1]
        x_v = VTRootLoc + VertTail_XAC(VertTailArea) - CG_pos[1]
        HorzTailArea = V_h*S*c/x_h
        VertTailArea = V_v*S*b/x_v
    HorzTail = MassObj(10*HorzTailArea, HTRootLoc+RelHorzTailCG_X(HorzTailArea), 0, 0)
    VertTail = MassObj(10*VertTailArea, VTRootLoc+RelVertTailCG_X(VertTailArea), 0, 0)
    Empennage = [HorzTail, VertTail]
    objs = [Fuselage, *MotorList, *MotorConList, *RotorList, MainWing, *Empennage, Canard, *PaxAndSeats]
    CG_pos = FindCG(objs) 