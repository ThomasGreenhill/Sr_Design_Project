%{
Plots the FS data from a given struct of data, stored in folder ./Figures
One .mat file is bounded by flap angle only

History:
    04.23.2021, XT. Created
%}

clear all
close all
clc

%% inputs (will move to function input)
filePath = "./FS Data/noflap.mat";
fieldReq = ["AoA", "Beta", "Velocity", "Cx", "Cy", "Cz", "CL", "CDi", "CDo", "CMx", "CMy", "CMz"];

%% Setup
saveDir = "./Figures";

if not(isfolder(saveDir))
   mkdir(saveDir); 
end

figWidth = 1000; figHeight = 800;
figXStart = 10; figYStart = 10;
figSize = [figXStart, figYStart, figWidth, figHeight];

%% Extracting data




