%% STOLpowerreq.m
% Provides figures for required power of STOL aircraft 
%
%   Inputs:
%       m: kg, airplane mass
%       dist_TO: m, target rakeoff distance
%       S: m^2, wing area
%       CL_max_TO: max CL during takeoff
%       sigma: air density ratio (compared to standard sea level atm.)
%       motDistr: 1xn vector of motor power distribution
%           
%
%   Outputs: 
%       outVec: if FAR 23, 1xn vector of motor power (hp)
%               if FAR 25, 1xn vector of motor thrust (N)
%
%   Calls:
%       {none}
%       
%   Notes:
%       1. Function uses empirical expression provided in Roskam Part I
%       2. FAR 23/25 based on aircraft mass included
%       3. When integrating functions, mute the FAR23/25 fprintf sections
%       4. Not well tested yet
%
%   History:
%           2/9/2021, Created by X.Tang
%           2/9/2021, Debugged by X.Tang
%       
%

function [outVec] = STOLpowerreq(m, dist_TO, S, CL_max_TO, sigma, motDistr)
    g = 9.81; % m/s^2
    % Input check
    [r, c] = size(motDistr);
    if ((r ~= 1) && (c ~= 1))   % if not a line vector
       fprintf("\nEnter either row or column vector for motDistr\n");
       return
    end
    
    % FAR 23/25 check
    dist_TO_Brit = dist_TO * 3.28084;   % meter to feet
    W = m*g; % N
    W_Brit = W * 0.224809;  % N to lbf
    S_Brit = S * 3.28084.^2;    % m^2 to ft^2
    bdy = 12500 * 0.453592;     % kg
    tol = 1e-3;         % tolerance for compare between double
    if (m <= bdy)   % FAR 23
        a1 = 8.134; a2 = 0.0149;
        TOP23 = zeros(1,2);
        delta = a2.^2 - 4*a1 * (-dist_TO_Brit);
        
        % Check real
        if (delta > 0)
            TOP23(1) = (-a2 + sqrt(delta)) / (2*a1);
            TOP23(2) = (-a2 - sqrt(delta)) / (2*a1);
            
            % Check positive num
            if ((TOP23(1) > 0) && (TOP23(2) <= 0))
                TOP23Val = TOP23(1);
            elseif ((TOP23(1) <= 0) && (TOP23(2) > 0))
                TOP23Val = TOP23(2);
            elseif ((TOP23(1) > 0) && (TOP23(2) > 0))
                fprintf("\nError: TOP23 has two positive roots\n");
                return
            else
                fprintf("\nError: TOp23 has two negative roots\n");
                return
            end 
        elseif (abs(delta) <= tol)
            TOP23Val = mean(TOP23);
            
            if (TOP23Val <= 0)
                fprintf("\nError: TOP23 has one negative root\n");
            end
        else        % imaginary
            fprintf("\nError: No real root for TOP23\n");
            return
        end
        
        % Calculation for power in hp
        PTO = (W_Brit.^2 / S_Brit) / (TOP23Val * sigma * CL_max_TO);
        
        % Power distribution
        sumDistr = sum(motDistr);
        outVec = zeros(1, length(motDistr));
        for i = 1:length(motDistr)
            curDistr = motDistr(i) / sumDistr;
            outVec(i) = curDistr * PTO;      
        end

        %% Can mute when integrated
        fprintf("\nAircraft category: FAR 23, motor POWER vector output\n");
        %%
    else            % FAR 25
        a3 = 37.5;
        TOP25 = S_Brit / a3;
        TTO_lbf = (W_Brit.^2 / S_Brit) / (TOP25 * sigma * CL_max_TO);
        TTO = TTO_lbf * 4.44822;    % from lbf to N
        
        % Thrust distribution
        sumDistr = sum(motDistr);
        outVec = zeros(1, length(motDistr));
        for i = 1:length(motDistr)
            curDistr = motDistr(i) / sumDistr;
            outVec(i) = curDistr * TTO;      
        end

        
        %% Can mute when integrated
        fprintf("\nAircraft category: FAR 25, motor THRUST vector output\n");
        %%
    end


    
    
end
