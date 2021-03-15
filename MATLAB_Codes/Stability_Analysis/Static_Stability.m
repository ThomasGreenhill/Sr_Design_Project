%% Code to compute the static margin of our aircraft (geom v1.5)
% TVG 03.15.2021

clc;
clear;
close all;
addpath("../../../Utilities/")
formatlatex()
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')
%% Geom v1.5 info
S = 16; %m^2
S_h = 3.007; %m^2
eta_h = 0.7; % Assumed
AR = 10; 
AR_h = 4.5;
depsda = 0.1; % Assumed
cbar = 1.26491; %m
cbar_h = 0.81745; %m
x_AC_h = 0.25*cbar_h + 7.75 - 3; %m
e_wf = 0.8; % Assumed
e_h = 0.7; % Assumed
%% Calculate the location of the aerodynamic center in the x-direction
Cla = 0.11; %deg^-1
CLa_wf = Cla/(1+57.3*Cla/(pi*e_wf*AR));
CLa_h = Cla/(1+57.3*Cla/(pi*e_h*AR_h));

xbar_AC = x_AC_fn(S, S_h, 0.25, x_AC_h, cbar, CLa_wf, CLa_h, depsda, eta_h);

% xbar_CG = (3.547-3)/cbar; % Empty
% xbar_CG = (0.62)/cbar; % OWE
xbar_CG = (0.43)/cbar; % TOGW

SM = (xbar_AC-xbar_CG)