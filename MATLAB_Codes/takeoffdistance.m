%% takeoffdistance.m
% Provides calculations for takeoff distance
%
%   Inputs:
%           W: Weight of aircraft
%           Tavg: Average thrust
%           S: Wing reference area
%           RHO: Density of air
%           CL_max: Maximum lift coefficient
%           mu_r: Rolling friction coefficient -- typical:
%               0.02 for dry concrete to 0.3 for very soft ground
%           CD_0: Zero lift drag coefficient
%           bspan: Wing span
%           e: Span efficiency factor
%           
%
%   Outputs: 
%
%   Calls:
%       {none}
%       
%   Notes:
%       1. Stability derivatives should be dimensionalized!
%       2. 
%
%   History:
%       2/9/2021: Created file. TVG
%       2/13/2021: Created function. GN
%

function [SG] = takeoffdistance(W, Tavg, S, RHO, CL_max, mu_r, CD_0, bspan, e)

g = 9.81; % [m/s^2]
Gam = 1.4;
Rgas = 287; % [J/(kg*K)]
T = 288; % [K]
a = sqrt(Gam*Rgas*T);

AR = (bspan^2)/S;
K = 1/(pi*e*AR);

Vstall = sqrt(2*W/(RHO*S*CL_max));
VLOF = 1.1*Vstall; % Liftoff velocity
Vavg = VLOF/sqrt(2);
Mavg = Vavg/a;

CL_opt = mu_r/(2*K); % Optimal lift coefficient
CD_avg = CD_0+(K*(CL_opt)^2);

qavg = 0.5*RHO*(Vavg^2); % Average dynamic pressure

Davg = CD_avg*qavg*S; % Average drag
Lavg = CL_opt*qavg*S; % Average lift

aavg = (g/W)*(Tavg - Davg-(mu_r*(W-Lavg)); % Average acceleration

SG = (VLOF^2)/(2*aavg); % Ground-roll distance