function [figH] = PlotDragPolar(dataSet, caseName, lgd, figSize, saveInfo)
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
    tol = 1e-12;
    CD_0_stored = 1e12;
    hold on
    for ii = 1:length(fieldNames)
        matrix = dataSet.data.(fieldNames(ii));
        CL_arr = matrix(:,7);
        CDi_arr = matrix(:,8);
        CDo_arr = matrix(:,9);
        CD_arr = CDi_arr + CDo_arr;
        plot(CL_arr, CD_arr) 
        
        CL_0_index = (abs(CL_arr) == min(abs(CL_arr)));
        CD_0 = CD_arr(CL_0_index);

        if CD_0 <= CD_0_stored
            CD_0_stored = [CL_arr(CL_0_index), CD_0]; 
        end

    end
    
    % Scatter CD_0
    scatter(CD_0_stored(1), CD_0_stored(2), 1500, 'x', 'k')
    xt = xticks; yt = yticks;
    xd = (max(xticks) - min(xticks)) / (length(xticks) - 1);
    yd = (max(yticks) - min(yticks)) / (length(yticks) - 1);
    text(CD_0_stored(1) + xd / 10, CD_0_stored(2) + yd / 2, strcat("$C_{D_{0_{ext}}} =",num2str(CD_0_stored(2),4),"$"),'fontsize',18)
    
    hold off
    legend(lgd, 'Location', 'best', 'Interpreter', 'latex')
    if length(fieldNames) == 1
        ttl = strcat("Drag Polar for ", caseName);
    else
        ttl = strcat("Drag Polars for ", caseName);
    end
    title(ttl, 'Interpreter', 'latex')
    xlabel("Lift Coefficient $C_L$", 'Interpreter', 'latex')
    ylabel("Drag Coeffieicnt $C_D$", 'Interpreter', 'latex')
    grid on

    if saveInfo.save == true
       saveas(figH, strcat(saveInfo.path, ttl, saveInfo.saveType)) 
    end

end