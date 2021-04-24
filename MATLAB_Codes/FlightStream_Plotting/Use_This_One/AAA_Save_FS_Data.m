
%{
Run this script for a quick save for FS data from google spread sheet


History:
    04.23.2021, XT. Created.
%}

clc
clear all
close all
%% Manually Input This Section!!!
% Version Direction
versionDir = "v1.5";

% Save file name
fileName = "climb_zoomed";

% Included flap configurations
flapConfig = ["f0", "f4u", "f4d"];

%% Not designed to change in this section
saveParentDir = "./FS Data";
fileType = ".mat";
savePath = strcat(saveParentDir, "/", versionDir, "/", fileName, fileType);
numDataSet = length(flapConfig);
data.fields = flapConfig;
fprintf(strcat("******Inputting data for ", fileName, "******\n"))

for ii = 1:numDataSet
    
    if not(isstring(flapConfig(ii))) && not(ischar(flapConfig(ii)))
        fprintf(strcat("flapConfig element", string(ii), " is not string or character array"))
    else
        
        cont = true;
        while cont == true
            inputMat = input(strcat("Please enter the matrix for '", flapConfig(ii), "'\nRemember to add []: \n"));
            
            if isnumeric(inputMat)
                cont = false;
                fprintf(strcat("Field '", flapConfig(ii), "' successfully added\n\n"))
            end
            
        end
        data.(flapConfig{ii}) = inputMat;
    end
    
end

fprintf("All fields successfully added!\n\n")

save(savePath, 'data');
