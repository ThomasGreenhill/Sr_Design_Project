%% Script to call propeller design functions and check
%   Outputs confirmed to match expectation 02.10.2021 TVG

clear all
close all
clc
%% Input Parameter

airprops.k = 1.4;
airprops.Rgas = 287;
airprops.T = 272.3;
airprops.P = 75262.4;
airprops.rho = 0.962870;

Vinf = 156 * 0.514444;               % m/s
n = 2400 / 60;                 % Hz
B = 3;
Cl = 0.4;
R = 82 / 2 * 0.0254;                % m
Treq = 1474.9435422;         % N
a0 = -2*pi/180;                      

% Functions
Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;
m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ sqrt(1 - 0.9^2)) .* (Ma > 0.9);

%% Function calls
[r, c, bet, Pdesign, Tdesign, Qdesign, etap, the] = ...
    propdesign(airprops, R, Vinf, n, Treq, Cl, B, m0fn, a0, Cdfn);

fprintf("\nThe propeller power is %.2f hp\n", Pdesign * 0.00134102);

line1 = zeros(size(c));

plotblade3D(r, R, c, bet, B, line1);