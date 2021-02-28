import sys
sys.path.append("../Python_Codes")
from Class130 import Airfoil
import os


foil = Airfoil("NACA   2412")

Re = 5e6
alf_start = 0
alf_end = 20

print(os.name)
print(os.name == 'nt')

#foil.polar(Re, alf_start, alf_end)