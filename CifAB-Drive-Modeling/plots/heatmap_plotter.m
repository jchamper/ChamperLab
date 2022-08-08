function heatmap_plotter(title_,xdata,ydata,colordata,xlabel,ylabel,num_xpoints,xround,num_ypoints,yround,colordata_range,show_colorbar,colormap_,missing_data_color)
    %12 or 13 parameters
    %titlelabel is what's in the figure. title_ is the name of the figure.
    %num_xpoints is the number of labels on x axis. 
    %colordata_range is 1x2 row vector. Blue in the first item, yellow in the second.
    warning off;
    figure;
    set_missing_data = false;
    if nargin == 12
        colormap_ = colormap('parula');
    end

    if nargin >= 13
        if colormap_ == 0
            %generation
            colormap_ = colormap('summer');
        end
        if colormap_ == 1
            %frequency
            colormap_ = colormap('parula');
        end
        if colormap_ == 2
            %max freqeuncy
            colormap_ = colormap(othercolor('BrBG9')); 
        end
        if colormap_ == 3
            %max frequency generation
            colormap_ = colormap(othercolor('BuOr_8')); 
        end
    end

    if nargin == 14
        set_missing_data = true;
    end


    colordata = flipud(colordata);
    ydata = fliplr(ydata);
    h = heatmap(xdata,ydata,colordata);
    h.Colormap = colormap_;

    h.XLabel = xlabel;
    h.YLabel = ylabel;
    h.XDisplayLabels = repmat(' ',[length(xdata),1]);
    h.YDisplayLabels = repmat(' ',[length(ydata),1]);

    xlabels = round(linspace(1,length(xdata),num_xpoints));
    ylabels = round(linspace(1,length(ydata),num_ypoints));
    for i = xlabels
        h.XDisplayLabels(i) = num2cell(round(xdata(i),xround));
    end
    for i = ylabels
        h.YDisplayLabels(i) = num2cell(round(ydata(i),yround));
    end

    if colordata_range(1) > colordata_range(2)
        h.Colormap = flipud(h.Colormap);
        colordata_range = fliplr(colordata_range);
    end
    h.ColorLimits = colordata_range;

    grid off;
    if ~show_colorbar
        colorbar off;
    end
    set(struct(h).NodeChildren(3), 'XTickLabelRotation', 0); % put instead of the last example line
    h.FontSize = 20;

    if set_missing_data
        if missing_data_color == 0
            missing_data_color = '#a4aca7';
        end
        h.MissingDataColor = missing_data_color;
    end



    set(gcf,'OuterPosition',[27 101 576 642]);
    set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
    exportgraphics(gcf,[title_ '.png'],'Resolution',600);
%     close;
end