%% Constant 
% Young's Modulus
E=71000; % From Table 14.1
% Coefficients for Ramberg-Osgood flow curve
H=977;
n=0.106;
% Coefficients for life
sf=1466; % From Table 14.1
ef=0.262; % From Table 14.1
b=-0.143; % From Table 14.1
c=-0.619; % From Table 14.1
% Stress Concentration
kt=4;
%% Normal Stress History
S=[0 336 48.3 336 48.3 292 48.3 255 48.3 219 48.3 181 48.3 143 48.3 105 48.3 67.6 ...
    48.3 67.6 -19.3 48.3 -67.6 48.3 -67.6 336];
[ii,jj]=size(S);
SigOr=[0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 2 21 2 23 24 25];
%% Define data storage arrays
syms s
sigPk=zeros(ii,jj); % stress corresponding to each turning point
epsPk=zeros(ii,jj);  % strain corresponding to each turning point
%% Handle first cycle
delS = S(ii,2)-S(ii,1);
signS = delS/abs(delS);
delS = abs(delS);
% Find delsig from delS using non-linear root finding
eqn1L=kt*delS;
eqn1R=sqrt(s.^2+s*E*(s/H).^(1/n));
eqn1 = eqn1L==eqn1R;
delsig=double(vpasolve(eqn1,s,[0 inf])); 
deleps=(delsig/E)+(delsig/H)^(1/n);
sigPk(2) = sigPk(1) + signS*delsig;
epsPk(2) = epsPk(1) + signS*deleps;
%% Loop over subsequent turning points
for i=3:jj
% Get origin point
if SigOr(i) == 0
iOrigin = i - 1;
else
iOrigin = SigOr(i);
end
delS = S(i)-S(iOrigin);
signS = delS/abs(delS);
delS = abs(delS);
% Find delsig from delS using non-linear root finding
eqn2L=kt*(1/2*delS);
eqn2R=sqrt((s/2).^2+(s/2)*E*((s/2)/H).^(1/n));
eqn2 = eqn2L==eqn2R;
delsig=double(vpasolve(eqn2,s,[0 inf])); 
deleps=2*((delsig/(2*E))+(delsig/(2*H)).^(1/n));
sigPk(i) = sigPk(iOrigin) + signS*delsig;
epsPk(i) = epsPk(iOrigin) + signS*deleps;
end
%% Make the stress-strain curve
Npts = 50;
figure (1)
% Plot initial loading
% Define array of points from 0 to first peak
stress=linspace(sigPk(1),sigPk(2),Npts);
% Compute strain from stress
strain = stress/E + (stress/H).^(1/n);
plot(strain,stress,'--','color','k')
hold on
plot(epsPk(2),sigPk(2),'x','color','k') 
hold on 
for i=3:jj
% Get origin point
if SigOr(i) == 0
iOrigin = i - 1;
else
iOrigin = SigOr(i);
end
% Compute range of stress
delsig = sigPk(i)-sigPk(iOrigin);
signS = delsig/abs(delsig);
delsig = abs(delsig);
% Define array of points from 0 to delsig
stress=linspace(0,delsig,Npts);
% Compute strain from stress with factor of 2 expansion
strain = stress/E + 2*(stress/2/H).^(1/n);
% Adjust vectors to account for origin and direction
strain = epsPk(iOrigin) + signS*strain;
stress = sigPk(iOrigin) + signS*stress;
plot(strain,stress,'color','k')
hold on
plot(epsPk(i),sigPk(i),'x','color','k') 
hold on 
end
grid on
xlabel('Strain')
ylabel('Stress (MPa)')
title('Stress-strain Curve')
%% Prepare Life Estimation
SMAX=zeros(11,1);
EMAX=zeros(11,1);
EMIN=zeros(11,1);
for kk=1:11
SMAX(kk,1)=sigPk(1,2*kk);
if kk==1  
EMAX(kk,1)=max(epsPk);
EMIN(kk,1)=min(epsPk(epsPk ~= 0));
else
EMAX(kk,1)=epsPk(2*kk);
EMIN(kk,1)=epsPk(2*kk+1);    
end
end
EA=(EMAX-EMIN)/2;
%% Life
syms N
Nnj=0; 
Ni=[1 11 35 88 180 300 510 780 1030 15 1];
LEQNr=(sf)^2/E*(2*N).^(2*b)+ef*sf*(2*N)^(b+c); % RHS of SWT
for kk=1:11
LEQNl=SMAX(kk,1)*EA(kk,1); % LHS of SWT 
if LEQNl>0
eqn5 = LEQNl==LEQNr;
Nfi=double(vpasolve(eqn5,N,[0 inf]));
else % the SWT equation cannot predict the Life when the product of maximum
     % stress and strain amplitude is negative so that these conditions
     % should be removed from calculation
Nfi=inf; % Let Nf=inf to make no addition in K.
end
Nnj=Nnj+Ni(kk)/Nfi;
end
Bf=1/Nnj; % The number of repetitions to cause fatigue cracking.
clear eqn5 LEQNl LEQNr