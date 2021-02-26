%% Fuel_Cell_Comparison.m
% SCRIPT to plot and compare different fuel cell performances 
%
%   Inputs:
%       fuelcelldata.mat
%   
%   Outputs:
%       plots
%
%   Notes:
%       
%
%   History:
%       02.06.2021: Created, TVG
%

clc;
clear;
close all;
addpath("../Utilities")
formatlatex()
warning('off', 'all')
mkdir("./Figures")
warning('on', 'all')
format shortG
%% Load data
load("fuelcelldata.mat")

%% Plot the specific power (power to weight ratio)
% Added 40% weight for the fuel cells that do not have submodules speficied

figure
X = categorical(fuelcelldata.Names);
X = reordercats(X,fuelcelldata.Names);
bar(X,fuelcelldata.RatedPower.Data./fuelcelldata.TotalWeight.Data)
ylabel("Specific Power (W/kg)")
xlabel("H$_2$ Fuel Cell Model")
title("Ballard Fuel Cell Specific Power",'FontSize',26)
saveas(gcf,"./Figures/figure.jpg")