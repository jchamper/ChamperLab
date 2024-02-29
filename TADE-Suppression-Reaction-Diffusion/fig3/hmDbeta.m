clear all
close all
clc
dvar=0.004:0.004:0.2;
betavar=2:0.16:10;
tic
f = 1;
s = 1;
ss = 0;
data=zeros(length(dvar),length(betavar));

for i=1:length(dvar)
    for j=1:length(betavar)
        D=dvar(i)
        beta=betavar(j)
        data(i,j)=finitedifference1d(f,beta, D, ss, s);
    end
end
toc
H=heatmap(betavar,dvar,data,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('\beta')
ylabel('D')

% Xticklabel=cell(size(H.XDisplayLabels))
% [Xticklabel{:}]=deal('');
% [Xticklabel{1:5:51}]=H.XDisplayLabels{1:5:51};
% H.XDisplayLabels=Xticklabel
% 
% Yticklabel=cell(size(H.YDisplayLabels))
% [Yticklabel{:}]=deal('');
% [Yticklabel{1:5:50}]=H.YDisplayLabels{1:5:50};
% H.YDisplayLabels=Yticklabel
% s = struct(H);
% s.XAxis.TickLabelRotation = 45;

datatest=data;
ii=find(data<0.005 &data>-0.005);
datatest(ii)=nan;

H=heatmap(betavar,dvar,datatest,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('beta')
ylabel('D')
title('Wavespeed')

Xticklabel=cell(size(H.XDisplayLabels))
[Xticklabel{:}]=deal('');
[Xticklabel{1:5:end}]=H.XDisplayLabels{1:5:end};
H.XDisplayLabels=Xticklabel

Yticklabel=cell(size(H.YDisplayLabels))
[Yticklabel{:}]=deal('');
[Yticklabel{1:5:end}]=H.YDisplayLabels{1:5:end};
H.YDisplayLabels=Yticklabel
H.MissingDataLabel='0'
s = struct(H);
s.XAxis.TickLabelRotation = 45;
caxis([-0.17,0.17])

saveas(H,'fig_3_D_beta.jpg')
save data_D_beta
