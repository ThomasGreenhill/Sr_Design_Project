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

alp_nf_62l = noflap62long(:,1);
alp_nf_44l = noflap44long(:,1);
alp_nf_62z = noflap62zoomed(:,1);
alp_nf_44z = noflap44zoomed(:,1);

CL_nf_62l = noflap62long(:,7);
CL_nf_44l = noflap44long(:,7);
CL_nf_62z = noflap62zoomed(:,7);
CL_nf_44z = noflap44zoomed(:,7);

% Induced drag
CDi_nf_62l = noflap62long(:,8);
CDi_nf_44l = noflap44long(:,8);
CDi_nf_62z = noflap62zoomed(:,8);
CDi_nf_44z = noflap44zoomed(:,8);

% Zero lift drag
CDo_nf_62l = noflap62long(:,9);
CDo_nf_44l = noflap44long(:,9);
CDo_nf_62z = noflap62zoomed(:,9);
CDo_nf_44z = noflap44zoomed(:,9);

% Total drag
CD_nf_62l = CDi_nf_62l + CDo_nf_62l;
CD_nf_44l = CDi_nf_44l + CDo_nf_44l;
CD_nf_62z = CDi_nf_62z + CDo_nf_62z;
CD_nf_44z = CDi_nf_44z + CDo_nf_44z;

%%% Flaps up data
load('flapup.mat')

alp_fu_62l = flapup62long(:,1);
alp_fu_44l = flapup44long(:,1);
alp_fu_62z = flapup62zoomed(:,1);
% alp_fu_44z = flapup44zoomed(:,1);

CL_fu_62l = flapup62long(:,7);
CL_fu_44l = flapup44long(:,7);
CL_fu_62z = flapup62zoomed(:,7);
% CL_fu_44z = flapup44zoomed(:,7);

% Induced drag
CDi_fu_62l = flapup62long(:,8);
CDi_fu_44l = flapup44long(:,8);
CDi_fu_62z = flapup62zoomed(:,8);
% CDi_fu_44z = flapup44zoomed(:,8);

% Zero lift drag
CDo_fu_62l = flapup62long(:,9);
CDo_fu_44l = flapup44long(:,9);
CDo_fu_62z = flapup62zoomed(:,9);
% CDo_fu_44z = flapup44zoomed(:,9);

% Total drag
CD_fu_62l = CDi_fu_62l + CDo_fu_62l;
CD_fu_44l = CDi_fu_44l + CDo_fu_44l;
CD_fu_62z = CDi_fu_62z + CDo_fu_62z;
% CD_fu_44z = CDi_fu_44z + CDo_fu_44z;

%% Plot Long CL vs. Alpha
%%% No flaps
figure
plot(alp_nf_62l,CL_nf_62l,'DisplayName',"Cruise: 62 m/s")
hold on
plot(alp_nf_44l,CL_nf_44l,'DisplayName',"Climb: 44 m/s")
legend
xlabel("Angle of Attack $\alpha$ (deg)")
ylabel("Lift Coefficient $C_L$")
title(["Lift Coefficient vs. Angle of Attack for Jiffy Jerboa", "During Climb and Cruise with No Flap Deflection"],'FontSize',30)
saveas(gcf,"./Figures/CLva_noflap.jpg")

%%% Flaps up
figure
plot(alp_fu_62l,CL_fu_62l,'DisplayName',"Cruise: 62 m/s")
hold on
plot(alp_fu_44l,CL_fu_44l,'DisplayName',"Climb: 44 m/s")
legend
xlabel("Angle of Attack $\alpha$ (deg)")
ylabel("Lift Coefficient $C_L$")
title(["Lift Coefficient vs. Angle of Attack for Jiffy Jerboa", "During Climb and Cruise with Flap Up 4$^{\circ}$"],'FontSize',30)
saveas(gcf,"./Figures/CLva_flapup.jpg")


%% Plot Zoomed CD vs CL
figure
plot(CL_nf_62l,CD_nf_62l,'DisplayName',"No Flap Deflection")
hold on
plot(CL_fu_62l,CD_fu_62l,'DisplayName',"Flap Up 4$^{\circ}$")
legend
xlabel("Lift Coefficient $C_L$")
ylabel("Total Airframe Drag Coefficient $C_D$")
title(["Drag Coefficient vs. Lift Coefficient for Jiffy Jerboa", "with Varying Flap Deflection"],'FontSize',30)
saveas(gcf,"./Figures/CDvCL.jpg")