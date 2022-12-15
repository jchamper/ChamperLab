dvar=0.004:0.004:0.2;
middle=zeros(1,length(dvar));
overbarrier=zeros(1,length(dvar));
middletime=zeros(1,length(dvar));
overbarriertime=zeros(1,length(dvar));
for i=1:length(dvar)
    width
    D=dvar(i)
    [middle(i),overbarrier(i),middletime(i),overbarriertime(i)]=barrier(width,D);
    if overbarrier(i)==0
        break
    end
end

save(['data_width=',num2str(width),'.mat'])

figure
data=Overbarriertime;
ii=find(data==0);
data(ii)=nan;

H=heatmap(Dvar,Widthvar,data*0.0005,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('D')
ylabel('width')

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
temp1=caxis;
s = struct(H);
s.XAxis.TickLabelRotation = 45;
colorbar
saveas(H,'fig_5b.jpg')
colorbar('off')
saveas(H,'fig_5b_nocolorbar.jpg')

figure
data=Middletime;
ii=find(data==0);
data(ii)=nan;

H=heatmap(Dvar,Widthvar,data*0.0005,'Colormap',turbo)
H.NodeChildren(3).YDir='normal';
H.CellLabelColor = 'none'
H.GridVisible = 'off'
xlabel('D')
ylabel('width')

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
caxis(temp1)
s = struct(H);
s.XAxis.TickLabelRotation = 45;
colorbar
saveas(H,'fig_5a.jpg')
colorbar('off')
saveas(H,'fig_5a_nocolorbar.jpg')


