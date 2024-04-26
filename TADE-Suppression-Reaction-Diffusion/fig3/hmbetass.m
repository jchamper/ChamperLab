clear all
close all
clc

betavar=2:0.16:10;
ssvar=0.4:0.008:0.7;
tic
D = 0.1;
f = 1;
s = 1;
data=zeros(length(betavar),length(ssvar));

for i=1:length(betavar)
    for j=1:length(ssvar)
        ss=ssvar(j)
        beta=betavar(i)
        data(i,j)=finitedifference1d(f,beta, D, ss, s);
    end
end
toc
H=heatmap(ssvar,betavar,data,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('ss')
ylabel('\beta')

Xticklabel=cell(size(H.XDisplayLabels))
[Xticklabel{:}]=deal('');
[Xticklabel{1:5:51}]=H.XDisplayLabels{1:5:51};
H.XDisplayLabels=Xticklabel

Yticklabel=cell(size(H.YDisplayLabels))
[Yticklabel{:}]=deal('');
[Yticklabel{1:5:50}]=H.YDisplayLabels{1:5:50};
H.YDisplayLabels=Yticklabel
s = struct(H);
s.XAxis.TickLabelRotation = 45;

saveas(H,'fig_3_beta_ss_0.4_0.7.jpg')
save data_beta_ss_0.4_0.7
