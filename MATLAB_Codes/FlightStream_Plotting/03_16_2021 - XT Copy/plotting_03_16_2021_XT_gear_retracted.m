%% Plotting for geom v1.5 mod by XT, with FS data created around midnight on 03.15.2021
% TVG 03.16.2021
clc;
clear all;
close all;
addpath("../../../Utilities/")
formatlatex()
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')

CDo = 0.019941411208039;
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
CD_nf_62l = CDi_nf_62l + CDo;
CD_nf_62z = CDi_nf_62z + CDo;
CD_nf_44z = CDi_nf_44z + CDo;

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
CD_fu_62l = CDi_fu_62l + CDo;
CD_fu_44z = CDi_fu_44z + CDo;
CD_fu_62z = CDi_fu_62z + CDo;

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
CD_fd_62l = CDi_fd_62l + CDo;
CD_fd_44z = CDi_fd_44z + CDo;
CD_fd_62z = CDi_fd_62z + CDo;

%%% Landing flap down
load('landing_flapdown.mat')

alp_landl = landing_flap_4down_38_long(:,1);
alp_landz = landing_flap_4down_38_zoomed(:,1);

CL_landl = landing_flap_4down_38_long(:,7);
CL_landz = landing_flap_4down_38_zoomed(:,7);

% Induced drag
CDi_landl = landing_flap_4down_38_long(:,8);
CDi_landz = landing_flap_4down_38_zoomed(:,8);

% Zero lift drag
CDo_landl = landing_flap_4down_38_long(:,9);
CDo_landz = landing_flap_4down_38_zoomed(:,9);

% Total drag
CD_landl = CDi_landl + CDo;
CD_landz = CDi_landz + CDo;

%% Plotting variables
sizeFont = 24;      % font size
sizeFig = [10, 10, 1500, 1200];     % size of figure
alf_ticks_long = -5:2.5:30;
alf_ticks_zoomed = -5:1:10;
CL_ticks_long = -1:0.25:2.5;
CL_ticks_zoomed = -0.5:0.25:1.5;
CD_ticks_long = 0:0.1:0.6;
CD_ticks_zoomed = 0:0.01:0.15;

%% Plot Long CL vs. Alpha
% Cruise
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(alp_nf_62l, CL_nf_62l, 'DisplayName', "No Flap")
hold on 
plot(alp_fu_62l, CL_fu_62l, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(alp_fd_62l, CL_fd_62l, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Angle of Attack $\alpha$ (deg)", 'FontSize', sizeFont)
ylabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
xticks(alf_ticks_long)
yticks(CL_ticks_long)
title(["Lift Coefficient vs. Angle of Attack for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection (Gear Retracted)"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CLva_all_ret.jpg")

% Landing
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(alp_landl, CL_landl, 'DisplayName', "Flap Down 4$^{\circ}$")
legend
xlabel("Angle of Attack $\alpha$ (deg)", 'FontSize', sizeFont)
ylabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
xticks(alf_ticks_long)
yticks(CL_ticks_long)
title(["Lift Coefficient vs. Angle of Attack for Jiffy Jerboa", "During Landing with Flap Down 4$^{\circ}$ (Gear Retracted)"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CLva_land_ret.jpg")

%% Plot long CD vs CL
% v = 62 m/s
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_62l, CD_nf_62l, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_62l, CD_fu_62l, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_62l, CD_fd_62l, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
ylabel("Total Airframe Drag Coefficient $C_D$", 'FontSize', sizeFont)
xticks(CL_ticks_long)
yticks(CD_ticks_long)
title(["Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection (Gear Retracted)"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_62_long_ret.jpg")

% Landing v = 38 m/s
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_landl, CD_landl, 'DisplayName', "No Flap Deflection")
legend
xlabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
ylabel("Total Airframe Drag Coefficient $C_D$", 'FontSize', sizeFont)
xticks(CL_ticks_long)
yticks(CD_ticks_long)
title(["Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Landing with Flap Down 4$^{\circ}$ (Gear Retracted)"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_land_long_ret.jpg")

%% Plot Zoomed CD vs CL
% v = 62 m/s
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_62z, CD_nf_62z, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_62z, CD_fu_62z, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_62z, CD_fd_62z, 'DisplayName', "Flap Down 4$^{\circ}$")
hold off
legend
xlabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
ylabel("Total Airframe Drag Coefficient $C_D$", 'FontSize', sizeFont)
xticks(CL_ticks_zoomed)
yticks(CD_ticks_zoomed)
xlim([-0.25, 0.75])
title(["Zoomed Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Cruise: 62 m/s with Varying Flap Deflection (Gear Retracted)"], 'FontSize', sizeFont)
hold on
scatter(0, CDo,1000,'+','k')
text(CL_fu_62z(29)+0.05,CDo,strcat("$C_{D_{0_{ret}}} =",num2str(CDo,4),"$"),'fontsize',18)
saveas(gcf,"./Figures/CDvCL_62_zoomed_ret.jpg")

% v = 44 m/s
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_nf_44z, CD_nf_44z, 'DisplayName', "No Flap Deflection")
hold on
plot(CL_fu_44z, CD_fu_44z, 'DisplayName', "Flap Up 4$^{\circ}$")
plot(CL_fd_44z, CD_fd_44z, 'DisplayName', "Flap Down 4$^{\circ}$")
legend
xlabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
ylabel("Total Airframe Drag Coefficient $C_D$", 'FontSize', sizeFont)
xticks(CL_ticks_zoomed)
yticks(CD_ticks_zoomed)
xlim([-0.25, 0.75])
title(["Zoomed Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Climb Cruise: 44 m/s with Varying Flap Deflection (Gear Retracted)"], 'FontSize', sizeFont)
scatter(0, CDo,1000,'+','k')
text(CL_fu_62z(29)+0.05,CDo,strcat("$C_{D_{0_{ret}}} =",num2str(CDo,4),"$"),'fontsize',18)
saveas(gcf,"./Figures/CDvCL_44_zoomed_ret.jpg")

% Landing v = 38 m/s
figure
% figure('Renderer', 'painters', 'Position', sizeFig)
plot(CL_landz, CD_landz, 'DisplayName', "No Flap Deflection")
legend
xlabel("Lift Coefficient $C_L$", 'FontSize', sizeFont)
ylabel("Total Airframe Drag Coefficient $C_D$", 'FontSize', sizeFont)
xticks(CL_ticks_zoomed)
yticks(CD_ticks_zoomed)
title(["Zoomed Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "During Landing with Flap Down 4$^{\circ}$ (Gear Retracted)"], 'FontSize', sizeFont)
saveas(gcf,"./Figures/CDvCL_land_zoomed_ret.jpg")

%%
LD62 = CL_nf_62l./CD_nf_62l;
LD44 = CL_nf_44z./CD_nf_44z;
