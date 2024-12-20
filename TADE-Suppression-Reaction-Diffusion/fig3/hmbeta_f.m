clear all
close all
clc
fvar=0.8:0.004:1;
betavar=2:0.16:10;
D = 0.2;
ss = 0;
s = 1;

data=zeros(length(fvar),length(betavar));

for i=1:length(fvar)
    for j=1:length(betavar)
        f=fvar(i)
        beta=betavar(j)
        data(i,j)=finitedifference1d(f,beta, D, ss, s);
    end
end

datatest=data;
ii=find(data<0.007 &data>-0.007);
datatest(ii)=nan;

H=heatmap(betavar,fvar,datatest,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('\beta')
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


saveas(H,'fig_3_f_beta.jpg')
save data_f_beta
