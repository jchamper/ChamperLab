clc;clear;close all;

legend_list = ["K=1000";"K=5000";"K=10000";"K=50000";"K→∞(continuous)";"K→∞(discrete)"];
x = 0.33:0.0025:0.4;
%continuous model threshold: 0.3611
%discrete model threshold: 0.3645
s1=[0.065, 0.09, 0.03, 0.105, 0.135, 0.155, 0.175, 0.235, 0.215, 0.255, 0.355, 0.31, 0.395, 0.49, 0.51, 0.58, 0.67, 0.635, 0.715, 0.735, 0.755, 0.835, 0.78, 0.85, 0.895, 0.89, 0.89, 0.95, 0.96];
s2=[0.0, 0.0, 0.0, 0.005, 0.005, 0.005, 0.035, 0.025, 0.04, 0.08, 0.16, 0.225, 0.27, 0.455, 0.545, 0.605, 0.765, 0.79, 0.85, 0.905, 0.935, 0.98, 0.975, 1.0, 0.995, 1.0, 1.0, 1.0, 1.0];
s3=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.015, 0.02, 0.065, 0.21, 0.25, 0.375, 0.475, 0.655, 0.83, 0.85, 0.93, 0.96, 0.995, 0.99, 0.985, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0];
s4=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.015, 0.07, 0.23, 0.515, 0.83, 0.95, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0];
x5 = 0.33:0.001:0.4;
s5=x5>=0.3611;
s6=x5>=0.3645;
plot(x,s1,x,s2,x,s3,x,s4,'LineWidth',2);
hold on;
plot(x5,s5,"Linestyle","--",'LineWidth',2);
plot(x5,s6,'LineWidth',2);
fontsize(gca,18,'points');
xlim([min(x),max(x)]);
xlabel('Introduction frequency');
ylabel('Drive establishment rate');
ylim([-0.003,1.003]);
legend1 = legend(legend_list,'Location','southeast');
set(legend1,...
    'Position',[0.17 0.0852946431325058 0.64 0.147766318876309],...
    'NumColumns',2);
set(gcf,'OuterPosition',[68 61 576 676]);
set(gca,'Position',[0.17 0.38 0.64 0.58]);
exportgraphics(gcf,['sim01_panmictic' '.png'],'Resolution',600);