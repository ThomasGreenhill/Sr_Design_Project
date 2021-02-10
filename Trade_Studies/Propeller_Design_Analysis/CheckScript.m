%% Script to call propeller design functions and check

clear all
close all
clc
%% Input Parameter
Vinf = 87 * 0.514444;               % m/s
n = 1854.4805 / 60;                 % Hz
B = 3;
Cl = 0.4;
R = 82 / 2 * 0.0254;                % m
Treq =  425.6896 * 4.44822;         % N
a0 = 330.803;                       % m/s

Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;
m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ sqrt(1 - 0.9^2)) .* (Ma > 0.9);

%% Function calls
[r, c, bet, Pdesign, Tdesign, Qdesign, etap, the] = propdesign(R, Vinf, n, Treq, Cl, B, m0fn, a0, Cdfn);

Pdesign = Pdesign * 0.00134102;
