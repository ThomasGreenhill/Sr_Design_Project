# -*- coding: utf-8 -*-

class MassObj:
    
    # MassObj is defined with the mass and xyz coordinates of the object
    
    def __init__(self, mass, x, y, z):
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        
def FindCG(objs):
    
    # Inputs:  A list of MassObj items
    # Outputs: A list of the x, y, and z COM locations
    
    total_mass = sum([obj.mass for obj in objs])
    xCOM = sum([obj.x*obj.mass for obj in objs])/total_mass
    yCOM = sum([obj.y*obj.mass for obj in objs])/total_mass
    zCOM = sum([obj.z*obj.mass for obj in objs])/total_mass
    
    return [total_mass, xCOM, yCOM, zCOM]

def Findmassmoment(objs): ## Changed by Yihui, 03/18/2021

    _, xCOM, yCOM, zCOM = FindCG(objs)
    Ixx = sum(map(lambda obj: obj.mass * ((obj.y - yCOM)**2 + (obj.z - zCOM)**2), objs))
    Iyy = sum(map(lambda obj: obj.mass * ((obj.x - xCOM)**2 + (obj.z - zCOM)**2), objs))
    Izz = sum(map(lambda obj: obj.mass * ((obj.x - xCOM)**2 + (obj.y - yCOM)**2), objs))
    return Ixx, Iyy, Izz

if __name__ == "__main__":
    
    # Sample for our aircraft:
        
    # Motors
    CanardMotor   = MassObj(12*2,-2.1,0,0)
    InboardMotor  = MassObj(12*2,1.38,0,0)
    MiddleMotor   = MassObj(12*2,1.7,0,0)
    OutboardMotor = MassObj(12*2,2,0,0)
    MotorList = [CanardMotor, InboardMotor, MiddleMotor, OutboardMotor]
    
    # Motor Controllers
    CanardMotorCon   = MassObj(8*2,-2.1-0.0762,0,0)
    InboardMotorCon  = MassObj(8*2,1.38-0.0762,0,0)
    MiddleMotorCon   = MassObj(8*2,1.7-0.0762,0,0)
    OutboardMotorCon = MassObj(8*2,2-0.0762,0,0)
    MotorConList = [CanardMotorCon, InboardMotorCon, MiddleMotorCon, OutboardMotorCon]
    
    # Rotors
    CanardRotor   = MassObj(2,-2.1+0.4,0,0)
    InboardRotor  = MassObj(2,1.38+1,0,0)
    MiddleRotor   = MassObj(2,1.7+1,0,0)
    OutboardRotor = MassObj(2,2+1,0,0)
    RotorList = [CanardRotor, InboardRotor, MiddleRotor, OutboardRotor]
    
    # Main Wing
    MainWing = MassObj(240,0.761,0,0)
    
    # Empennage
    HorzTail = MassObj(46,5.44,0,0)
    VertTail = MassObj(20.98,5.385,0,0)
    Empennage = [HorzTail, VertTail]
    
    # Canard
    Canard = MassObj(8.45,-2.17,0,0)
    
    # Passengers+Seats
    FrontPax = MassObj(88.45,-0.937,0,0)
    RearPax1 = MassObj(88.45,0.251,0,0)
    RearPax2 = MassObj(88.45,0.251,0,0)
    PaxAndSeats = [FrontPax, RearPax1, RearPax2]
    
    objs = [*MotorList, *MotorConList, *RotorList, MainWing, *Empennage, \
            Canard, *PaxAndSeats]
    CG_pos = FindCG(objs)
    
    print("Mass: {}".format(CG_pos[0]))
    print("xCOM: {}".format(CG_pos[1]))
