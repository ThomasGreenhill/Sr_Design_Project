function [figH] = PlotLiftCurve(dataSet, caseName, lgd, figSize, saveInfo)

    % Checking
    if not(isstring(caseName)) && not(ischar(caseName))
        error("Error: caseName should be a string or a character array") 
    end
    
    if not(isstring(lgd)) && not(ischar(lgd))
        error("Error: lgd should be a string array or a character array")
    end

    % Main
    fieldNames = dataSet.data.fields;
    figH = figure('Renderer', 'painters', 'Position', figSize);
    hold on
    for ii = 1:length(fieldNames)
        matrix = dataSet.data.(fieldNames(ii));
        alf_arr = matrix(:,1);
        CL_arr = matrix(:,7);
        plot(alf_arr, CL_arr) 
    end
    hold off
    legend(lgd, 'Location', 'best', 'Interpreter', 'latex')
    if length(fieldNames) == 1
        ttl = strcat("Lift Curve for ", caseName);
    else
        ttl = strcat("Lift Curves for ", caseName); 
    end
    title(ttl, 'Interpreter', 'latex')
    xlabel("$Angle of Attack \alpha$", 'Interpreter', 'latex')
    ylabel("Lift Coefficient $C_L$", 'Interpreter', 'latex')
    grid on
    
    if saveInfo.save == true
       saveas(figH, strcat(saveInfo.path, ttl, saveInfo.saveType)) 
    end

end