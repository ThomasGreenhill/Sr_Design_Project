% Provides calculations and figures for cruise function
%
%   Inputs:
%       Constants:
%       v_inf: free stream velocity (m/s)
%       rho_inf: air density (kg/m^3)
%       S: wing area (m^2)
%       CD_wing: wing total drag coeff.
%       CD_other: other component total drag coeff. based on wing area
%       motDistr: motor power/thrust distribution, ex [1,1,1]
%       log_switch: true if motDistr is for power
%                   false if motDistr is for thrust
%
%       R, n, Cl_prop, B, m0fn, a0, Cdfn: See propdesign parameters
%           
%
%   Outputs: 
%       Dt: total drag of the 
%       Tm: distributed thrust of motor
%       Pm: distributed power of motor (hp)
%
%   Calls:
%       propdesign (By TGreenhill)
%       
%   Notes:
%       1. Will be improved to accomodate arbitrary wing geometries rather than just using e
%
%   History:
%       2/9/2021: Created by X.Tand
%

function [Dt, Tm, Pm] = cruisepowerreq(v_inf, rho_inf, S, CD_wing, CD_other, motDistr, log_switch, ...
    R, n, Cl_prop, B, m0fn, a0, Cdfn)

    % Input check
    [r, c] = size(motDistr);
    if ((r ~= 1) && (c ~= 1))   % if not a line vector
       fprintf("\nEnter either row or column vector for motDistr\n");
       return
    end

    CD_total = CD_wing + CD_other;
    Dt= CD_total * 0.5 * v_inf.^2 * rho_inf * S;
    
    % Each motor
    sumDistr = sum(motDistr);
    if log_switch == true   % distributed T
        Pm = zeros(1, length(motDistr));
        for i = 1:length(motDistr)
            curDistr = motDistr(i) / sumDistr;
            curT = curDistr * Dt;
            [~, ~, ~, curPower, ~, ~, ~,~] = ...
            propdesign(R, v_inf, n, curT, Cl_prop, B, m0fn, a0, Cdfn);
            Pm(i) = curPower * 0.00134102;        % Converts from W to hp
        end
        
    else        % distributed Power (use iteration)
        %% FIXME: complete the distributed power part
        
        
        
    end






end
