D=0.03;
width=1;
[X1_save, X2_save, X4_save] = barrier_snapshot(width,D)

save(['data_barrier_snapshot.mat'])


dx=0.02;dy=0.02;
x=-5:dx:5;y=-6:dy:2;
[XX,YY]=meshgrid(y,x);

hold on
total=(X1_save{1,1}+X2_save{1,1}+X4_save{1,1});
H=plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{4,1}+X2_save{4,1}+X4_save{4,1});
plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{8,1}+X2_save{8,1}+X4_save{8,1});
plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{12,1}+X2_save{12,1}+X4_save{12,1});
plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{16,1}+X2_save{16,1}+X4_save{16,1});
plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{20,1}+X2_save{20,1}+X4_save{20,1});
plot(y,total(255,:),'LineWidth',1.5)
total=(X1_save{24,1}+X2_save{24,1}+X4_save{24,1});
plot(y,total(255,:),'LineWidth',1.5)

lgd=legend('t=5','t=20','t=40','t=60','t=80','t=100','t=120')
lgd.FontSize=10;
xlabel('y-position','FontSize',10)
ylabel('Total Population ','FontSize',10)

saveas(H,'fig_5_snapshot.jpg')

figure
H = mesh(XX,YY,X1_save{20,1})
title("Total Population at t=100")
saveas(H,'fig_5_t100_snapshot.jpg')