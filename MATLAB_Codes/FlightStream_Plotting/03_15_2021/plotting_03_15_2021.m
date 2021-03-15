%% Plotting for geom v1.5 mod by XT, with FS data created around midnight on 03.14.2021
% TVG 03.15.2021

clc;
clear;
close all;
addpath("../../../Utilities/")
formatlatex()
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')

%% Plot the shoprt range refined
load('v1_4_polar_short_range_refined.mat')

figure
plot(v1_4_polar_short_range_refined(1:2:end-1,1), v1_4_polar_short_range_refined(1:2:end-1,7))
xlabel("$\alpha$ (deg)")
ylabel("$C_L$")
title("Lift Coefficient $C_L$ vs. Angle of Attack $\alpha$ from FlightStream for Geometry v1.5")
saveas(gcf,"./Figures/v1_4_polar_short_range_refined_Clva.jpg")

figure
plot(v1_4_polar_short_range_refined(1:2:end-1,7), v1_4_polar_short_range_refined(1:2:end-1,8)+v1_4_polar_short_range_refined(1:2:end-1,9))
xlabel("$C_L$")
ylabel("$C_{D_t}$")
title(["Total Aircraft Drag Coefficient $C_{D_t}$ vs. Lift Coefficient $C_L$", "from FlightStream for Geometry v1.5"])
saveas(gcf,"./Figures/v1_4_polar_short_range_refined_ClvCd.jpg")

figure
plot(v1_4_polar_short_range_refined(1:2:end-1,7), v1_4_polar_short_range_refined(1:2:end-1,11))
xlabel("$C_L$")
ylabel("$C_M$")
title("Lift Coefficient $C_L$ vs. $y$-Moment Coefficient $C_{m_y}$ from FlightStream for Geometry v1.5")
saveas(gcf,"./Figures/v1_4_polar_short_range_refined_CmvCl.jpg")