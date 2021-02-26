%% Constant 
% Young's Modulus
E=71000; % From Table 14.1
H=977; % From Table 14.1
n=0.106; % From Table 14.1
% Stress Concentration
kt=4;
% Stress-strain curve data
deltae=[0.00563 0.00437 0.00480 0.00920 0.02900];
deltas=zeros(1,5);
[uu,vv]=size(deltas);
for i=1:vv
syms s
eqn1L=sum(deltae(uu,1:i));
eqn1R=s/E+(s/H)^(1/n);
eqn1 = eqn1L==eqn1R;
delsig=double(vpasolve(eqn1,s,[0 inf]));
if i==1
deltas(uu,i)=delsig;
else
deltas(uu,i)=delsig-sum(deltas(uu,1:i-1));
end
end
% Coefficients for life
sf=1466; % From Table 14.1
ef=0.262; % From Table 14.1
b=-0.143; % From Table 14.1
c=-0.619; % From Table 14.1
%% Normal Stress History
S=[0 336 48.3 336 48.3 292 48.3 255 48.3 219 48.3 181 48.3 143 48.3 105 48.3 67.6 ...
    48.3 67.6 -19.3 48.3 -67.6 48.3 -67.6 336];
[ii,jj]=size(S);
%% Stress-strain Curve data points
EGlobal= NaN(ii,(jj)*vv);
SGlobal= NaN(ii,(jj)*vv);
EGlobal(ii,1)=0;
SGlobal(ii,1)=0;
Nc=ones(1,jj);
% Initial conditions
u=1;
f=2;
E0 = 0; S0 = 0;
EL = 0; SL = 0;
P= zeros(uu,vv); 
PT=zeros(jj,vv);
signS=1;
for i=2:jj
E0 = E0 + signS*EL;
S0 = S0 + signS*SL;
delS=S(i)-S(i-1);
signS=delS/abs(delS);
sigEps=(kt*delS)^2/E;
EL = 0; SL = 0;
for j=1:vv
Str = SL + abs(signS-P(uu,j))*deltas(uu,j);
Etr = EL + abs(signS-P(uu,j))*deltae(uu,j);
sigEpsTr = Str*Etr; 
if sigEpsTr < sigEps
P(uu,j)=signS;
EGlobal(ii,u+1)=E0+signS*Etr;
SGlobal(ii,u+1)=S0+signS*Str;
SL = Str;
EL = Etr;  
u=u+1;
else
k=(Str-SL)/(Etr-EL);
Eint=((k*EL-SL)+sqrt((SL-k*EL)^2+4*k*sigEps))/(2*k);
Sint=SL+k*(Eint-EL);
P(uu,j)= P(uu,j)+ signS*(Sint-SL)/(deltas(uu,j));  
PT(i,:)=P;
EGlobal(ii,u+1)=E0+signS*Eint;
SGlobal(ii,u+1)=S0+signS*Sint;
SL = Sint;
EL = Eint;
u=u+1;
Nc(1,f)=u;
f=f+1;
break
end
end  
end
figure (1)
plot(EGlobal(uu,Nc(1):Nc(2)),SGlobal(uu,Nc(1):Nc(2)),'--')
hold on
for r=1:jj/2-1
plot(EGlobal(uu,Nc(2*r):Nc(2*(r+1))),SGlobal(uu,Nc(2*r):Nc(2*(r+1))),'k')  
hold on
end
hold on
for r=2:jj-1
plot(EGlobal(uu,Nc(r)),SGlobal(uu,Nc(r)),'x','color','k')  
hold on
end
grid on
legend('Piecewise-linear Reference','location','southeast')
xlabel('Strain')
ylabel('Stress (MPa)')
title('Stress-strain Curve')
clear delS sigEps sigEpsTr Sint Eint E0 S0 EL SL k 
clear i j ii jj uu vv r