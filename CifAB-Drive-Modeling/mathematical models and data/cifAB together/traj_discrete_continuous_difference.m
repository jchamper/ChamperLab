clc;clear;close all;
FONTSIZE = 20;
LINEWIDTH = 2;
GENERATIONS = 10;
INTRO = 0.362;

%continuous
[gen,al,ca] = cifAB_together_odeplot([0,GENERATIONS],INTRO,1,1,1,0);
figure;hold on;
plot(gen,al,'LineWidth', LINEWIDTH,'LineStyle','-','Color','#ec9bad');
plot(gen,ca,'LineWidth', LINEWIDTH,'LineStyle','--','Color','#ec9bad');
%discrete
[gen,al,ca] = cifAB_together_plot([0,GENERATIONS],INTRO,1,1,1,0);
plot(gen,al,'LineWidth', LINEWIDTH,'LineStyle','-','Color','#5698c3');
plot(gen,ca,'LineWidth', LINEWIDTH,'LineStyle','--','Color','#5698c3');
ylim([0.1,0.55]);
xlabel("Generation");
ylabel("Frequency");
fontsize(gcf,FONTSIZE,'points');
legend1 = legend(["allele frequency (continuous)";"carrier freqeuncy (continuous)";"allele frequency (discrete)";"carrier freqeuncy (discrete)"],'FontSize',15);
set(legend1,...
    'Position',[0.222023823679912 0.267944060973007 0.566071414415326 0.19981751259226]);
set(gcf,'OuterPosition',[27 101 576 642]);
set(gca,'Position',[0.18 0.231751824817518 0.63 0.618406902006191]);
exportgraphics(gcf,['traj continuous discrete comparison' '.png'],'Resolution',600);