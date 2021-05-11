
%{
Run this script for a quick save for FS data from google spread sheet
Please strictly stick to the field names included
Ask Xuchang before adding or changing fields (they will affect plotting)

History:
    04.23.2021, XT. Created.
    04.24.2021, XT. Debugged.
%}

clc
clear
close all
%% Manually Input This Section!!!
% Version Direction
versionDir = "v2.1/no_prop/v2.1_nlg";  % Make sure it's the right version!

% Save file name
fileName = "CTOL_zoomed";  % Double check the name matches in plot

% Included flap configurations
flapConfig = ["f0", "f4u", "f4d"];  % Keep the field names this way
%flapConfig = ["f4d"];

%% Not designed to change in this section
saveParentDir = "./FS Data";

if not(isfolder(strcat(saveParentDir, '/', versionDir)))
   mkdir(strcat(saveParentDir, '/', versionDir))
end

fileType = ".mat";
savePath = strcat(saveParentDir, "/", versionDir, "/", fileName, fileType);
numDataSet = length(flapConfig);
data.fields = flapConfig;
fprintf(strcat("******Inputting data for ", fileName, "******\n"))
sizes = zeros(2, numDataSet);

for ii = 1:numDataSet
    
    if not(isstring(flapConfig(ii))) && not(ischar(flapConfig(ii)))
        fprintf(strcat("flapConfig element", string(ii), " is not string or character array"))
    else
        
        cont = true;
        while cont == true
            inputMat = input(strcat("Please enter the matrix for '", flapConfig(ii), "'\nRemember to add []: \n"));
            
            if isnumeric(inputMat)
                cont = false;
                [numRows, numCols] = size(inputMat);
                fprintf(strcat("Field '", flapConfig(ii), "' successfully added\n\n"))
            end
            
        end
        data.(flapConfig{ii}) = inputMat;
        sizes(:,ii) = [numRows; numCols];
    end
    
end

data.size = sizes;
fprintf("All fields successfully added!\n\n")
save(savePath, 'data');
