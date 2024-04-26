clear all
close all
clc
svar=0.5:0.01:1;
ssvar=0.4:0.008:0.7;

data=zeros(length(svar),length(ssvar));
beta = 10;
D = 0.1;
f = 1;

for i=1:length(svar)
    for j=1:length(ssvar)
        s=svar(i)
        ss=ssvar(j)
        data(i,j)=finitedifference1d(f,beta, D, ss, s);
    end
end

% H=heatmap(ssvar,dvar,data,'Colormap',turbo)
% H.NodeChildren(3).YDir='normal';
% H.CellLabelColor = 'none'
% H.GridVisible = 'off'
% xlabel('ss')
% ylabel('D')
% title('Wavespeed')
% 
% Xticklabel=cell(size(H.XDisplayLabels))
% [Xticklabel{:}]=deal('');
% [Xticklabel{1:5:51}]=H.XDisplayLabels{1:5:51};
% H.XDisplayLabels=Xticklabel
% 
% Yticklabel=cell(size(H.YDisplayLabels))
% [Yticklabel{:}]=deal('');
% [Yticklabel{1:5:51}]=H.YDisplayLabels{1:5:51};
% H.YDisplayLabels=Yticklabel

datatest=data;
ii=find(data<0.005 &data>-0.005);
datatest(ii)=nan;

H=heatmap(ssvar,svar,datatest,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('ss')
ylabel('s')
title('Wavespeed')

Xticklabel=cell(size(H.XDisplayLabels))
[Xticklabel{:}]=deal('');
[Xticklabel{1:5:51}]=H.XDisplayLabels{1:5:51};
H.XDisplayLabels=Xticklabel

Yticklabel=cell(size(H.YDisplayLabels))
[Yticklabel{:}]=deal('');
[Yticklabel{1:5:51}]=H.YDisplayLabels{1:5:51};
H.YDisplayLabels=Yticklabel
H.MissingDataLabel='0'
s = struct(H);
s.XAxis.TickLabelRotation = 45;

saveas(H,'fig_3_s_ss_0.4_0.7.jpg')
save data_s_ss_0.4_0.7
