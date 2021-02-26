%% Update the value of crack size for each cycle
C2=3*10^-7; % Material constant.
Kc=70; % Material constant.
c=0.125; % Radius of circle.
ai=0.25; % Initial crack length.
a=ai; % Initial condition of a.
Smin=[0 20 24 24 18 28];
Smax=[46 46 40 36 42 44];
DeltaN=[1 2 3 17 3 3];
%{
% Final crack length estimation.
syms ac 
dr=1-c/ac; Fr=0.5*(3-dr)*(1+1.243*(1-dr)^3);
eqn= Kc==Fr*max(Smax)*sqrt(pi*(ac-c));
af=double(vpasolve(eqn,ac,[0.3 0.8])); % in inch
clear Fr dr eqn
%}
%{
% Reference plot
at=linspace(0,af,1000);
[u,v]=size(at);
Kref=Kc*ones(u,v);
Kt=46.*0.5*(3-(1-c./at)).*(1+1.243*(1-(1-c./at)).^3).*sqrt(pi*(at-c));
figure (1)
plot(at,Kt)
hold on
plot(at,Kref,'--')
ylim([0 80])
grid on
%}
% intial condition for the loop
j=1; 
while j>0
t=mod(j,29);
if t==27 || t==28 || t==0
    k=6;
elseif t==1
    k=1;
elseif t==2 || t==3
    k=2;
elseif t==4 || t==5 || t==6
    k=3;
elseif t==24 || t==25 || t==26
    k=5;    
else
    k=4;
end
clear t
DeltaS=Smax(k)-Smin(k);
R=Smin(k)/Smax(k);
for v=1:DeltaN(k)
d=(a-c)/a; F=0.5*(3-d)*(1+1.243*(1-d)^3);
DeltaK=F*DeltaS*sqrt(pi*(a-c));
daN=(C2*(DeltaK)^(2.2))/((1-R)*Kc-DeltaK);  da=daN;
a=a+da;
clear d F daN da
j=j+1;
end
clear DeltaS R
if DeltaK>Kc
Flight=floor(j/sum(DeltaN));
break
else
end
end