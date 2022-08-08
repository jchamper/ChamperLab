clc;clear;close all;
FONTSIZE = 20;
LINEWIDTH = 2;

I = 0.5;
F = 0.9;

colorA = '#ec9bad';
colorB = '#5698c3';

generations = 300;
figure;hold on;
x_label = 'Generation';
fontsize(gcf,FONTSIZE,'points');
[generation_list,cifa_allele,cifb_allele,cifa_carrier,cifb_carrier] = different_loci_regular_odeplot([0,generations],I,F,0);

plot(generation_list,cifa_allele,'LineWidth', LINEWIDTH,'LineStyle','--','Color',colorA);
plot(generation_list,cifa_carrier,'LineWidth', LINEWIDTH,'LineStyle','-','Color',colorA);
plot(generation_list,cifb_allele,'LineWidth', LINEWIDTH,'LineStyle','--','Color',colorB);
plot(generation_list,cifb_carrier,'LineWidth', LINEWIDTH,'LineStyle','-','Color',colorB);

set(gcf,'OuterPosition',[27 101 576 642]);
set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
xlabel(x_label,'FontSize',FONTSIZE);
ylabel('Frequency','FontSize',FONTSIZE);
legend1 = legend('CifA allele','CifA carrier','CifB allele','CifB carrier');
set(legend1,...
    'Position',[0.52023810114534 0.63108273126058 0.27142856605351 0.19981751259226],...
    'FontSize',15);
exportgraphics(gcf,['t13 fitness 0.9 intro 0.5' '.png'],'Resolution',600);
