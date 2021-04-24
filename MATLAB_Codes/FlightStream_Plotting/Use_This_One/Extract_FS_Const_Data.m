function [outputStructs] = Extract_FS_Const_Data(filePath, fieldReq)
%{
Extracts the data output from FS constant flow analysis
Data output stored in .mat files

Input:
    filePath: (string)
        Path to .mat file


Output:
	outputStructs: (array-like)
        Output array of structs, each with 12 fields of data.
        The array size depends on the data set number stored
   
History:
    04.23.2021, XT. Created.
    04.23.2021, XT. Debugged

%}

% Checking
if not(isstring(filePath))
    
    if ischar(filePath)
        filePath = convertCharsToStrings(filePath);
    else
        fprintf("Error: Please provide the filePath as a string")
        return
    end
    
end

charNum = 0;
for index = 1:length(fieldReq)
    
    if not(isstring(fieldReq(index)))
        
        if ischar(fieldReq(index))
           charNum = charNum + 1;
        end
        
    end
    
end

if (charNum ~= 0) && (charNum ~= length(fieldReq))
    fprintf("Error: Required field names are not all character array or string. ")
    fprintf("Exiting Extract_FS_Const_Data function...\n")
elseif charNum == length(fieldReq)
    fieldReq = convertCharsToStrings(fieldReq);
end

if not(isfile(filePath))
    fprintf("Error: Target file does not exist. Exiting Extract_FS_Const_Data function...\n")
    return 
end
    
% Loading data
metaData = load(filePath);
fields = fieldnames(metaData);  % field names

if isempty(fields)
   fprintf("Error: Extracted file is empty. Exiting Extract_FS_Const_Data function...\n") 
   return
end

% Extracting
for dataNum = 1:length(fields)
    [~, numCols] = size(metaData.(fields{dataNum}));
    
    if numCols ~= length(fieldReq)
       fprintf("Error: The FS data format has incorrect column number: ")
       fprintf(string(numCols))
       fprintf(strcat("\nThere should be" , string(length(fieldReq)), " columns\n"))
       fprintf("Exiting Extract_FS_Const_Data function...\n")
       return
    end
    
    for col = 1:numCols
        data.(fieldReq{col}) = metaData.(fields{dataNum})(:,col);
    end
    
    outputStructs(dataNum) = data;
end

end
