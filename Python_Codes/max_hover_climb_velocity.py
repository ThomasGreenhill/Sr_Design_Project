# Iterator to calculate the max hover climb velocity for 
# jIfFy jErBoA
# TVG 03.17.2021

P_max_cont = 384e3
P_hover = 248e3
TOGW = 13000
fbody = 32
rho = 1.225

P_drag = lambda V : 0.5*fbody*rho*V**3

# Guess vinf
V = 8

for iter in range(100):
    V = (P_max_cont-P_hover-P_drag(V))/TOGW

print(V)