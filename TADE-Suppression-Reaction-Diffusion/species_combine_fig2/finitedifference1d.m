% function data=finitedifference1d(D,beta)
D=0.1;beta=5;
dx=0.1;dt=.01;
x=-20:dx:20;t=0:dt:50;
gamma=beta-1;
lambda=beta-1;
s=1;ss=0;
X1=zeros(length(t),length(x));
X2=zeros(length(t),length(x));
X3=zeros(length(t),length(x));
X4=zeros(length(t),length(x));
X5=zeros(length(t),length(x));
X6=zeros(length(t),length(x));


%initial condition
N0=lambda/gamma;
xx=x>=-5 & x<=5;
X1(1,:)=N0-0.8*N0*xx;
X2(1,:)=0.8*N0*xx;


%boundary condition
X1(:,1)=0;
X1(:,end)=0;

for n=2:length(t)
    N=X1(n-1,2:end-1)+X2(n-1,2:end-1)+X3(n-1,2:end-1)+X4(n-1,2:end-1)+X5(n-1,2:end-1)+X6(n-1,2:end-1);
%     N(N==0)=1;
    X1(n,2:end-1)=X1(n-1,2:end-1)+dt/(dx)^2*D*(X1(n-1,3:end)-2*X1(n-1,2:end-1)+X1(n-1,1:end-2))+ ...
        dt*(lambda./N.*(X1(n-1,2:end-1).*(X1(n-1,2:end-1)+(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2)*(1-s)*(1+(1-ss)^2))+ ...
        (1-s)^2*(1-ss)^2*(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2).^2)-gamma*N.*X1(n-1,2:end-1));
    X2(n,2:end-1)=X2(n-1,2:end-1)+dt/(dx)^2*D*(X2(n-1,3:end)-2*X2(n-1,2:end-1)+X2(n-1,1:end-2))+ ...
        dt*(lambda./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)*(1-ss)+1/4*(1+s)+1/2*(1-s)*ss*(1-ss))+ ...
        X3(n-1,2:end-1)*(1/2*s*(1-ss)+1/2*s+(1-s)*ss*(1-ss))+X4(n-1,2:end-1)+X5(n-1,2:end-1)*1/2*(1+s)+X6(n-1,2:end-1)*s)+...
        (1-s)*(1-ss)*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X3(n-1,2:end-1)*(1/2*(1+2*s)+(1-s)*ss)+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)))-gamma*N.*X2(n-1,2:end-1));
    X3(n,2:end-1)=X3(n-1,2:end-1)+dt/(dx)^2*D*(X3(n-1,3:end)-2*X3(n-1,2:end-1)+X3(n-1,1:end-2))+ ...
        dt*((1-s)*lambda./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1-ss)^2+1/4)+ ...
        X3(n-1,2:end-1)*(1/2*(1-ss)^2+1/2)+X5(n-1,2:end-1)*1/2+X6(n-1,2:end-1))+...
        (1-s)*(1-ss)^2*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*1/8+X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/8+X6(n-1,2:end-1)*1/4)+ ...
        (1-s)*(1-ss)^2*X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/4+X6(n-1,2:end-1)*1/2))-gamma*N.*X3(n-1,2:end-1));
    X4(n,2:end-1)=X4(n-1,2:end-1)+dt/(dx)^2*D*(X4(n-1,3:end)-2*X4(n-1,2:end-1)+X4(n-1,1:end-2))+ ...
        dt*(lambda./N.*X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16*(1+s+(1-s)*ss)^2+ ...
        X3(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X4(n-1,2:end-1)*1/4*(1+s+(1-s)*ss)+X5(n-1,2:end-1)*1/8*(1+s+(1-s)*ss)^2+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/4*(s+(1-s)*ss)^2+X4(n-1,2:end-1)*1/2*(s+(1-s)*ss)+ ...
        X5(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+X6(n-1,2:end-1)*1/2*(s+(1-s)*ss)^2))-gamma*N.*X4(n-1,2:end-1));
    X5(n,2:end-1)=X5(n-1,2:end-1)+dt/(dx)^2*D*(X5(n-1,3:end)-2*X5(n-1,2:end-1)+X5(n-1,1:end-2))+ ...
        dt*((1-s)*(1-ss)*lambda./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/8*(1-s)*ss+1/8*(1+s))+ ...
        X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/4*(1+2*s))+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss))+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/2*s)+X4(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(s+(1-s)*ss)))-gamma*N.*X5(n-1,2:end-1));
    X6(n,2:end-1)=X6(n-1,2:end-1)+dt/(dx)^2*D*(X6(n-1,3:end)-2*X6(n-1,2:end-1)+X6(n-1,1:end-2))+ ...
        dt*((1-s)^2*(1-ss)^2*lambda./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16+X3(n-1,2:end-1)/8+X5(n-1,2:end-1)/8+ ...
        X6(n-1,2:end-1)/4)+X3(n-1,2:end-1).*(X3(n-1,2:end-1)/4+X5(n-1,2:end-1)/4+X6(n-1,2:end-1)/2))-gamma*N.*X6(n-1,2:end-1));
end

figure
t=10;
hold on
plot(x,X1(t/dt,:)+X2(t/dt,:)+X3(t/dt,:)+X4(t/dt,:)+X5(t/dt,:)+X6(t/dt,:),'LineWidth',1)
plot(x,X1(t/dt,:),'LineWidth',1.5)
plot(x,X2(t/dt,:),'LineWidth',1.5)
plot(x,X3(t/dt,:),'LineWidth',1.5)
plot(x,X4(t/dt,:),'LineWidth',1.5)
plot(x,X5(t/dt,:),'LineWidth',1.5)
plot(x,X6(t/dt,:),'LineWidth',1.5)
lgd=legend('N','X_{1}','X_{2}','X_{3}','X_{4}','X_{5}','X_{6}')
lgd.FontSize=9;
xlabel('x-position','FontSize',10)
ylabel('Genotype Frequency','FontSize',10)

q=(X2/2+X3/2+X4+X5+X6)./(X1+X2+X3+X4+X5+X6);
figure
hold on
plot(x,q(1,:),'LineWidth',1.5)
plot(x,q(10/dt,:),'LineWidth',1.5)
plot(x,q(20/dt,:),'LineWidth',1.5)
plot(x,q(30/dt,:),'LineWidth',1.5)
plot(x,q(40/dt,:),'LineWidth',1.5)
plot(x,q(50/dt,:),'LineWidth',1.5)
lgd=legend('t=0','t=10','t=20','t=30','t=40','t=50')
lgd.FontSize=10;
xlabel('x-position','FontSize',10)
ylabel('Drive alle Frequency','FontSize',10)