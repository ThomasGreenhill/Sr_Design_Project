function [figH] = PlotDragPolar(dataSet, dragBreakDown, caseName, lgd, figSize, saveInfo, mark, ending)
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
    CD_0_mark = 1e12;
    CD_0_stored = [];
    hold on
    for ii = 1:length(fieldNames)
        matrix = dataSet.data.(fieldNames(ii));
        CL_arr = matrix(:,7);
        CDi_arr = matrix(:,8);
        if dragBreakDown.bool == true
            CDo_arr = dragBreakDown.f_total ./ dragBreakDown.S_ref;
        else
            CDo_arr = matrix(:,9);
        end
        CD_arr = CDi_arr + CDo_arr;
        plot(CL_arr, CD_arr, 'LineWidth', 2) 
        
        CL_0_index = (abs(CL_arr) == min(abs(CL_arr)));
        CD_0_current = CD_arr(CL_0_index);

        if CD_0_current <= CD_0_mark
            CD_0_mark = CD_0_current;
            CD_0_stored = [CL_arr(CL_0_index), CD_0_current]; 
        end

    end
    
    % Scatter CD_0
    if mark.CD_o == true
        xd = (max(xticks) - min(xticks)) / (length(xticks) - 1);
        yd = (max(yticks) - min(yticks)) / (length(yticks) - 1);
        scatter(CD_0_stored(1), CD_0_stored(2), 1500, 'x', 'k')
        text(CD_0_stored(1) + xd / 10, CD_0_stored(2) + yd / 2, ...
            strcat("$C_{D_0} =",num2str(CD_0_stored(2),4),"$"), ...
            'fontsize', 18, 'Interpreter', 'latex')
    end
        
    hold off
    legend(lgd, 'Location', 'northwest', 'fontsize', 16, 'Interpreter', 'latex')
    if length(fieldNames) == 1
        ttl = strcat("Drag Polar for ", caseName, ending);
    else
        ttl = strcat("Drag Polars for ", caseName, ending);
    end
    title(ttl, 'fontsize', 20, 'Interpreter', 'latex')
    xlabel("Lift Coefficient $C_L$", 'fontsize', 18, 'Interpreter', 'latex')
    ylabel("Drag Coeffieicnt $C_D$", 'fontsize', 18, 'Interpreter', 'latex')
    grid on

    if saveInfo.save == true
       saveas(figH, strcat(saveInfo.path, ttl, saveInfo.saveType)) 
    end

end