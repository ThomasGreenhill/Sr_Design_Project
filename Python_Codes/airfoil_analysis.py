from Class130 import Airfoil, AtmData


# Use XFOIL to test the stall angle of NLF 0414 F airfoil

foilpath = '../Sizing/OpenVSP/v1.5_03_13_2021/Airfoil/NLF 0414F.dat'
foilname = 'NLF0414'

# Atm
h = 6000 / 3.28084  # ft
vel = 62    # m/s
is_SI = True
atm = AtmData(vel, h, is_SI)

c = 1
Re = (atm.dens * atm.vel * c) / atm.visc

alf_start = 0
alf_end = 80
num_alfs = 50
iter_num = 100

foil = Airfoil(foilname)
foil.set_iter_num(iter_num)
foil.set_num_alfs(num_alfs)
foil.add_geom_file(foilpath)
foil.get_polar(Re, alf_start, alf_end)
foil.lift_curve()
foil.drag_polar()