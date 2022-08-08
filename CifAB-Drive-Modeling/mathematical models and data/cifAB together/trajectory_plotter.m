clc;clear;close all;
FONTSIZE = 20;
LINEWIDTH = 2;

intro_list = fliplr([0.1,0.3,0.36,0.3605,0.36051,0.37,0.6,0.8]);
generations = 40;
x_label = 'Generation';
figure(1);hold on;
fontsize(gcf,FONTSIZE,'points');
figure(2);hold on;
fontsize(gcf,FONTSIZE,'points');
for intro = intro_list
    %specify color for intro=0.8
    if intro==0.8
        [generation_list,allele_frequency,carrier_frequency] = cifAB_together_odeplot([0,generations],intro,1,1,1,0);
        figure(1);
        plot(generation_list,allele_frequency,'LineWidth', LINEWIDTH,'Color','#ec9bad');
        figure(2);
        plot(generation_list,carrier_frequency,'LineWidth', LINEWIDTH,'Color','#ec9bad');
        continue
    end
    [generation_list,allele_frequency,carrier_frequency] = cifAB_together_odeplot([0,generations],intro,1,1,1,0);
    figure(1);
    plot(generation_list,allele_frequency,'LineWidth', LINEWIDTH);
    figure(2);
    plot(generation_list,carrier_frequency,'LineWidth', LINEWIDTH);
end

% figure(1);
% set(gcf,'OuterPosition',[27 101 576 642]);
% set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
% xlabel(x_label,'FontSize',FONTSIZE);
% ylabel('Drive allele frequency','FontSize',FONTSIZE);
% exportgraphics(gcf,['t01 allele' '.png'],'Resolution',600);

figure(2);
set(gcf,'OuterPosition',[27 101 576 642]);
set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
xlabel(x_label,'FontSize',FONTSIZE);
ylabel('Drive carrier frequency','FontSize',FONTSIZE);
legend1 = legend(fliplr(["0.1","0.3","0.36","0.3605","0.36051","0.37","0.6","0.8"]));
set(legend1,...
    'Position',[0.4363 0.567556270121748 0.373214280019913 0.163321163314972],...
    'NumColumns',2,...
    'FontSize',12);
set(gcf,'OuterPosition',[27 101 576 642]);
set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
exportgraphics(gcf,['t01 carrier' '.png'],'Resolution',600);