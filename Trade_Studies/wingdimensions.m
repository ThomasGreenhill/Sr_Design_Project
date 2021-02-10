%% wingdimensions.m
%   Computes the required chord and planform area for a wing based on a set
%   of requirements
%   
%   Inputs:
%       Cla: Airfoil lift curve slope (deg) -- typical value 0.11
%       W: Aircraft weight
%       Clmax: Airfoil max lift coefficient
%       bspan: Wing span
%       rho: Air density
%       V: Freestream velocity
%       e: Wing span efficiency 
%   
%   Outputs:
%       {none}
%
%   Notes:
%
%
%   History:
%       02.09.2021: Created and debugged, TVG
%

function [c, S] = wingdimensions(Cla, W, Clmax, bspan, rho, V, e)
q = 0.5*rho*V^2;

c = 1;
S = bspan*c;
cor = 1;
iterlim = 1e3;
tol = 1e-6;
iter = 1;

liftcoeff = @(Cla, e, AR, a) a*Cla/(1+57.3*Cla/(pi*e*AR));

while iter < iterlim && cor >= tol 
    a = 17;
    
    Sold = S;
    
    AR = bspan/c;    
    
    CLrequired = W/(S*q);
    
    while a*Cla < Clmax
        CLdesign = liftcoeff(Cla, e, AR, a);
        a = a+0.1;
    end
    
    if CLdesign < CLrequired
        c = c*(1-(CLdesign-CLrequired)/(CLrequired+CLdesign));
    elseif CLdesign > CLrequired
        c = c*(1-(CLdesign-CLrequired)/(CLrequired+CLdesign));
    else
        break 
    end
    S = c*bspan;
    
    cor = abs(S-Sold);
    iter = iter + 1;
    
end

end
