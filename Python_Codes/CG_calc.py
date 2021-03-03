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
    # Outputs: A tuple of the x, y, and z COM locations
    
    total_mass = sum([obj.mass for obj in objs])
    xCOM = sum([obj.x*obj.mass for obj in objs])/total_mass
    yCOM = sum([obj.y*obj.mass for obj in objs])/total_mass
    zCOM = sum([obj.z*obj.mass for obj in objs])/total_mass
    
    return (xCOM, yCOM, zCOM)

if __name__ == "__main__":
    
    # Simple test with two arbitrary objects "a" and "b"
    
    a = MassObj(1,0,0,0)
    b = MassObj(1,2,3,4)
    objs = [a,b]
    
    CG_pos = FindCG(objs)
    
    print("xCOM: {}".format(CG_pos[0]))
    print("yCOM: {}".format(CG_pos[1]))
    print("zCOM: {}".format(CG_pos[2]))