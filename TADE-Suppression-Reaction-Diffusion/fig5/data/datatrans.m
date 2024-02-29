clear
close all
clc
Widthvar=0.1:0.1:2;
Dvar=0.005:0.005:0.1;
Middle=zeros(length(Widthvar),length(Dvar));
Overbarrier=zeros(length(Widthvar),length(Dvar));
Middletime=zeros(length(Widthvar),length(Dvar));
Overbarriertime=zeros(length(Widthvar),length(Dvar));
for jj=1:20
    width=0.1*jj;
    load(['data_barrier',num2str(width),'.mat'])
    Middle(jj,:)=middle;
    Middletime(jj,:)=middletime;
    Overbarrier(jj,:)=overbarrier;
    Overbarriertime(jj,:)=overbarriertime;
end

H=heatmap(Dvar,Widthvar*2,Middletime*0.0005,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
ylabel('corridor width')
xlabel('D')
title('reach the end of the barrier')
saveas(H,'fig_5a.jpg')

figure
H=heatmap(Dvar,Widthvar*2,Overbarriertime*0.0005,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
ylabel('corridor width')
xlabel('D')
title('pass through the barrier')
saveas(H,'fig_5b.jpg')
