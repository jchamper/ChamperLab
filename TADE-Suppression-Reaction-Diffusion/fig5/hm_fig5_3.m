dvar=0.005:0.005:0.1;
% widthvar = 0.1:0.1:2;
widthvar=0.5;
middle=zeros(length(widthvar),length(dvar));
overbarrier=zeros(length(widthvar),length(dvar));
middletime=zeros(length(widthvar),length(dvar));
overbarriertime=zeros(length(widthvar),length(dvar));

for i=1:length(widthvar)
    for j=1:length(dvar)
        width = widthvar(i)
        D=dvar(j)
        [middle(i,j),overbarrier(i,j),middletime(i,j),overbarriertime(i,j)]=barrier(width,D);
    end
end

save(['data_barrier', num2str(widthvar), '.mat'])

% save(['data_width=',num2str(width),'.mat'])
% 
% figure
% data=Overbarriertime;
% ii=find(data==0);
% data(ii)=nan;
% 
% H=heatmap(Dvar,Widthvar,data*0.0005,'Colormap',turbo)
% H.NodeChildren(3).YDir='normal';
% H.CellLabelColor = 'none'
% H.GridVisible = 'off'
% xlabel('D')
% ylabel('width')
% 
% Xticklabel=cell(size(H.XDisplayLabels))
% [Xticklabel{:}]=deal('');
% [Xticklabel{1:5:50}]=H.XDisplayLabels{1:5:50};
% H.XDisplayLabels=Xticklabel
% 
% Yticklabel=cell(size(H.YDisplayLabels))
% [Yticklabel{:}]=deal('');
% [Yticklabel{1:5:50}]=H.YDisplayLabels{1:5:50};
% H.YDisplayLabels=Yticklabel
% H.MissingDataLabel='0'
% H. MissingDataColor=[0.7 0.7 0.7]
% temp1=caxis;
% s = struct(H);
% s.XAxis.TickLabelRotation = 45;
% colorbar
% saveas(H,'fig_5b.jpg')
% colorbar('off')
% saveas(H,'fig_5b_nocolorbar.jpg')
% 
% figure
% data=Middletime;
% ii=find(data==0);
% data(ii)=nan;
% 
% H=heatmap(Dvar,Widthvar,data*0.0005,'Colormap',turbo)
% H.NodeChildren(3).YDir='normal';
% H.CellLabelColor = 'none'
% H.GridVisible = 'off'
% xlabel('D')
% ylabel('width')
% 
% Xticklabel=cell(size(H.XDisplayLabels))
% [Xticklabel{:}]=deal('');
% [Xticklabel{1:5:50}]=H.XDisplayLabels{1:5:50};
% H.XDisplayLabels=Xticklabel
% 
% Yticklabel=cell(size(H.YDisplayLabels))
% [Yticklabel{:}]=deal('');
% [Yticklabel{1:5:50}]=H.YDisplayLabels{1:5:50};
% H.YDisplayLabels=Yticklabel
% H.MissingDataLabel='0'
% H. MissingDataColor=[0.7 0.7 0.7]
% caxis(temp1)
% s = struct(H);
% s.XAxis.TickLabelRotation = 45;
% colorbar
% saveas(H,'fig_5a.jpg')
% colorbar('off')
% saveas(H,'fig_5a_nocolorbar.jpg')
% 
% 
