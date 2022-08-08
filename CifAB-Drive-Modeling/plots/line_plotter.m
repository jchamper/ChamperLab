% clc;clear;close all;
% x = 1:10;
% y = 10:-1:1;
% line_plotter_('title',x,y,'bg','bg');

function line_plotter_(title_,xdata,ydata,x_label,y_label)
    FONTSIZE = 20;
    LINEWIDTH = 2;
    plot(xdata,ydata,'LineWidth', LINEWIDTH);
    xlabel(x_label);
    ylabel(y_label);
    ylim([0,1]);
    xlim([min(xdata),max(xdata)+0.0001]);
%     set(gca,'XTickLabel','');
%     set(gca,'YTickLabel','');
    fontsize(gca,FONTSIZE,'points');
    grid on;
    set(gcf,'OuterPosition',[27 101 576 642]);
    set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
    exportgraphics(gcf,[title_ '.png'],'Resolution',600);
%     close;
end
