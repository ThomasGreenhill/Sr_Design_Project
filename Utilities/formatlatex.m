%% formatlatex.m
%   Sets the default figure format to latex
%   
%   Inputs:
%       {none}
%   
%   Outputs:
%       {none}
%
%   Notes:
%       'defaultfigureposition' and font size parameters can be adjusted 
%       for smaller screens if plots are too big
%
%   History:
%       02.01.2021: Copied and pasted from previous projects
%

function [] = formatlatex()

reset(groot)
set(groot, 'defaulttextinterpreter', 'latex')
set(groot, 'defaultcolorbarticklabelinterpreter', 'latex')
set(groot, 'defaultfigureposition', [100, 100, 1000, 600])
set(groot, 'defaultaxesticklabelinterpreter', 'latex')
set(groot, 'defaultlegendinterpreter', 'latex')
set(groot, 'defaultaxesfontsize', 24)
set(groot, 'defaultaxeslinewidth', 1)
set(groot, 'defaultscattermarker', 'x')
set(groot, 'defaultscatterlinewidth', 3.5)
set(groot, 'defaultlinemarkersize', 15)
set(groot, 'defaultlinelinewidth', 2.5)
set(groot, 'defaultAxesXgrid', 'on', 'defaultAxesYgrid', 'on', 'defaultAxesZgrid', 'on')
set(groot, 'defaultAxesGridLineStyle', '-.')
set(groot, 'defaultAxesXlim', [0, 2 * pi]);
set(groot, 'defaultAxesYlim', [-0.6, 0.6]);

end