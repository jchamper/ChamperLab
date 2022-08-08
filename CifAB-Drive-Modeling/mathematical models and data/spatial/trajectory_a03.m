clc;clear;close all;

%change k and b, plot the stuff in a circular arena, plot freq-r as well.
k = 0;
b = 4;
r_crit = 0.2;

num_points = 500; %number of points to plot in R axis
LINEWIDTH = 2;
%linemap
subplot(211);hold on;
r_w = linspace(0,0.5,num_points); %length of arena is 2r-1
w = ones(1,num_points);
r_d = r_w(1:round(length(r_w)*2*r_crit));
d = k*r_d + b;
d = [d zeros(1,(length(w)-length(d)))];
plot(r_w,w,r_w,d,'LineWidth', LINEWIDTH);
limits = [0,1+max(d)+0.1];
ylim(limits);
xlim([0,0.5]);
xlabel('Radius');
ylabel('Relative density');
fontsize(gca,15,'points');
legend('Wild-type homozygotes', 'Drive homozygotes');
set(gca,'Position',[0.13 0.61 0.775 0.31]);

%3D map
subplot(212);hold on;
num_points = 2*num_points-1;
[X,Y] = meshgrid(linspace(0,1,num_points));
%wt
W = ones(num_points);
W([1,end],:) = 0;
W(:,[1,end]) = 0;
zlim(limits);
mesh(X,Y,W,'EdgeColor','#5698c3','FaceAlpha','texturemap');
D = 1 + spinner(d);
mesh(X,Y,D,'EdgeColor','interp');
view(gca,[-227.4 39.6000000048183]);
fontsize(gca,15,'points');
set(gca,'Position',[0.13 0.061 0.775 0.382377541239974]);




exportgraphics(gcf,['traj_03uniform_circle' '.png'],'Resolution',600);