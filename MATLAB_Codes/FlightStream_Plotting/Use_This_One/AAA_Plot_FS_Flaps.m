%{
Plots the FS data from a given struct of data, stored in folder ./Figures
One .mat file is bounded by flap angle only

History:
    04.23.2021, XT. Created
%}

clear
close all
clc
%% input parameters (could change)
dirPath = "./FS Data";
version = "v1.5";
fileType = ".mat";
fieldReq = ["AoA", "Beta", "Velocity", "Cx", "Cy", "Cz", "CL", "CDi", "CDo", "CMx", "CMy", "CMz"];

save_or_not = true;
show_or_not = true;
%% Setup
saveDir = "./Figures";
saveInfo.save = save_or_not;
saveInfo.path = strcat(saveDir, "/", version, "/");
saveInfo.saveType = ".png";

if (saveInfo.save == true) && not(isfolder(saveInfo.path))
   mkdir(saveInfo.path); 
end

if show_or_not == false
    set(0,'DefaultFigureVisible','off');
else
    set(0,'DefaultFigureVisible','on');
end

figWidth = 2000; figHeight = 1000;
figXStart = 10; figYStart = 10;
figSize = [figXStart, figYStart, figWidth, figHeight];

%% Extracting data
% cruise_long
fileName = "cruise_long";
cruise_long = load(strcat(dirPath, "/", version, "/", fileName, fileType));

fileName = "cruise_zoomed";
cruise_zoomed = load(strcat(dirPath, "/", version, "/", fileName, fileType));

%fileName = "climb_long";
%climb_long = load(strcat(dirPath, "/", version, "/", fileName, fileType));

fileName = "climb_zoomed";
climb_zoomed = load(strcat(dirPath, "/", version, "/", fileName, fileType));

fileName = "CTOL_long";
CTOL_long = load(strcat(dirPath, "/", version, "/", fileName, fileType));

fileName = "CTOL_zoomed";
CTOL_zoomed = load(strcat(dirPath, "/", version, "/", fileName, fileType));

%% Plot cruise long
caseName = "Cruise, Long";
lgd = ["$0^o$ flap", "$4^o$ flap up", "$4^o$ flap down"];
cruise_long_lc = PlotLiftCurve(cruise_long, caseName, lgd, figSize, saveInfo);
cruise_long_dp = PlotDragPolar(cruise_long, caseName, lgd, figSize, saveInfo);

%% Plot cruise zoomed
caseName = "Cruise, Zoomed";
lgd = ["$0^o$ flap", "$4^o$ flap up", "$4^o$ flap down"];
%cruise_zoomed_lc = PlotLiftCurve(cruise_zoomed, caseName, lgd, figSize, saveInfo);
cruise_zoomed_dp = PlotDragPolar(cruise_zoomed, caseName, lgd, figSize, saveInfo);

%% Plot climb zoomed
caseName = "Climb, Zoomed";
lgd = ["$0^o$ flap", "$4^o$ flap up", "$4^o$ flap down"];
%climb_zoomed_lc = PlotLiftCurve(climb_zoomed, caseName, lgd, figSize, saveInfo);
climb_zoomed_dp = PlotDragPolar(climb_zoomed, caseName, lgd, figSize, saveInfo);

%% Plot landing long
caseName = "Conventional Landing, Long";
lgd = ["$4^o$ flap down"];
landing_long_lc = PlotLiftCurve(CTOL_long, caseName, lgd, figSize, saveInfo);
landing_long_dp = PlotDragPolar(CTOL_long, caseName, lgd, figSize, saveInfo);

%% Plot landing zoomed
caseName = "Conventional Landing, Zoomed";
lgd = ["$4^o$ flap down"];
%landing_zoomed_lc = PlotLiftCurve(CTOL_zoomed, caseName, lgd, figSize, saveInfo);
landing_zoomed_dp = PlotDragPolar(CTOL_zoomed, caseName, lgd, figSize, saveInfo);

%%
set(0,'DefaultFigureVisible','on');

close all
clear 
clc
