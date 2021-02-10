%% CruiseReq3D.m
% Provides calculations and figures for cruise function
%
%   Inputs:
%       Constants:
%       fsVec: [v_inf (m/s), rho_inf (kg/m^3)]
%       wingVec: [Wing Area (m^2), Wing Span (m), Oswald's Eff. Ratio, CD_parasitic (of wing)]
%       planeVec: [Total Weight (N), Other component's Cd (Based on wing area)]
%           
%
%   Outputs: 
%       Dt: total drag of the 
%       Pt: total power required for cruise
%
%   Calls:
%       {none}
%       
%   Notes:
%       1. Will be improved to accomodate arbitrary wing geometries rather than just using e
%
%   History:
%       2/9/2021: Created. X.T.
%

function [Dt, Pt] = CruiseReq3D(fsVec, wingVec, planeVec)
% Obtaining parameters
V = fsVec(1); rho = fsVec(2);
S = wingVec(1); b = wingVec(2); e = wingVec(3); CD_o = wingVec(4);
W = planeVec(1); CD_other = planeVec(2);

% Main
CL_req = (2*W) / (rho*V*S);
AR = b.^2 / S;
CD_i = CL_req.^2 / (pi*e*AR);
CD_t = CD_i + CD_o + CD_other;
Dt = CD_t * 0.5 * rho * V.^2 * S;   % Total drag
Pt = Dt * V;                        % Total power required

end
