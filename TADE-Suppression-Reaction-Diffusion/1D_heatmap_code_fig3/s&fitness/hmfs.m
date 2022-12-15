clear all
close all
clc
fvar=0.8:0.004:1;
svar=0.5:0.01:1;

data=zeros(length(fvar),length(svar));

for i=1:length(fvar)
    for j=1:length(svar)
        f=fvar(i)
        s=svar(j)
        data(i,j)=finitedifference1d(f,s);
    end
end

datatest=data;
ii=find(data<0.007 &data>-0.007);
datatest(ii)=nan;

H=heatmap(svar,fvar,datatest,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('s')
ylabel('f')
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
