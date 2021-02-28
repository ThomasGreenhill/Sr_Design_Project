import sys

sys.path.append("../Python_Codes")
from Class130 import Airfoil

foil = Airfoil("NACA   2412")

Re = 5e6
alf_start = 0
alf_end = 5

plr = foil.get_polar(Re, alf_start, alf_end)
foil.geom_plot(save=True, show=False)
foil.lift_curve(save=True, show=False)
foil.drag_polar(save=True, show=False)
