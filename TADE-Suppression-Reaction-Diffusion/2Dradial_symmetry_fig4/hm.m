clear all
close all
clc
rvar=0.1:0.1:5;
ssvar=0:0.004:0.2;
data=zeros(length(rvar),length(ssvar));

for i=1:length(rvar)
    for j=1:length(ssvar)
        r=rvar(i)
        ss=ssvar(j)
        %         [data1(i,j),data2(i,j)]=finitedifference2d(D,ss);
        data(i,j)=finitedifference2d(r,ss);
    end
end

% H=heatmap(ssvar,dvar,data,'Colormap',turbo)
% H.NodeChildren(3).YDir='normal';
% H.CellLabelColor = 'none'
% H.GridVisible = 'off'
% xlabel('s^{‘}')
% ylabel('D')

H=heatmap(ssvar,rvar,data,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('ss')
ylabel('radius')

Xticklabel=cell(size(H.XDisplayLabels))
[Xticklabel{:}]=deal('');
[Xticklabel{1:5:50}]=H.XDisplayLabels{1:5:50};
H.XDisplayLabels=Xticklabel

Yticklabel=cell(size(H.YDisplayLabels))
[Yticklabel{:}]=deal('');
[Yticklabel{1:5:50}]=H.YDisplayLabels{1:5:50};
H.YDisplayLabels=Yticklabel
H.MissingDataLabel='0'
H. MissingDataColor=[0.7 0.7 0.7]
colorbar
saveas(H,'fig_4b.jpg')
colorbar('off')
saveas(H,'fig_4b_nocolorbar.jpg')

