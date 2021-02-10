%% VTOLpowerreq.m
% Provides figures for required power of VTOL aircraft in hover configuration
%   to hover.
%
%   Inputs:
%       m: Aircraft mass
%       
%           
%
%   Outputs: 
%       {}
%
%   Calls:
%       {none}
%       
%   Notes:
%       1.
%
%   History:
%       
%

function [] = VTOLpowerreq(m, gfactor, nummot )
    g = 9.81; 

    Freq = m*gfactor*g;

    Fprops = Freq/nummot; 


end


