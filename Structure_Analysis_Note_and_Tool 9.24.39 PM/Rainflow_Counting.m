Y=[0 350*1.1 0 350 70 280 70 210 70 140 70 0 350];
[m,n]=size(Y);
dx=1;
X=1:dx:n;
figure (1)
plot(X,Y)
c=rainflow(Y);
TT = array2table(c,'VariableNames',{'Count','Range','Mean','Start','End'});
