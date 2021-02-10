%% propdesign.m
% Code to design a propeller, based on EAE 130A project 2
%
%   Inputs:
%       airprops: struc of air properties at desired conditions
%       R: Propeller radius
%       Vinf: Air velocity at propeller inlet
%       n: Propeller angular rate (Hz)
%       Treq: Required thrust
%       Cl: Blade sectional lift coefficient -- typical 0.4
%       B: Number of blades
%       m0fn: Kind of like lift curve slope function -- typical:
%           m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ ...
%              sqrt(1 - 0.9^2)) .* (Ma > 0.9);
%       a0: Blade sectional zero-lift angle of attack
%       Cdfn: Blade sectional drag coefficient -- typical:
%           Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;
%  
%   Outputs: 
%       r: Vector of nn points from 0 to R along a blade
%       c: Vector of blade design chord distribution
%       bet: Vector of blade design pitch angle distribution
%       Pdesign: Propeller design power
%       Tdesign: Propeller design thrust
%       Qdesign: Propeller design torque
%       etap: Propeller design efficiency
%       the: Propeller design theta angle
%
%   Calls:
%       {none}
%
%   Notes:
%       1. 02.09.2021 implementation uses sea level standard atmosphere
%       
%   History:
%       02.09.2021: Imported from previous project, TVG
%       02.09.2021: Modified header, XT
%       02.10.2021: Added air properties as an input and debugged using
%           propdesign_check.m

function [r, c, bet, Pdesign, Tdesign, Qdesign, etap, the] = ...
    propdesign(airprops, R, Vinf, n, Treq, Cl, B, m0fn, a0, Cdfn)
k = airprops.k;
Rgas = airprops.Rgas;
T = airprops.T;
P = airprops.P;
rho = airprops.rho; %kg/m^3
nn = 201;

K = 0.94;

D = 2 * R;
r = linspace(0.15*R, R, nn);
x = r / R;
tc = 0.04 ./ x.^1.2;

a = sqrt(k*Rgas*T);

Ma = Vinf / a;

MDD = K - tc - Cl / 10;

J = Vinf / (n * D);
ome = 2 * pi * n; %rad/s
phi = atan(J./(pi * x)); %rad
VR = sqrt(Vinf^2+(ome * r).^2);
M = VR / a;

if max(M) > max(MDD)
    fprintf("Error, M>MDD \n \n");
    fprintf("M = %f \n", max(M));
    fprintf("MDD = %f \n", max(MDD));

    fprintf("Drag Divergence Mach Number Exceeded \n \n");
    dragdiverg = true;
else
    dragdiverg = false;
end

m0 = m0fn(M);

% Prepare for iteration
% Initial values:
v0 = 0.1 * ones(1, nn);
Tdesign = 2.2e3;
iter = 1;
iterlim = 1e3;

if Tdesign == Treq
    fprintf("Error: Trequired = Tdesign. Either change Trequired or modify initial value of Tdesign in code")
    return
end

while round(Tdesign, 10) ~= round(Treq, 10) && iter < iterlim
    the = atan((Vinf+v0)./(2 * pi * n * r)) - phi; %rad

    % Cl is fixed, calculate c:
    sig = 8 * x .* the .* cos(phi) .* tan(the+phi) ./ Cl; %rad
    c = sig * pi * R / B;

    alp = Cl ./ m0 + a0;
    bet = alp + phi + the;
    Cd = Cdfn(Cl);

    lamT = 1 ./ (cos(phi)).^2 .* (Cl * cos(phi + the) - Cd * sin(phi + the));
    lamQ = 1 ./ (cos(phi)).^2 .* (Cl * sin(phi + the) + Cd * cos(phi + the));

    dCTdx = sig * pi^3 .* x.^2 / 8 .* lamT;
    dCQdx = sig * pi^3 .* x.^3 / 16 .* lamQ;

    xx = x(x >= 0.15);

    CT = trapz(xx, dCTdx(x >= 0.15));
    CQ = trapz(xx, dCQdx(x >= 0.15));

    AF = 10^5 / 16 * trapz(xx, c(x >= 0.15)/D.*x(x >= 0.15).^3);
    CLdes = 4 * trapz(xx, Cl*x(x >= 0.15).^3);

    CP = 2 * pi * CQ;

    etap = CT / CP * J;
    Tdesign = CT * rho * n^2 * D^4;
    

    if Tdesign < Treq
        v0 = v0 * (1 - (Tdesign - Treq) / abs(Tdesign + Treq));
    elseif Tdesign > Treq
        v0 = v0 * (1 - (Tdesign - Treq) / abs(Tdesign + Treq));
    else
        break
    end
    iter = iter + 1;

end

Pdesign = CP * rho * n^3 * D^5;
Qdesign = CQ * rho * n^2 * D^5;

if dragdiverg
    return;
end

end
