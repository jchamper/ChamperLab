clear all
close all
clc
dvar=0.01:0.0038:0.2;
ssvar=0:0.008:0.4;
data=zeros(length(dvar),length(ssvar));

for i=1:length(dvar)
    for j=1:length(ssvar)
        D=dvar(i)
        ss=ssvar(j)
        data(i,j)=finitedifference1d(D,ss);
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

H=heatmap(ssvar,dvar,datatest,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('ss')
ylabel('D')
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

save data
