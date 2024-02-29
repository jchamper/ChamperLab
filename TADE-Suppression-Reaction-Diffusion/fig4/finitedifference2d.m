function data=finitedifference2d(radius,ss)
dr=0.1;dt=.01;
r=0:dr:40;t=0:dt:50;
beta=5;

D=0.1;s=1;
X1=zeros(length(t),length(r));
X2=zeros(length(t),length(r));
X3=zeros(length(t),length(r));
X4=zeros(length(t),length(r));
X5=zeros(length(t),length(r));
X6=zeros(length(t),length(r));

%initial condition
N0=1;
rr=r<=radius;
X1(1,:)=N0;
X2(1,:)=0.8*N0*rr;

%boundary condition
% X1(:,1)=N0;
X1(:,end)=N0;

for n=2:length(t)
    N=X1(n-1,2:end-1)+X2(n-1,2:end-1)+X3(n-1,2:end-1)+X4(n-1,2:end-1)+X5(n-1,2:end-1)+X6(n-1,2:end-1);
    %     N(N==0)=1;
    lambda = (1 - beta) * N + beta;
    X1(n,2:end-1)=X1(n-1,2:end-1)+dt/(dr)^2*D*(X1(n-1,3:end)-2*X1(n-1,2:end-1)+X1(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X1(n-1,3:end)-X1(n-1,2:end-1))+ ...
        dt*(lambda./N.*(X1(n-1,2:end-1).*(X1(n-1,2:end-1)+(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2)*(1-s)*(1+(1-ss)^2))+ ...
        (1-s)^2*(1-ss)^2*(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2).^2)-N.*X1(n-1,2:end-1));
    X2(n,2:end-1)=X2(n-1,2:end-1)+dt/(dr)^2*D*(X2(n-1,3:end)-2*X2(n-1,2:end-1)+X2(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X2(n-1,3:end)-X2(n-1,2:end-1))+ ...
        dt*(lambda./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)*(1-ss)+1/4*(1+s)+1/2*(1-s)*ss*(1-ss))+ ...
        X3(n-1,2:end-1)*(1/2*s*(1-ss)+1/2*s+(1-s)*ss*(1-ss))+X4(n-1,2:end-1)+X5(n-1,2:end-1)*1/2*(1+s)+X6(n-1,2:end-1)*s)+...
        (1-s)*(1-ss)*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X3(n-1,2:end-1)*(1/2*(1+2*s)+(1-s)*ss)+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)))-N.*X2(n-1,2:end-1));
    X3(n,2:end-1)=X3(n-1,2:end-1)+dt/(dr)^2*D*(X3(n-1,3:end)-2*X3(n-1,2:end-1)+X3(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X3(n-1,3:end)-X3(n-1,2:end-1))+ ...
        dt*((1-s)*lambda./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1-ss)^2+1/4)+ ...
        X3(n-1,2:end-1)*(1/2*(1-ss)^2+1/2)+X5(n-1,2:end-1)*1/2+X6(n-1,2:end-1))+...
        (1-s)*(1-ss)^2*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*1/8+X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/8+X6(n-1,2:end-1)*1/4)+ ...
        (1-s)*(1-ss)^2*X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/4+X6(n-1,2:end-1)*1/2))-N.*X3(n-1,2:end-1));
    X4(n,2:end-1)=X4(n-1,2:end-1)+dt/(dr)^2*D*(X4(n-1,3:end)-2*X4(n-1,2:end-1)+X4(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X4(n-1,3:end)-X4(n-1,2:end-1))+ ...
        dt*(lambda./N.*X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16*(1+s+(1-s)*ss)^2+ ...
        X3(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X4(n-1,2:end-1)*1/4*(1+s+(1-s)*ss)+X5(n-1,2:end-1)*1/8*(1+s+(1-s)*ss)^2+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/4*(s+(1-s)*ss)^2+X4(n-1,2:end-1)*1/2*(s+(1-s)*ss)+ ...
        X5(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+X6(n-1,2:end-1)*1/2*(s+(1-s)*ss)^2))-N.*X4(n-1,2:end-1));
    X5(n,2:end-1)=X5(n-1,2:end-1)+dt/(dr)^2*D*(X5(n-1,3:end)-2*X5(n-1,2:end-1)+X5(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X5(n-1,3:end)-X5(n-1,2:end-1))+ ...
        dt*((1-s)*(1-ss)*lambda./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/8*(1-s)*ss+1/8*(1+s))+ ...
        X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/4*(1+2*s))+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss))+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/2*s)+X4(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(s+(1-s)*ss)))-N.*X5(n-1,2:end-1));
    X6(n,2:end-1)=X6(n-1,2:end-1)+dt/(dr)^2*D*(X6(n-1,3:end)-2*X6(n-1,2:end-1)+X6(n-1,1:end-2))+dt/dr*D./r(2:end-1).*(X6(n-1,3:end)-X6(n-1,2:end-1))+ ...
        dt*((1-s)^2*(1-ss)^2*lambda./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16+X3(n-1,2:end-1)/8+X5(n-1,2:end-1)/8+ ...
        X6(n-1,2:end-1)/4)+X3(n-1,2:end-1).*(X3(n-1,2:end-1)/4+X5(n-1,2:end-1)/4+X6(n-1,2:end-1)/2))- ...
        N.*X6(n-1,2:end-1));
end



q=(X2/2+X3/2+X4+X5+X6)./(X1+X2+X3+X4+X5+X6);
q_50=q(50/dt,:);
a=find(q_50>0.2);
% if isempty(a)
%     data=nan
% else
    q_45=q(40/dt,:);
    b=find(q_45>0.2);
%  q_40=q(40/dt,:);
%     b=find(q_40>0.2);
% end

if isempty(b)
    data=nan
else
    if isempty(a)
        data=-b(end)*dr/5
    else
        data=(a(end)-b(end))*dr/5
    end
end


% figure
% hold on
% plot(r,q(1,:))
% plot(r,q(500,:))
% plot(r,q(1000,:))
% plot(r,q(1500,:))
% plot(r,q(2000,:))