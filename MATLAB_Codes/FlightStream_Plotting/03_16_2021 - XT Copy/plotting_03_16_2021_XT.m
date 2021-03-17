%% Plotting for geom v1.5 mod by XT, with FS data created around midnight on 03.15.2021
% TVG 03.16.2021
clc;
clear;
close all;
addpath("../../../Utilities/")
formatlatex()
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')

%% Load the data
%%% No flaps data
load('noflap.mat')

alp_nf_62l = no_flap_62_long(:,1);
alp_nf_62z = no_flap_62_zoomed(:,1);
alp_nf_44z = no_flap_44_zoomed(:,1);

CL_nf_62l = no_flap_62_long(:,7);
CL_nf_62z = no_flap_62_zoomed(:,7);
CL_nf_44z = no_flap_44_zoomed(:,7);

% Induced drag
CDi_nf_62l = no_flap_62_long(:,8);
CDi_nf_62z = no_flap_62_zoomed(:,8);
CDi_nf_44z = no_flap_44_zoomed(:,8);

% Zero lift drag
CDo_nf_62l = no_flap_62_long(:,9);
CDo_nf_62z = no_flap_62_zoomed(:,9);
CDo_nf_44z = no_flap_44_zoomed(:,9);

% Total drag
CD_nf_62l = CDi_nf_62l + CDo_nf_62l;
CD_nf_62z = CDi_nf_62z + CDo_nf_62z;
CD_nf_44z = CDi_nf_44z + CDo_nf_44z;

%%% Flaps up data
load('flapup.mat')

alp_fu_62l = flap_4up_62_long(:,1);
alp_fu_44z = flap_4up_44_zoomed(:,1);
alp_fu_62z = flap_4up_62_zoomed(:,1);

CL_fu_62l = flap_4up_62_long(:,7);
CL_fu_44z = flap_4up_44_zoomed(:,7);
CL_fu_62z = flap_4up_62_zoomed(:,7);

% Induced drag
CDi_fu_62l = flap_4up_62_long(:,8);
CDi_fu_44z = flap_4up_44_zoomed(:,8);
CDi_fu_62z = flap_4up_62_zoomed(:,8);

% Zero lift drag
CDo_fu_62l = flap_4up_62_long(:,9);
CDo_fu_44z = flap_4up_44_zoomed(:,9);
CDo_fu_62z = flap_4up_62_zoomed(:,9);

% Total drag
CD_fu_62l = CDi_fu_62l + CDo_fu_62l;
CD_fu_44z = CDi_fu_44z + CDo_fu_44z;
CD_fu_62z = CDi_fu_62z + CDo_fu_62z;

%%% Flaps down data
load('flapdown.mat')

alp_fd_62l = flap_4down_62_long(:,1);
alp_fd_44z = flap_4down_44_zoomed(:,1);
alp_fd_62z = flap_4down_62_zoomed(:,1);

CL_fd_62l = flap_4down_62_long(:,7);
CL_fd_44z = flap_4down_44_zoomed(:,7);
CL_fd_62z = flap_4down_62_zoomed(:,7);

% Induced drag
CDi_fd_62l = flap_4down_62_long(:,8);
CDi_fd_44z = flap_4down_44_zoomed(:,8);
CDi_fd_62z = flap_4down_62_zoomed(:,8);

% Zero lift drag
CDo_fd_62l = flap_4down_62_long(:,9);
CDo_fd_44z = flap_4down_44_zoomed(:,9);
CDo_fd_62z = flap_4down_62_zoomed(:,9);

% Total drag
CD_fd_62l = CDi_fd_62l + CDo_fd_62l;
CD_fd_44z = CDi_fd_44z + CDo_fd_44z;
CD_fd_62z = CDi_fd_62z + CDo_fd_62z;

%% Plotting variables
sizeFont = 20;      % font size
sizeFig = [10, 10, 2200, 1800];     % size of figure
alf_ticks_long = -5:2.5:30;
alf_ticks_zoomed = -5:1:10;
CL_ticks_long = -1:0.25:2.5;
CL_ticks_zoomed = -0.5:0.25:1.5;
CD_ticks_long = 0:0.1:0.6;
CD_ticks_zoomed = 0:0.01:0.15;

%% Plot Long CL vs. Alpha
figure
figure('Renderer', 'painters', 'Position', sizeFig)
plot(alp_nf_62l, CL_nf_62l, 'DisplayName', "No Flap")
hold on 
plot(alp_fu_62l, CL_fu_62l, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(alp_fd_62l, CL_fd_62l, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Angle of Attack $\alpha$ (deg)")
ylabel("Lift Coefficient $C_L$")
xticks(alf_ticks_long)
yticks(CL_ticks_long)
title(["Lift Coefficient vs. Angle of Attack for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CLva_all.jpg")

%% Plot long CD vs CL
% v = 62 m/s
figure
figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_62l, CD_nf_62l, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_62l, CD_fu_62l, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_62l, CD_fd_62l, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Lift Coefficient $C_L$")
ylabel("Total Airframe Drag Coefficient $C_D$")
xticks(CL_ticks_long)
yticks(CD_ticks_long)
title(["Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_62_long.jpg")

%% Plot Zoomed CD vs CL
% v = 62 m/s
figure
figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_62z, CD_nf_62z, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_62z, CD_fu_62z, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_62z, CD_fd_62z, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Lift Coefficient $C_L$")
ylabel("Total Airframe Drag Coefficient $C_D$")
xticks(CL_ticks_zoomed)
yticks(CD_ticks_zoomed)
title(["Zoomed Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_62_zoomed.jpg")

% v = 44 m/s
figure
figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_44z, CD_nf_44z, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_44z, CD_fu_44z, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_44z, CD_fd_44z, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Lift Coefficient $C_L$")
ylabel("Total Airframe Drag Coefficient $C_D$")
xticks(CL_ticks_zoomed)
yticks(CD_ticks_zoomed)
title(["Zoomed Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Climb Cruise: 44 m/s with Varying Flap Deflection"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_44_zoomed.jpg")

%%
close all
clear all
clc

