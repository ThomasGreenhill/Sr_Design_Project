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
Smin=[-67.6 48.3 48.3 48.3 48.3 48.3 48.3 48.3 48.3 -19.3 -67.6];
Smax=[336 336 292 255 219 181 143 105 67.6 48.3 48.3];
LN=[0 1 1 1 1 1 1 1 1 1 1 1];
DR=[0 1 1 1 1 1 1 1 1 1 1 1]; % L: +1, U: -1
[u,v]=size(Smax);
%% Set up the data points for hysteresis loop
M=10^2; % The number of data points needed for each branch
syms s
epsilon_data= NaN(v,1+2*M);
sigma_data= NaN(v,1+2*M);
for kk=1:v
% Maximum stress and strain
eqn1L=kt*Smax(u,kk);
eqn1R=sqrt(s.^2+s*E*(s/H).^(1/n));
eqn1 = eqn1L==eqn1R;
sigma_data(kk,1)=double(vpasolve(eqn1,s,[0 inf])); 
epsilon_data(kk,1)=(sigma_data(kk,1)/E)+(sigma_data(kk,1)/H)^(1/n);
% The hysteresis loop
eqn2L=kt*(1/2*(Smax(u,kk)-Smin(u,kk)));
eqn2R=sqrt(s.^2+s*E*(s/H).^(1/n));
eqn2 = eqn2L==eqn2R;
sigma_a=double(vpasolve(eqn2,s,[0 inf])); 
delta_sigma=linspace(0,2*sigma_a,M);
delta_epsilon=2*((delta_sigma/(2*E))+(delta_sigma/(2*H)).^(1/n));
sigma_data(kk,2:M+1)=sigma_data(kk,1)-delta_sigma;
epsilon_data(kk,2:M+1)=epsilon_data(kk,1)-delta_epsilon;
sigma_data(kk,M+2:2*M+1)=sigma_data(kk,M+1)+delta_sigma;
epsilon_data(kk,M+2:2*M+1)=epsilon_data(kk,M+1)+delta_epsilon;
end
%% Adjust the location of the loops
for kk=1:v
if kk~=1
if DR(kk)==1
eqn3L=kt*(1/2*(Smax(u,LN(kk))-Smin(u,kk)));
eqn3R=sqrt(s.^2+s*E*(s/H).^(1/n));
eqn3 = eqn3L==eqn3R;
sigma_ar=double(vpasolve(eqn3,s,[0 inf])); 
epsilon_ar=((sigma_ar/E)+(sigma_ar/H)^(1/n));
sigma_min=max(sigma_data(LN(kk),:))-2*sigma_ar;
epsilon_min=max(epsilon_data(LN(kk),:))-2*epsilon_ar;
pyx=epsilon_min-min(epsilon_data(kk,:));
pyy=sigma_min-min(sigma_data(kk,:));
epsilon_data(kk,:)=epsilon_data(kk,:)+pyx;
sigma_data(kk,:)=sigma_data(kk,:)+pyy;    
clear sigma_min epsilon_min epsilon_ar epsilon_ar pyx pyy
elseif DR(kk)==-1
eqn3L=kt*(1/2*(Smax(u,kk)-Smin(u,LN(kk))));
eqn3R=sqrt(s.^2+s*E*(s/H).^(1/n));
eqn3 = eqn3L==eqn3R;
sigma_ar=double(vpasolve(eqn3,s,[0 inf])); 
epsilon_ar=((sigma_ar/E)+(sigma_ar/H)^(1/n));
sigma_max=min(sigma_data(LN(kk),:))+2*sigma_ar;
epsilon_max=min(epsilon_data(LN(kk),:))+2*epsilon_ar;
pyx=epsilon_max-max(epsilon_data(kk,:));
pyy=sigma_max-max(sigma_data(kk,:));
epsilon_data(kk,:)=epsilon_data(kk,:)+pyx;
sigma_data(kk,:)=sigma_data(kk,:)+pyy; 
clear sigma_max epsilon_max epsilon_ar epsilon_ar pyx pyy
else
end
end
end
%% Stress-strain Curve
% Reference Ramberg-Osgood flow curve
RSF=linspace(0,max(sigma_data(1,:)),100);
ESF=(RSF/E)+(RSF/H).^(1/n);
figure (1)
plot(ESF,RSF,'--','color','k')
hold on
for kk = 1:v
plot(epsilon_data(kk,:),sigma_data(kk,:),'k')
hold on
plot(max(epsilon_data(kk,:)),max(sigma_data(kk,:)),'x','color','k') 
hold on
plot(min(epsilon_data(kk,:)),min(sigma_data(kk,:)),'x','color','k')
end
grid on
xlabel('Strain')
ylabel('Stress (MPa)')
title('Stress-strain Curve')
