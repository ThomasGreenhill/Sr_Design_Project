%% Calculates the aerodynamic center of an aircraft according to eqn 5.51 in
%   Yechout
%
%   Inputs:
%       S: Wing planform area (reference area) (UNITS OF LENGTH^2)
%       S_h: Planform area of horizontal tail (UNITS OF LENGTH^2)
%       xbar_AC_wf: Wing and fuselage aerodynamic center location w.r.t.
%           wing root LE, normalized by MAC. Typically ~0.25 (NONDIM) 
%       x_AC_h: Horizontal tail aerodynamic center location w.r.t wing root
%           LE (UNITS OF LENGTH)
%       cbar: Wing MAC (UNITS OF LENGTH)
%       CLa_wf: Lift curve slope of wing and fuse (UNITS of DEG^-1)
%       CLa_h: Lift curve slope of horizontal tail (UNITS of DEG^-1)
%       depsda: Derivative of downwash angle w.r.t. alpha (typical 0.1)
%       eta_h: Horizontal tail dynamic pressure ratio (qbar_h/qbar)
%
%   Outputs: 
%       xbar_AC: Location of MAC-normalized aicraft aero. center w.r.t.
%           wing root LE
%
%   Calls:
%       {None}
%       
%   Notes:
%       Test using:
%           xbar_AC = x_AC_fn(506, 120, 0.25, 26.25, 8.8, 0.082, 0.0631, 0.1, 0.9)
%       Result should be 0.602 (example 5.1 in Yechout)
%
%   History:
%       03.15.2021: Created and debugged, TVG
%       

%%
function [xbar_AC] = x_AC_fn(S, S_h, xbar_AC_wf, x_AC_h, cbar, CLa_wf, CLa_h, depsda, eta_h)

xbar_AC_h = x_AC_h/cbar;

xbar_AC = (xbar_AC_wf + CLa_h/CLa_wf*eta_h*S_h/S*xbar_AC_h*(1-depsda))/(1+CLa_h/CLa_wf*eta_h*S_h/S*(1-depsda));

end

