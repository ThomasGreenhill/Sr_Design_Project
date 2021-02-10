%% 3D Propeller Plotting Utility (single)
function [] = plotblade3D(r, R, c, bet, B, line1)

Rxfn = @(bet) [1, 0, 0; 0, cos(bet), sin(bet); 0, -sin(bet), cos(bet)];

bet = bet(r > 0.15*R);
c = c(r > 0.15*R);
line1 = line1(r > 0.15*R);
r = r(r > 0.15*R);

x = [r, flip(r)];
y = [c / 2 + line1, flip(line1 - c / 2)];
bb = [bet, flip(bet)];
z = zeros(size(x));

vec = [x; y; z];
rotvec = zeros(size(vec));

figure('Position', [100, 100, 800, 800])

for ii = 1:length(x)
    rotvec(:, ii) = Rxfn(bb(ii)) * vec(:, ii);
end

for Blades = 1:B
    the = 2 * pi / B * Blades;
    xrot = x * cos(the) - y * sin(the);
    yrot = x * sin(the) + y * cos(the);

    fill3(xrot, yrot, rotvec(3, :), 'k')
    alpha(0.75)
    hold on
    axis([-5, 5, -5, 5])
    xlabel("x")
    ylabel("y")
    zlabel("z")
    axis equal
end

end