clear all
clc

v_inf = 87 * 0.514444;
R = 41 * 0.0254;
n = 1854.4805 / 60;
T_req = 425.6896 * 4.44822;
Cl = 0.4;
B = 3;
a_0 = deg2rad(-2);

m0fn = @(Ma) (2 * pi ./ sqrt(1 - Ma.^2)) .* (Ma <= 0.9) + (2 * pi ./ ...
              sqrt(1 - 0.9^2)) .* (Ma > 0.9);
          
Cdfn = @(Cl) 0.0095 + 0.0040 * (Cl - 0.2).^2;


[r, c, bet, Pdesign, Tdesign, Qdesign, etap, the, dCTdx] = ...
    propdesign(R, v_inf, n, T_req, Cl, B, m0fn, a_0, Cdfn);

Pdesign = Pdesign * 0.00134102
T_req
Tdesign