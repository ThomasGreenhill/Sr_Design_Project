% Provides figures for required power of VTOL aircraft
%
%   Inputs:
%       m: kg, Aircraft mass
%       gfactor: Loading factor (1 = hovering)
%       motDistr = Thrust distribution of motors (1x3)
%                   Enter [1,1,1] for same distr. with 3 motors
%       
%
%   Outputs: 
%       powerVec = Vector of power required by each motor (hp)
%
%   Calls:
%       propdesign function (provided by TGreenhill)
%       
%   Notes:
%       1. Not well tested yet
%
%   History:
%           2/9/2021, Created by X.Tang
%           2/9/2021, Debugged by X.Tang
%       
%

function [powerVec] = VTOLpowerreq(m, gfactor, motDistr)
    % Input check
    [r, c] = size(motDistr);
    if ((r ~= 1) && (c ~= 1))   % if not a line vector
       fprintf("\nEnter either row or column vector for motDistr\n");
       return
    end
    
    % Acceleration near earth surface
    g = 9.81; 
    
    % Thrust required to operate
    Treq = m*gfactor*g;
    
    %% Parameters left to change as further discussed with group
    Vinf = 87 * 0.514444;               % m/s
    n = 1854.4805 / 60;                 % Hz
    B = 3;
    Cl = 0.4;
    R = 82 / 2 * 0.0254;                % m
    a0 = 330.803;                       % m/s
    
    Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;
    m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ sqrt(1 - 0.9^2)) .* (Ma > 0.9);
    
    %% Each motor
    sumDistr = sum(motDistr);
    powerVec = zeros(1, length(motDistr));
    for i = 1:length(motDistr)
        curDistr = motDistr(i) / sumDistr;
        curT = curDistr * Treq;
        [~, ~, ~, curPower, ~, ~, ~,~] = ...
        propdesign(R, Vinf, n, curT, Cl, B, m0fn, a0, Cdfn);
        powerVec(i) = curPower * 0.00134102;        % Converts from W to hp
    end

end


