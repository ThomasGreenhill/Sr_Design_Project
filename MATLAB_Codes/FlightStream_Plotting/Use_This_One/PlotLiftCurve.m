function [figH] = PlotLiftCurve(dataSet, caseName, lgd, figSize, saveInfo, mark)

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
    CL_max_mark = -1e12;
    CL_max_stored = [];
    hold on
    for ii = 1:length(fieldNames)
        matrix = dataSet.data.(fieldNames(ii));
        alf_arr = matrix(:,1);
        CL_arr = matrix(:,7);
        plot(alf_arr, CL_arr, 'LineWidth', 2) 
        
        CL_max_index = (CL_arr == max(CL_arr));
        CL_max_current = CL_arr(CL_max_index);
        
        if CL_max_current >= CL_max_mark
            CL_max_mark = CL_max_current;
            CL_max_stored = [alf_arr(CL_max_index), CL_max_current];
        end
        
    end
    
    % Scatter CL_max
    if mark.CL_max == true
        xd = (max(xticks) - min(xticks)) / (length(xticks) - 1);
        yd = (max(yticks) - min(yticks)) / (length(yticks) - 1);
        scatter(CL_max_stored(1), CL_max_stored(2), 1500, 'x', 'k')
        text(CL_max_stored(1) - 1.2 * xd, CL_max_stored(2) - yd / 10, ...
            strcat("$C_{L_{max}} =",num2str(CL_max_stored(2),4),"$"), ...
            'fontsize', 18, 'Interpreter', 'latex')
    end
    
    hold off
    legend(lgd, 'Location', 'northwest', 'fontsize', 16, 'Interpreter', 'latex')
    if length(fieldNames) == 1
        ttl = strcat("Lift Curve for ", caseName);
    else
        ttl = strcat("Lift Curves for ", caseName); 
    end
    title(ttl, 'fontsize', 20, 'Interpreter', 'latex')
    xlabel("$Angle of Attack \alpha$", 'fontsize', 18, 'Interpreter', 'latex')
    ylabel("Lift Coefficient $C_L$", 'fontsize', 18, 'Interpreter', 'latex')
    grid on
    
    if saveInfo.save == true
       saveas(figH, strcat(saveInfo.path, ttl, saveInfo.saveType)) 
    end

end