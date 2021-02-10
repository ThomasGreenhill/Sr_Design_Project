%% VTOLpowerreq.m
% Provides figures for required power of VTOL aircraft
%
%   Inputs:
%       m: Aircraft mass
%       gfactor: Loading factor (1 = hovering)
%       numMotor = Number of motors
%       
%
%   Outputs: 
%       Tm = Thrust required by each motor (equally distributed)
%
%   Calls:
%       {none}
%       
%   Notes:
%       1.
%
%   History:
%           2/9/2021, X.Tang
%       
%

function [Tm] = VTOLpowerreq(m, gfactor, numMotor)
    g = 9.81; 

    Freq = m*gfactor*g;

    Fprops = Freq/numMotor; 


end


