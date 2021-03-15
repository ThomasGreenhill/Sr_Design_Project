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


%% Plot the long range unrefined
load('polar_long_range.mat')

figure
plot(polarlongrange(:,1), polarlongrange(:,7))
xlabel("$\alpha$ (deg)")
ylabel("$C_L$")
title("Lift Coefficient $C_L$ vs. Angle of Attack $\alpha$ from FlightStream for Geometry v1.5")
saveas(gcf,"./Figures/polarlongrange_Clva.jpg")

%% Plot the long range refined
load('polar_long_range_refined.mat')

figure
plot(polarlongrangerefined(:,1), polarlongrangerefined(:,7))
xlabel("$\alpha$ (deg)")
ylabel("$C_L$")
title("Lift Coefficient $C_L$ vs. Angle of Attack $\alpha$ from FlightStream for Geometry v1.5")
saveas(gcf,"./Figures/polarlongrangerefined_Clva.jpg")

figure
plot(polarlongrangerefined(:,7), polarlongrangerefined(:,8)+polarlongrangerefined(:,9))
xlabel("$C_L$")
ylabel("$C_{D_t}$")
title(["Total Aircraft Drag Coefficient $C_{D_t}$ vs. Lift Coefficient $C_L$", "from FlightStream for Geometry v1.5"])
saveas(gcf,"./Figures/polarlongrangerefined_ClvCd.jpg")


%% Plot the refined for drag bucket evaluation
load('polar_refined_alf_2_8.mat')

figure
plot(polarzoomedalf28txt(:,7), polarzoomedalf28txt(:,8)+polarzoomedalf28txt(:,9))
xlabel("$C_L$")
ylabel("$C_{D_t}$")
title(["Total Aircraft Drag Coefficient $C_{D_t}$ vs. Lift Coefficient $C_L$", "from FlightStream for Geometry v1.5"])
saveas(gcf,"./Figures/polarzoomedalf28_ClvCd.jpg")

