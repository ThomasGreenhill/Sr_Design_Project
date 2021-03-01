%% EAE 130A Project #2: Propeller Design and Analysis
% TVG 01.22.2021

clc;
clear;
close all;
formatlatex()
warning('off', 'all')
mkdir './Figures'
warning('on', 'all')

%% Global Variables
global k Rgas T P rho nn K
k = 1.4;
Rgas = 1717;
T = 490.17; %R
P = 1.5721e3; %lbf/ft^2
rho = 1.8685e-3; %slugs/ft^3
nn = 201;
K = 0.94;

%% Design Variables
R = 82 / 2 / 12; %ft (according to C182RG flight manual)
Vinf = 156 * 1.68781; %ft/s (156 knots assumed)
% Vinf = 1;
n = 2400 / 60; %RPS (235 BHP at 2400 RPM);
Peng = 177 * 550.000037; %lbf.ft/s

Cl = 0.4; % Assumed
B = 3; % Number of blades
m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ ...
    sqrt(1 - 0.9^2)) .* (Ma > 0.9); % (lift curve slope, assumed)
a0 = -2 * pi / 180; % Assumed
Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;

% Engine power function from figure 2 (uses cubic interpolation)
Pengdata = [2400, 177; 2300, 170; 2200, 165; 2100, 158; 2000, 150; 1900, ...
    141; 1800, 131];
Pengfn = @(RPM) 550.000037 * pchip(Pengdata(:, 1), Pengdata(:, 2), RPM);

%% Design the propeller, optimized for diameter

% Rseq = R - 2:0.01:R;
Rseq = R;
etap = zeros(size(Rseq));


for ii = 1:length(Rseq)
    [r{ii}, c{ii}, bet{ii}, Pdesign{ii}, Tdesign{ii}, Qdesign{ii}, ...
        etap(ii), the{ii}] = propdesign(Rseq(ii), Vinf, n, PengS, Cl, ...
        B, m0fn, a0, Cdfn);
end

[~, jj] = max(etap);


Ropt = Rseq(jj);
ropt = r{jj};
copt = c{jj};
betopt = bet{jj};
Pdesignopt = Pdesign{jj};
Tdesignopt = Tdesign{jj};
Qdesignopt = Qdesign{jj};
etapopt = etap(jj);
theopt = the{ii};

straightline = zeros(1, nn);

plotblades2D(r{jj}, Rseq(jj), c{jj}, B, straightline)
title([strcat("2D View of Optimal Propeller Design, Diameter = ", ...
    num2str(2 * Ropt), " (ft)"), strcat("Mean Chord = ", ...
    num2str(mean(c{jj}) * 12), " (in), $\beta_{0.75R} = ", ...
    num2str(bet{jj}(uint64(length(r{jj}) * 0.75)) * 180 / pi), ...
    "^{\circ}$")], 'FontSize', 24)
saveas(gcf, "./Figures/design_2dview.jpg")

plotblade3D(r{jj}, Rseq(jj), c{jj}, bet{jj}, B, straightline)
title([strcat("3D View of Optimal Propeller Design, Diameter = ", ...
    num2str(2 * Ropt), " (ft)"), strcat("Mean Chord = ", ...
    num2str(mean(c{jj}) * 12), " (in), $\beta_{0.75R} = ", ...
    num2str(bet{jj}(uint64(length(r{jj}) * 0.75)) * 180 / pi), ...
    "^{\circ}$")], 'FontSize', 24)
saveas(gcf, "./Figures/design_3dview.jpg")

plotbladeprops(Ropt, r{jj}, c{jj}, bet{jj}, Cl)
saveas(gcf, "./Figures/design_properties.jpg")

figure
sgtitle("Propeller Chord Distribution", 'FontSize', 24)
subplot(2, 1, 1)
plot(ropt/Ropt, copt*12)
xlabel("$x = r/R$")
ylabel("$c$ (in)")
xlim([0.15, 1])

subplot(2, 1, 2)
plot(ropt/Ropt, copt/(2 * Ropt))
xlabel("$x = r/R$")
ylabel("$c/D$")
xlim([0.15, 1])
saveas(gcf, "./Figures/design_chorddistr.jpg")

%% Analyze the fixed-pitch propeller design
Vseq = linspace(55, 160, 101) * 1.68781; %ft/s


for ii = 1:length(Vseq)
    [J(ii), Pd(ii), CP(ii), Td(ii), CT(ii), etapd(ii)] = ...
        propanalysis(Ropt, Vseq(ii), n, B, m0fn, a0, Cdfn, copt, betopt);
end

plotpropanalysis(Vseq, J, Pd, CP, Td, CT, etapd);
saveas(gcf, "./Figures/analysis_properties.jpg")

Vclimb = 87 * 1.68781; %ft/s

%% Additional Analysis on the variable-pitch propeller design
Vseq = Vclimb - 30:3:Vclimb + 126;

for ii = 1:length(Vseq)
    iterlim = 1e3;

    %%% Determine the efficiency with fixed pitch by varying the angular rate
    % until the propeller power matches the engine power at that angular rate.
    % Initial values for iteration
    nfix = 2000 / 60;
    iter = 1;
    Pdfix(ii) = 0;


    while round(Pdfix(ii), 4) ~= round(Pengfn(nfix * 60), 4) && iter <= iterlim
        Pnfix = Pengfn(nfix*60);
        [Jfix(ii), Pdfix(ii), ~, Tdfix(ii), ~, etapfix(ii)] = ...
            propanalysis(Ropt, Vseq(ii), nfix, B, m0fn, a0, Cdfn, copt, betopt);

        if Pdfix(ii) < Pnfix
            nfix = nfix * (1 + 0.5 * (Pnfix - Pdfix(ii)) / (Pnfix + Pdfix(ii)));

        elseif Pdfix(ii) > Pnfix
            nfix = nfix * (1 + 0.5 * (Pnfix - Pdfix(ii)) / (Pnfix + Pdfix(ii)));

        else
            break
        end

        iter = iter + 1;

    end


    %%% Optimize the blade variation for climb:
    % Initial values for iteration
    if Vseq(ii) < Vinf
        dbet = 5 * pi / 180 / (Vinf - Vclimb) * Vseq(ii) - 5 * pi / ...
            180 / (Vinf - Vclimb) * Vinf;
    else
        dbet = 2 * pi / 180;
    end

    iter = 1;
    Pdvar(ii) = 0;

    while round(Pdvar(ii), 6) ~= round(Peng, 6) && iter <= iterlim
        [Jvar(ii), Pdvar(ii), ~, Tdvar(ii), ~, etapvar(ii)] = ...
            propanalysis(Ropt, Vseq(ii), n, B, m0fn, a0, Cdfn, copt, betopt+dbet);

        if Pdvar(ii) < 0
            Pdvar(ii) = 10;
        end

        if Pdvar(ii) < Peng && dbet < 0
            dbet = dbet * (1 - 2 * (Peng - Pdvar(ii)) / (Peng + Pdvar(ii)));
        elseif Pdvar(ii) > Peng && dbet < 0
            dbet = dbet * (1 - 2 * (Peng - Pdvar(ii)) / (Peng + Pdvar(ii)));
        elseif Pdvar(ii) < Peng && dbet >= 0
            dbet = dbet * (1 + 2 * (Peng - Pdvar(ii)) / (Peng + Pdvar(ii)));
        elseif Pdvar(ii) > Peng && dbet >= 0
            dbet = dbet * (1 + 2 * (Peng - Pdvar(ii)) / (Peng + Pdvar(ii)));
            if round(dbet, 14) == 0
                break
            end
        else
            break
        end
        iter = iter + 1;
    end

    % Difference in efficiency between fixed and variable pitch
    detap(ii) = (-etapfix(ii) + etapvar(ii)) / etapfix(ii);
    dT(ii) = (-Tdfix(ii) + Tdvar(ii)) / Tdfix(ii);
    deltabeta(ii) = dbet;
    RPMfix(ii) = nfix * 60;
end

%% Additional Plotting
close all
figure('Position', [100, 100, 1000, 1500])
sgtitle(["Performance Comparison Between Variable Pitch Propeller", ...
    "and Fixed Pitch Propeller"], 'fontsize', 30)
subplot(5, 1, 1)
h1 = plot(Vseq/1.68781, Pdfix/550, 'displayname', 'Fixed');
hold on
text(Vclimb/1.68781, Pdfix(Vseq == Vclimb)/550-10, strcat("$P_{fixed} = ", ...
    num2str(Pdfix(Vseq == Vclimb) / 550), "$ HP"), 'FontSize', 16)

h2 = plot(Vseq/1.68781, Pdvar/550, 'DisplayName', 'Variable');
ylabel("Propeller Power (HP)")
xlabel("Flight Speed (kn)")
title("Propeller Power vs. Airspeed for Variable and Fixed Pitch Propellers")
h3 = plot([Vclimb / 1.68781, Vclimb / 1.68781], [110, 190], ':k');
ylim([110, 180])
text(Vclimb/1.68781, Pdvar(Vseq == Vclimb)/550-10, strcat("$P_{variable} = ", ...
    num2str(Pdvar(Vseq == Vclimb) / 550), "$ HP"), 'FontSize', 16)
legend([h1, h2], 'Location', 'best')

subplot(5, 1, 2)
h1 = plot(Vseq/1.68781, Tdfix, 'displayname', 'Fixed');
hold on
text(Vclimb/1.68781, Tdfix(Vseq == Vclimb)-50, strcat("$T_{fixed} = ", ...
    num2str(Tdfix(Vseq == Vclimb)), "$ lbf"), 'FontSize', 16)

h2 = plot(Vseq/1.68781, Tdvar, 'DisplayName', 'Variable');
ylabel("Propeller Thrust (lbf)")
xlabel("Flight Speed (kn)")
title("Propeller Thrust vs. Airspeed for Variable and Fixed Pitch Propellers")
h3 = plot([Vclimb / 1.68781, Vclimb / 1.68781], [300, 700], ':k');
ylim([300, 700])
text(Vclimb/1.68781, Tdvar(Vseq == Vclimb)+50, strcat("$T_{variable} = ", ...
    num2str(Tdvar(Vseq == Vclimb)), "$ lbf"), 'FontSize', 16)
legend([h1, h2], 'Location', 'best')

subplot(5, 1, 3)
h1 = plot(Vseq/1.68781, etapfix, 'displayname', 'Fixed');
hold on
text(Vclimb/1.68781, etapfix(Vseq == Vclimb)+0.07, ...
    strcat("$\eta_{p_{fixed}} = ", num2str(etapfix(Vseq == Vclimb)), ...
    "$"), 'FontSize', 16)

h2 = plot(Vseq/1.68781, etapvar, 'DisplayName', 'Variable');
ylabel("Propeller Efficiency")
xlabel("Flight Speed (kn)")
title("Propeller Efficiency vs. Airspeed for Variable and Fixed Pitch Propellers")
h3 = plot([Vclimb / 1.68781, Vclimb / 1.68781], [0.6, 1], ':k');
text(Vclimb/1.68781, etapvar(Vseq == Vclimb)-0.05, ...
    strcat("$\eta_{p_{variable}} = ", num2str(etapvar(Vseq == Vclimb)), ...
    "$"), 'FontSize', 16)
ylim([0.6, 1])
legend([h1, h2], 'Location', 'best')

subplot(5, 1, 4)
plot(Vseq/1.68781, dT*100)
ylabel("\% Thrust Difference")
xlabel("Flight Speed (kn)")
title(["Percent Thrust Difference Between Variable", ...
    "Pitch Prop and Fixed Pitch Prop"])
hold on
plot([Vclimb / 1.68781, Vclimb / 1.68781], [0, 35], ':k')
text(Vclimb/1.68781, dT(Vseq == Vclimb)*100+3, strcat("$\Delta T = ", ...
    num2str(dT(Vseq == Vclimb) * 100), "$ \%"), 'FontSize', 16)
ylim([0, 35])
xlim([60, 180])

subplot(5, 1, 5)
yyaxis left
plot(Vseq/1.68781, deltabeta*180/pi)
ylabel("$\Delta \beta$ (deg) for Variable Pitch Prop")
hold on
plot([Vclimb / 1.68781, Vclimb / 1.68781], [-8, 0], ':k')
text(Vclimb/1.68781, deltabeta(Vseq == Vclimb)*180/pi-1, ...
    strcat("$\Delta \beta = ", num2str(deltabeta(Vseq == Vclimb) ...
    * 180 / pi), "^{\circ}$"), 'FontSize', 16)
ylim([-8, 0])

yyaxis right
plot(Vseq/1.68781, RPMfix)
ylabel("Engine RPM for Fixed Pitch Prop")
xlabel("Flight Speed (kn)")
hold on
plot([Vclimb / 1.68781, Vclimb / 1.68781], [1500, 2500], ':k')
text(Vclimb/1.68781, RPMfix(Vseq == Vclimb)+150, strcat("RPM $ = ", ...
    num2str(RPMfix(Vseq == Vclimb)), "$"), 'FontSize', 16)
ylim([1500, 2500])
title(["Engine RPM (Fixed Pitch Prop) and $\Delta \beta$", ...
    "(Variable Pitch Prop) vs. Airspeed"])

saveas(gcf, "./Figures/fix_var_comparison.jpg")

%% Fixed Pitch Analysis
nseq = linspace(1600, 2400, 51) / 60;

for ii = 1:length(nseq)
    [Jnfix(ii), Pdnfix(ii), CPnfix(ii), Tdnfix(ii), CTnfix(ii), ...
        etapdnfix(ii)] = propanalysis(Ropt, Vclimb, nseq(ii), B, m0fn, ...
        a0, Cdfn, copt, betopt);
end

Pengseq = Pengfn(nseq*60);

figure
yyaxis left
h1 = plot(nseq*60, Pdnfix/550, 'DisplayName', 'Propeller Power');
hold on
h2 = plot(nseq*60, Pengseq/550, 'DisplayName', 'Engine Power');
ylabel("Power (HP)")
text(1860, 120, strcat("RPM = ", num2str(RPMfix(Vseq == Vclimb)), ...
    ", Power = ", num2str(Pdfix(Vseq == Vclimb) / 550), ...
    " (HP), Thrust = ", num2str(Tdfix(Vseq == Vclimb)), " (lbf)"), ...
    'Fontsize', 16)
yyaxis right
h3 = plot(nseq*60, Tdnfix, 'DisplayName', 'Propeller Thrust');
ylabel("Thrust (lbf)")
xlabel("RPM")
title("Power and Thrust of Fixed Pitch Propeller vs. RPM", 'FontSize', 30)
h4 = plot([RPMfix(Vseq == Vclimb), RPMfix(Vseq == Vclimb)], [100, 1100], ':k');
ylim([100, 1100])
legend([h1, h2, h3])
saveas(gcf, "./Figures/fix_perform.jpg")

%% Variable Pitch Analysis

dbetseq = linspace(-8, 0, 51) * pi / 180;

for ii = 1:length(dbetseq)
    [Jbvar(ii), Pdbvar(ii), CPbvar(ii), Tdbvar(ii), CTbvar(ii), ...
        etapdbvar(ii)] = propanalysis(Ropt, Vclimb, n, B, m0fn, a0, ...
        Cdfn, copt, betopt+dbetseq(ii));

end

figure
yyaxis left
h1 = plot(dbetseq*180/pi, Pdbvar/550, 'DisplayName', 'Propeller Power');
hold on
h2 = plot(dbetseq*180/pi, 177*ones(size(dbetseq)), 'DisplayName', ...
    'Engine Power');
ylabel("Power (HP)")

text(-6, 160, strcat("$\Delta \beta$ = ", num2str(deltabeta(Vseq == ...
    Vclimb) * 180 / pi), "$^{\circ}$, Power = ", num2str(Pdvar(Vseq == ...
    Vclimb) / 550), " (HP), Thrust = ", num2str(Tdvar(Vseq == Vclimb)), ...
    " (lbf)"), 'Fontsize', 16)
yyaxis right
h3 = plot(dbetseq*180/pi, Tdbvar, 'DisplayName', 'Propeller Thrust');
ylabel("Thrust (lbf)")
xlabel("$\Delta \beta$ (deg)")
title("Power and Thrust of Variable Pitch Propeller vs. $\Delta \beta$", ...
    'FontSize', 30)
h4 = plot([deltabeta(Vseq == Vclimb), deltabeta(Vseq == Vclimb)]*180/pi, ...
    [100, 1100], ':k');
ylim([100, 1100])
legend([h1, h2, h3])
saveas(gcf, "./Figures/var_perform.jpg")

%% Propeller Design Function
function [r, c, bet, Pdesign, Tdesign, Qdesign, etap, the] = ...
    propdesign(R, Vinf, n, Peng, Cl, B, m0fn, a0, Cdfn)
global k Rgas T rho nn K

D = 2 * R; %ft
r = linspace(0, R, nn);
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
v0 = 0.5 * ones(1, nn);
Pdesign = 10e4;
iter = 1;
iterlim = 1e3;

while round(Pdesign, 10) ~= round(Peng, 10) && iter < iterlim
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
    Pdesign = CP * rho * n^3 * D^5;

    if Pdesign < Peng
        v0 = v0 * (1 + (Peng - Pdesign) / Peng);
    elseif Pdesign > Peng
        v0 = v0 * (1 + (Peng - Pdesign) / Peng);
    else
        break
    end
    iter = iter + 1;

end

Tdesign = CT * rho * n^2 * D^4;
Qdesign = CQ * rho * n^2 * D^5;

if dragdiverg
    return;
end

end

%% Propeller Analysis Function
function [J, Pdesign, CP, Tdesign, CT, etap] = propanalysis(R, Vinf, n, ...
    B, m0fn, a0, Cdfn, c, bet)
global k Rgas T rho nn K

D = 2 * R; %ft
r = linspace(0, R, nn);
x = r / R;

J = Vinf / (n * D);
ome = 2 * pi * n;

phi = atan(J./(pi * x));

VR = sqrt(Vinf^2+(ome * r).^2);
a = sqrt(k*Rgas*T);
M = VR / a;

m0 = m0fn(M);

sig = B * c / (pi * R);
the = zeros(size(r));

for ii = 2:length(r)
    aa = cos(phi(ii)) - sig(ii) * m0(ii) / (8 * x(ii)) * tan(phi(ii));
    bb = Vinf / VR(ii) + ((bet(ii) - phi(ii) - a0) * tan(phi(ii)) + 1) * ...
        sig(ii) * m0(ii) / (8 * x(ii));
    cc = -(bet(ii) - phi(ii) - a0) * sig(ii) * m0(ii) / (8 * x(ii));

    % quadratic formula (too slow):
    %             the(ii) = (-bb + sqrt(bb^2-4*aa*cc))/(2*aa);

    % use newton's method to solve the equation theii^2*a + theii*b + c ==
    % 0 for increased speed
    f = @(the) aa * the^2 + bb * the + cc;
    fprime = @(the) 2 * aa * the + bb;

    [the(ii), iter] = newton(f, fprime, 1e-2, 1e-10);

    clear aa bb cc f fprime
end

alp = bet - phi - the;
Cl = m0 .* (alp - a0);
Cd = Cdfn(Cl);

lamT = 1 ./ (cos(phi)).^2 .* (Cl .* cos(phi + the) - Cd .* sin(phi + the));
lamQ = 1 ./ (cos(phi)).^2 .* (Cl .* sin(phi + the) + Cd .* cos(phi + the));

dCTdx = sig * pi^3 .* x.^2 / 8 .* lamT;
dCQdx = sig * pi^3 .* x.^3 / 16 .* lamQ;

xx = x(x >= 0.15);

CT = trapz(xx, dCTdx(x >= 0.15));
CQ = trapz(xx, dCQdx(x >= 0.15));
CP = 2 * pi * CQ;

etap = CT / CP * J;
Pdesign = CP * rho * n^3 * D^5;

Tdesign = CT * rho * n^2 * D^4;
Qdesign = CQ * rho * n^2 * D^5;

end

%% 2D Propeller Plotting Utility
function [] = plotblades2D(r, R, c, B, line1)
c = c(r > 0.15*R);
line1 = line1(r > 0.15*R);
r = r(r > 0.15*R);

figure('Position', [100, 100, 800, 800])

for Blades = 1:B
    x = [r, flip(r)];
    y = [c / 2 + line1, flip(line1 - c / 2)];
    the = 2 * pi / B * Blades;


    xrot = x * cos(the) - y * sin(the);
    yrot = x * sin(the) + y * cos(the);

    fill(xrot, yrot, 'k')
    alpha(0.75)
    hold on
    axis equal
end

end

%% 3D Propeller Plotting Utility (single)
function [] = plotblade3D(r, R, c, bet, B, line1)

Rxfn = @(bet) [1, 0, 0; 0, cos(bet), sin(bet); 0, -sin(bet), cos(bet)];

bet = bet(r > 0.15*R);
c = c(r > 0.15*R);
line1 = line1(r > 0.15*R);
r = r(r > 0.15*R);

x = [r, flip(r)];
y = [c / 2 + line1, flip(line1 - c / 2)];
bb = [bet, flip(bet)];
z = zeros(size(x));

vec = [x; y; z];
rotvec = zeros(size(vec));

figure('Position', [100, 100, 800, 800])

for ii = 1:length(x)
    rotvec(:, ii) = Rxfn(bb(ii)) * vec(:, ii);
end

for Blades = 1:B
    the = 2 * pi / B * Blades;
    xrot = x * cos(the) - y * sin(the);
    yrot = x * sin(the) + y * cos(the);

    fill3(xrot, yrot, rotvec(3, :), 'k')
    alpha(0.75)
    hold on
    axis([-5, 5, -5, 5])
    xlabel("x")
    ylabel("y")
    zlabel("z")
    axis equal
end

end

%% Propeller Properties Plotting Utility
function [] = plotbladeprops(R, r, c, bet, Cl)

figure('Position', [100, 100, 1000, 1500])
sgtitle(strcat("Properties of Optimal Propeller Design, Diameter = ", ...
    num2str(2 * R), " (ft)"), 'FontSize', 30)

subplot(4, 1, 1)
plot(r/R, bet*180/pi)
xlabel("Radial Position Along Propeller Blade $x = \frac r R$ (ft)")
ylabel("Pitch Angle $\beta$ (deg)")
title(strcat("Blade Pitch Angle Distribution $\beta_{0.75R} = ", ...
    num2str(bet(uint64(length(r) * 0.75)) * 180 / pi), "^{\circ}$"), ...
    'fontsize', 24)
xlim([0.15, 1])

subplot(4, 1, 2)
plot(r/R, 0.04./(r / R).^1.2)
xlabel("Radial Position Along Propeller Blade $x = \frac r R$ (ft)")
ylabel("Tickness Ratio $\frac t c$ (Nondim)")
title("Blade Thickness Distribution", 'fontsize', 24)
xlim([0.15, 1])

subplot(4, 1, 3)
plot(r/R, c)
xlabel("Radial Position Along Propeller Blade $x = \frac r R$ (ft)")
ylabel("Chord $c$ (ft)")
title("Blade Chord Distribution", 'fontsize', 24)
xlim([0.15, 1])

subplot(4, 1, 4)
plot(r/R, Cl*ones(size(r)))
xlabel("Radial Position Along Propeller Blade $x = \frac r R$ (ft)")
ylabel("Lift Coefficient $C_l$")
title("Blade Lift Coefficient Distribution", 'fontsize', 24)
xlim([0.15, 1])

end

%% Propeller Analysis Plotting Utility
function [] = plotpropanalysis(Vseq, J, Pdesign, CP, Tdesign, CT, etap)

figure('Position', [100, 100, 1000, 1500])
sgtitle(["Analysis of Propeller Design with RPM = 2400", ...
    strcat("$V_{\infty}$ in Range $", num2str(min(Vseq) / ...
    1.68781), "$ to $", num2str(max(Vseq) / 1.68781), "$ (kn)")], ...
    'FontSize', 30)

subplot(5, 1, 1)
plot(J, Pdesign/550.000037)
xlabel("Advance Ratio")
ylabel("Propeller Power (HP)")
title("Propeller Power vs. Advance Ratio")

subplot(5, 1, 2)
plot(J, CP)
xlabel("Advance Ratio")
ylabel("Propeller Power Coefficient $C_P$")
title("Propeller Power Coefficient vs. Advance Ratio")

subplot(5, 1, 3)
plot(J, Tdesign)
xlabel("Advance Ratio")
ylabel("Propeller Thrust (lbf)")
title("Propeller Thrust vs. Advance Ratio")

subplot(5, 1, 4)
plot(J, CT)
xlabel("Advance Ratio")
ylabel("Propeller Thrust Coefficient $C_T$")
title("Propeller Thrust Coefficient vs. Advance Ratio")

subplot(5, 1, 5)
plot(J, etap)
xlabel("Advance Ratio")
ylabel("Propeller Efficiency $\eta_p$")
title("Propeller Efficiency vs. Advance Ratio")

end

%% formatlatex FUNCTION DEFINITION
function [] = formatlatex()

reset(groot)
set(groot, 'defaulttextinterpreter', 'latex')
set(groot, 'defaultcolorbarticklabelinterpreter', 'latex')
set(groot, 'defaultfigureposition', [100, 100, 1000, 600])
set(groot, 'defaultaxesticklabelinterpreter', 'latex')
set(groot, 'defaultlegendinterpreter', 'latex')
set(groot, 'defaultaxesfontsize', 18)
set(groot, 'defaultaxeslinewidth', 1)
set(groot, 'defaultscattermarker', 'x')
set(groot, 'defaultscatterlinewidth', 2)
set(groot, 'defaultlinemarkersize', 15)
set(groot, 'defaultlinelinewidth', 2.5)
set(groot, 'defaultAxesXgrid', 'on', 'defaultAxesYgrid', 'on', 'defaultAxesZgrid', 'on')
set(groot, 'defaultAxesGridLineStyle', '-.')
set(groot, 'defaultAxesXlim', [0, 2 * pi]);
set(groot, 'defaultAxesYlim', [-0.6, 0.6]);


% fprintf('.............................................................\n')
% fprintf('////////////////// FORMAT IS SET TO LATEX /////////////////// \n')
% fprintf('.............................................................\n')
end

%% newton FUNCTION DEFINITION
% Uses symbolic substitution to evaluate the zeros of a function
function [x_zero, iter] = newton(f, fprime, guess, tolerance)

xx(1:2) = [0, guess];

ii = 2;
iter = 1;

while abs(tolerance) < abs(xx(ii)-xx(ii - 1)) || iter == 1
    ffprime = fprime(xx(ii));

    ff = f(xx(ii));


    if ffprime == 0
        fprintf('Error, slope at point = 0. Choose a different initial condition')
        break
    end

    xx(ii+1) = xx(ii) - ff / ffprime;
    ii = ii + 1;
    iter = iter + 1;
end
x_zero = xx(end);

end