%% Ballard_VeloCity.m
% SCRIPT to produce data for Honeywell/Ballard VeloCity series H2 fuel cells
%
%   Inputs:
%       {none}
%   
%   Outputs:
%       fuelcelldata.mat
%
%   Notes:
%       Data taken from the following datasheets:
%           https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcvelocity-md30-spec-sheet
%           https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcvelocity-hd-spec-sheet
%           https://www.ballard.com/about-ballard/publication_library/product-specification-sheets/fcmovetm-spec-sheet
%           70kW has subsystems fully integrated whereas others do not
%
%   History:
%       02.06.2021: Created, TVG
%

fuelcelldata.Names = ["30kW FCveloCity-MD"; "85kW FCveloCity-HD85"; "100kW FCveloCity-HD100"; "70kW FCmove-HD"];
    
fuelcelldata.RatedPower.Units = "W";
fuelcelldata.RatedPower.Data = [30e3; 85e3; 100e3; 70e3]; %W

fuelcelldata.MinVoltage.Units = "V";
fuelcelldata.MinVoltage.Data = [85; 260; 357; 250];
    
fuelcelldata.MaxVoltage.Units = "V";
fuelcelldata.MaxVoltage.Data = [180; 419; 577; 500];

fuelcelldata.MaxCurrent.Units = "A";
fuelcelldata.MaxCurrent.Data = [300; 284; 257; 240];

fuelcelldata.CellDimensions.Units = "m";
fuelcelldata.CellDimensions.Data = [900, 480, 375;
                                1130, 869, 487;
                                1200, 869, 487;
                                1812, 816, 415]*1e-3; %m [l1, w1, h1; l2, w2, h2; ...]

fuelcelldata.CellWeight.Units = "kg";    
fuelcelldata.CellWeight.Data = [125; 256; 280; 250]; %kg 
                                        
fuelcelldata.CoolantDimensions.Units = "m";
fuelcelldata.CoolantDimensions.Data = [0, 0, 0;
                                       737, 529, 379;
                                       737, 529, 379;
                                       0, 0, 0]*1e-3; %m [l1, w1, h1; l2, w2, h2; ...]

fuelcelldata.CoolantWeight.Units = "kg";
fuelcelldata.CoolantWeight.Data = [0; 44; 44; 0];

fuelcelldata.AirDimensions.Units = "m";
fuelcelldata.AirDimensions.Data = [0, 0, 0;
                                   676, 418, 352;
                                   676, 418, 352;
                                   0, 0, 0]*1e-3; %m [l1, w1, h1; l2, w2, h2; ...]

fuelcelldata.AirWeight.Units = "kg";
fuelcelldata.AirWeight.Data = [0; 61; 61; 0];
                                       

fuelcelldata.Oxidant = ["Air"; "Air"; "Air"; "Air"];

fuelcelldata.FuelFlowRate.Units = "kg.s^-1";
fuelcelldata.FuelFlowRate.Data = [0.7; 0; 0; 0]*1e-3; %kg.s^-1 

fuelcelldata.FuelEfficiency = [0; 0; 0; 0.57];

fuelcelldata.SoundLevel.Units = "dBa";
fuelcelldata.SoundLevel.Data = [75; 0; 0; 0]; %dBa

save("fuelcelldata.mat")
                                        

