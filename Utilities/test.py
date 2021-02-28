import sys
sys.path.append("../Python_Codes")
from Class130 import Airfoil
import pandas as pd
import os


foil = Airfoil("NACA   2412")

Re = 5e6
alf_start = 0
alf_end = 5

polar = foil.polar(Re, alf_start, alf_end)
alf_col = polar["alpha"]
for item in alf_col:
    print(item)
