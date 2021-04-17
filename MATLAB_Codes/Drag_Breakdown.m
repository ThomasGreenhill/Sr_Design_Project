%% EAE 130A Project # 1
% TVG 01.11.2021
clc; clear; close all;

formatlatex()
warning('off','all')
mkdir './Figures'
warning('on','all')
format long
%% Atmospheric Properties and Global Variables
rho = 1.02393;
mu = 0.0000175212;
k = 1.4;
P = 81199.6;
T = 276.263;
R = 278.14;
tc = 0.12;

a = sqrt(k*R*T);R
Ucruise = 62;
Ma = Ucruise/a;

W = 13000; %N
%% General Dimensions
% Wing dimensions
bspan_total = 6.325*2; %m
bspan_nofuse = bspan_total - 1.3; %m
c_root = 1.4050; 
c_tip = 1.124; 
lfuse = 9; %m
dfuse = 1.4; %m
Sref = 16;


% Horizontal stab dimensions
Sht = 2.8; %m^2

% Vertical stab dimensions
Svt= 1.8; %m^2

% Front pylon dimension
Sfp = 0.85;

%% Wetted Area Calculations
% Wing
xx = linspace(1,0,1001);
x_airfoil = [xx, xx(end-1:-1:1)];
y_airfoil = camNACA(0.02, 0.4, 0.12, x_airfoil);
dx = abs(x_airfoil(2)-x_airfoil(1));
cl = curvelength(x_airfoil,y_airfoil);
Swet_wing = cl*(c_root+c_tip)*(bspan_total/2);
% Se_wing = 2*(c_root*(y_break-4.05/2) + 1/2*(c_root+c_tip)*(bspan_total/2-y_break));
MGCw = 1.265;

clear xx dx cl y_airfoil

% Fuselage
Swet_fuse = 22.14; %m^2
clear S_sides S_top S_front

% NACA 0012
y_airfoil = symNACA(0.12, x_airfoil);
cl = curvelength(x_airfoil,y_airfoil);

% Horizontal tail
S_ht = 3.01;
% Swet_ht = cl*S_ht;
Swet_ht = 5.84; 
bht = 3.68;
MGCht = S_ht/(bht);
ARht = bht^2/S_ht;

% Vertical tail
bvt = 2.048;
S_vt = 1.85;
% Swet_vt = cl*S_vt;
Swet_vt = 3.61;
MGCvt = S_vt/(bvt);

clear cl y_airfoil

% Nose Wheel Extended and Retracted
ext.Snw = 0.95 * 0.0929; %m^2
ret.Snw = 0.6*2 * 0.0929; %m^2

% Main Wheels Extended and Retracted
ext.Smw = 3.2*1.75/12*2 * 0.0929; %m^2, assumes a diameter of 1.75" and a length of 3.2'
ret.Smw = 3.3*2/12 * 0.0929; %m^2, assumes a hole 2" wide and a length 3.3'

%% Drag Coefficient Functions
Re = @(rho,v,l,mu) rho*v*l/mu;
Cf = @(Ma,Re) 0.455/(log10(Re)^2.58*(1+0.144*Ma^2)^0.58);
CD0ww = @(Rwf,RLS,Cf,Lp,tc,Swet,Sref) Rwf*RLS*Cf*(1+Lp*tc+100*tc^4)*Swet/Sref;
CD0ff = @(Rwf,Cff,lf,df,Swet,Sref) Rwf*Cff*(1+60/(lf/df)^3+0.0025*lf/df)*Swet/Sref;
CDi = @(CL,e,AR) CL^2/(pi*e*AR);

%% Wing Zero-Lift Drag Coefficient
% Misc.
Rwf = 1.02;
RLS = 1.08;
Lp = 1.2;

% Fuselage Reynold's Number
Ref = Re(rho,Ucruise,lfuse,mu);

% Wing Reynold's Number
Rew = Re(rho,Ucruise,MGCw,mu);

% Wing Friction
Cfw = Cf(Ma,Rew);

% Wing CD0
CD0w = CD0ww(Rwf,RLS,Cfw,Lp,0.14,Swet_wing,Sref);

% Total
CDw = CD0w;
fw = CDw*Sref;

%% Fuselage Zero-Lift Drag Coefficient
% Fuselage Friction
Cff = Cf(Ma,Ref);

% Zero-Lift Drag
CD0f = CD0ff(Rwf,Cff,lfuse,dfuse,Swet_fuse,Sref);

% Total, Multiplied by 150% for windshield drag
CDf = CD0f*1.5;
ff = 0.6*CDf*Sref;

%% Front pylon
MGCfp = 0.33;
Refp = Re(rho, Ucruise, 0.33, mu);

Rfp = 1.02;
RLSfp = 1.05;

% Front pylon friction
Cffp = Cf(Ma, Refp);

% Front Pylon Zero-Lift Drag
CD0fp = CD0ww(Rfp,RLSfp,Cffp,Lp,tc,Swet_vt*Sfp/Svt,Sfp);

ffp = CD0fp*Sfp;

%% Vertical Tail Zero-Lift Drag Coefficient
% Vertical Tail Reynold's Number
Revt = Re(rho,Ucruise,MGCvt,mu);

% Misc.
RLSvt = 1.05;
Lamtc = 9.4;

% Vertical Tail Friction
Cfvt = Cf(Ma,Revt);

% Vertical Tail Zero-Lift Drag
CD0vt = CD0ww(Rwf,RLSvt,Cfvt,Lp,tc,Swet_vt,S_vt);

% Total
CDvt = CD0vt;
fvt = CDvt*Svt;

%% Horizontal Tail Drag Coefficient
% Horizontal Tail Reynold's Number
Reht = Re(rho,Ucruise,MGCht,mu);

% Misc.
RLSht = 1.07;
Lamtc = 8.2;

% Horizontal Tail Friction
Cfht = Cf(Ma,Reht);

% Horizontal Tail Zero Lift Drag
CD0ht = CD0ww(Rwf,RLSht,Cfht,Lp,tc,Swet_ht,S_ht);

% Total
CDht = CD0ht;
fht = CDht*Sht;

%% Nose Wheel Extended Drag Coefficient
ext.CDnw = 0.64; %Torenbeek Fig F-19
ext.fnw = ext.CDnw*ext.Snw;

ret.CDnw = 0.0009; %Roskam Figure 5.33a (Full Length Fairing, Not Sealed)
ret.fnw = ret.CDnw*ret.Snw;

%% Main Wheels Extended & Retracted Drag Coefficient
ext.CDmw = 0.31; %Torenbeek Fig F-19
ext.fmw = ext.CDmw*ext.Smw;

ret.CDmw = 0.0012; %Roskam Figure 5.33a (Short Length Fairing)
ret.fmw = ret.CDmw*ext.Smw;

%% Subtotal
ext.fsubtot = ffp + fw + ff + fvt + fht + ext.fnw + ext.fmw;
ret.fsubtot = ffp + fw + ff + fvt + fht + ret.fnw + ret.fmw;

%% Interference Drag
% Ten percent of subtotal
ext.fint = 0.1*ext.fsubtot;
ret.fint = 0.1*ret.fsubtot;

%% Cooling Drag
% Ten percent of total
ext.fcool = coolingdrag(ext.fsubtot+ext.fint);
ret.fcool = coolingdrag(ret.fsubtot+ret.fint);

%% CDmin for Wheels Extended and Retracted
ext.ftot = ext.fsubtot+ext.fint+ext.fcool;
ret.ftot = ret.fsubtot+ret.fint+ret.fcool;

ext.CDmin = ext.ftot/Sref;
ret.CDmin = ret.ftot/Sref;


%% Parabolic Drag Polar
close all
Drag_Polar = @(CD_min, CL_min, AR, e, CL)  CD_min + (CL-CL_min).^2/(pi*AR*e);

CL = 0:0.002:1.6;

% Assume e = 0.84 (Roskam pg 193)
e = 0.84;

ext.Drag_Polar = Drag_Polar(ext.CDmin,0,7.45,e,CL);
ret.Drag_Polar = Drag_Polar(ret.CDmin,0,7.45,e,CL);

figure(1)
title(["Jiffy Jerboa Drag Polars, Landing Gear Extended and Retracted","Assuming Wing Oswald Efficiency $e = 0.84$"])
hold on


plot(CL,ext.Drag_Polar,'DisplayName',"Landing Gear Extended")
ylabel("Drag Coefficient $C_D$")
xlabel("Lift Coefficient $C_L$")

plot(CL,ret.Drag_Polar,'DisplayName',"Landing Gear Retracted")
ylabel("Drag Coefficient $C_D$")
xlabel("Lift Coefficient $C_L$")
legend

text(CL(1)+0.05,ext.Drag_Polar(1)*1.3,strcat("$C_{D_{0_{ext}}} =",num2str(ext.Drag_Polar(1),4),"$"),'fontsize',18)
text(CL(1)+0.05,ret.Drag_Polar(1)*0.8,strcat("$C_{D_{0_{ret}}} =",num2str(ret.Drag_Polar(1),4),"$"),'fontsize',18)

ylim([0.01,0.21])

saveas(gcf,"./Figures/Drag_Polars.jpg")

%% Required power
Power_Required = @(CD0,rho,V,W,bspan_total,Sref,e) CD0*0.5*rho*V.^3*Sref + (W/bspan_total)^2*1./(0.5*rho*V*pi*e);

eta_prop = 0.85;

Pav = eta_prop*384000;

V = 25:0.05:70;

ext.Preq = Power_Required(ext.CDmin,rho,V,W,bspan_total,Sref,e); %W
ret.Preq = Power_Required(ret.CDmin,rho,V,W,bspan_total,Sref,e); %W

figure(2)
title(["Power Available and Power Required for Jiffy Jerboa with", "Landing Gear Extended and Retracted"])
hold on

plot(V,ext.Preq,'DisplayName',"Required, Landing Gear Extended")
plot(V,ret.Preq,'DisplayName',"Required, Landing Gear Retracted")

plot([20,70],Pav*ones(2,1),'--k','DisplayName',"Available")

xlabel("Airspeed (ft/s)")
ylabel("Power (W)")
legend

% axis([0,380,0,400])

% text(V(find(round(ext.Preq,0)==round(Pav,0)))-100,Pav+10,strcat("$V_{max_{ext}} =",num2str(V(find(round(ext.Preq,1)==round(Pav,1)))),"$ ft/s"),'FontSize',18)
% text(V(find(round(ret.Preq,1)==round(Pav,1)))+10,Pav+10,strcat("$V_{max_{ret}} =",num2str(V(find(round(ret.Preq,1)==round(Pav,1)))),"$ ft/s"),'FontSize',18)

% Find the max excess power
[ext.Pmin,ext.PminInd] = min(ext.Preq);
[ret.Pmin,ret.PminInd] = min(ret.Preq);

% Find the max climb rate
text(50,140,strcat("$RC_{max_{ext}}=",num2str((Pav-ext.Preq(ext.PminInd))/(0.00181818182*W)),"$ ft/s"),'FontSize',18)
text(50,100,strcat("$RC_{max_{ret}}=",num2str((Pav-ret.Preq(ret.PminInd))/(0.00181818182*W)),"$ ft/s"),'FontSize',18)

saveas(gcf,"./Figures/Power_Curves.jpg")
%% FUNCTIONS %%
%% NACA Cambered Airfoil Equation
function y = camNACA(m,p,t,xx)
% Equation for cambered NACA airfoil with unit chord length
ii = 1;
y = zeros(size(ii));
for x = xx
    if ii ~= length(xx)
        if xx(ii+1) > xx(ii)
            if x >= 0 && x <= p
                y(ii) = m/p^2*(2*p*x-x^2)+(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
            elseif x >= p && x <= 1
                y(ii) = m/(1-p)^2*((1-2*p)+2*p*x-x^2)+(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
            else
                fprintf("x out of bounds")
            end
        else
            if x >= 0 && x <= p
                y(ii) = m/p^2*(2*p*x-x^2)-(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
            elseif x >= p && x <= 1
                y(ii) = m/(1-p)^2*((1-2*p)+2*p*x-x^2)-(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
            else
                fprintf("x out of bounds")
            end
        end
    else
        if x >= 0 && x <= p
            y(ii) = m/p^2*(2*p*x-x^2)+(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
        elseif x >= p && x <= 1
            y(ii) = m/(1-p)^2*((1-2*p)+2*p*x-x^2)-(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
        end
    end
    ii = ii+1;
end
end
%% NACA Uncambered Airfoil Equation
function y = symNACA(t,xx)
% Equation for symmetrical NACA airfoil with unit chord length
ii = 1;
y = zeros(size(ii));
for x = xx
    if ii ~= length(xx)
        if xx(ii+1) > xx(ii)
            y(ii) = 5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4);
        else
            y(ii) = -(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
        end
    else
        if y(ii-1) > 0
            y(ii) = (5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
        elseif y(ii-1) < 0
            y(ii) = -(5*t*(0.2969*sqrt(x)-0.126*x-0.3516*x^2+0.2843*x^3-0.1015*x^4));
        end
    end
    ii = ii+1;
end
end
%% Curve Length Calculator
function l = curvelength(x,y)
l = 0;
for ii = 1:length(x)-1
    l = l+sqrt((x(ii)-x(ii+1))^2 + (y(ii)-y(ii+1))^2);
end
end
%% Fixed Point Iteration
function f_cool = coolingdrag(subtotal)
tol = 1e-12;
f_cool = 0;
iterlim = 1e3;

cor = 2;
iter = 1;
total = subtotal;

while cor>tol && iter<iterlim
    old = f_cool;
    
    total = subtotal + total*0.1;
    
    f_cool = 0.1*total;
    
    cor = abs(old-f_cool);
    iter = iter+1;
end

end
%% formatlatex FUNCTION DEFINITION
function [] = formatlatex()

reset(groot)
set(groot,'defaulttextinterpreter','latex')
set(groot,'defaultcolorbarticklabelinterpreter','latex')
set(groot,'defaultfigureposition',[100 100 800 600])
set(groot,'defaultaxesticklabelinterpreter','latex')
set(groot,'defaultlegendinterpreter','latex')
set(groot,'defaultaxesfontsize',18)
set(groot,'defaultaxeslinewidth',1)
set(groot,'defaultscattermarker','x')
set(groot,'defaultscatterlinewidth',2)
set(groot,'defaultlinemarkersize',15)
set(groot,'defaultlinelinewidth',2.5)
set(groot,'defaultAxesXgrid','on','defaultAxesYgrid','on','defaultAxesZgrid','on')
set(groot,'defaultAxesGridLineStyle','-.')
set(groot,'defaultAxesXlim',[0 2*pi]);
set(groot,'defaultAxesYlim',[-0.6 0.6]);


% fprintf('.............................................................\n')
% fprintf('////////////////// FORMAT IS SET TO LATEX /////////////////// \n')
% fprintf('.............................................................\n')
end
