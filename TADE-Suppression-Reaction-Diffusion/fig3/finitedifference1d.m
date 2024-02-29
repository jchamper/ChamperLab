function data=finitedifference1d(f, beta, D, ss, s)
dx=0.1;dt=.01;
x=-20:dx:20;t=0:dt:30;
X1=zeros(length(t),length(x));
X2=zeros(length(t),length(x));
X3=zeros(length(t),length(x));
X4=zeros(length(t),length(x));
X5=zeros(length(t),length(x));
X6=zeros(length(t),length(x));


%initial condition
N0=1;
xx=x>=-5 & x<=5;
X1(1,:)=N0-0.8*N0*xx;
X2(1,:)=0.8*N0*xx;


%boundary condition
X1(:,1)=0;
X1(:,end)=0;

for n=2:length(t)
    N=X1(n-1,2:end-1)+X2(n-1,2:end-1)+X3(n-1,2:end-1)+X4(n-1,2:end-1)+X5(n-1,2:end-1)+X6(n-1,2:end-1);
%     N(N==0)=1;
    lambda = (1 - beta) * N + beta;
    X1(n,2:end-1)=X1(n-1,2:end-1)+dt/(dx)^2*D*(X1(n-1,3:end)-2*X1(n-1,2:end-1)+X1(n-1,1:end-2))+ ...
        dt*(lambda./N.*(X1(n-1,2:end-1).*(X1(n-1,2:end-1)+(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2)*(1-s)*(1+(1-ss)^2))+ ...
        (1-s)^2*(1-ss)^2*(X2(n-1,2:end-1)*1/4+X3(n-1,2:end-1)*1/2).^2)-N.*X1(n-1,2:end-1));
    X2(n,2:end-1)=X2(n-1,2:end-1)+dt/(dx)^2*D*(X2(n-1,3:end)-2*X2(n-1,2:end-1)+X2(n-1,1:end-2))+ ...
        dt*(lambda*f./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)*(1-ss)+1/4*(1+s)+1/2*(1-s)*ss*(1-ss))+ ...
        X3(n-1,2:end-1)*(1/2*s*(1-ss)+1/2*s+(1-s)*ss*(1-ss))+X4(n-1,2:end-1)+X5(n-1,2:end-1)*1/2*(1+s)+X6(n-1,2:end-1)*s)+...
        (1-s)*(1-ss)*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X3(n-1,2:end-1)*(1/2*(1+2*s)+(1-s)*ss)+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)))-N.*X2(n-1,2:end-1));
    X3(n,2:end-1)=X3(n-1,2:end-1)+dt/(dx)^2*D*(X3(n-1,3:end)-2*X3(n-1,2:end-1)+X3(n-1,1:end-2))+ ...
        dt*((1-s)*lambda*f./N.*(X1(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/4*(1-ss)^2+1/4)+ ...
        X3(n-1,2:end-1)*(1/2*(1-ss)^2+1/2)+X5(n-1,2:end-1)*1/2+X6(n-1,2:end-1))+...
        (1-s)*(1-ss)^2*X2(n-1,2:end-1).*(X2(n-1,2:end-1)*1/8+X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/8+X6(n-1,2:end-1)*1/4)+ ...
        (1-s)*(1-ss)^2*X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*1/4+X6(n-1,2:end-1)*1/2))-N.*X3(n-1,2:end-1));
    X4(n,2:end-1)=X4(n-1,2:end-1)+dt/(dx)^2*D*(X4(n-1,3:end)-2*X4(n-1,2:end-1)+X4(n-1,1:end-2))+ ...
        dt*(lambda*f*f./N.*X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16*(1+s+(1-s)*ss)^2+ ...
        X3(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X4(n-1,2:end-1)*1/4*(1+s+(1-s)*ss)+X5(n-1,2:end-1)*1/8*(1+s+(1-s)*ss)^2+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*1/4*(s+(1-s)*ss)^2+X4(n-1,2:end-1)*1/2*(s+(1-s)*ss)+ ...
        X5(n-1,2:end-1)*(1/4*(1+2*s)*(1-s)*ss+1/4*s*(1+s)+1/4*(1-s)^2*ss^2)+X6(n-1,2:end-1)*1/2*(s+(1-s)*ss)^2))-N.*X4(n-1,2:end-1));
    X5(n,2:end-1)=X5(n-1,2:end-1)+dt/(dx)^2*D*(X5(n-1,3:end)-2*X5(n-1,2:end-1)+X5(n-1,1:end-2))+ ...
        dt*((1-s)*(1-ss)*lambda*f*f./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)*(1/8*(1-s)*ss+1/8*(1+s))+ ...
        X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/4*(1+2*s))+X4(n-1,2:end-1)*1/4+X5(n-1,2:end-1)*(1/4*(1+s)+1/4*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss))+ ...
        X3(n-1,2:end-1).*(X3(n-1,2:end-1)*(1/2*(1-s)*ss+1/2*s)+X4(n-1,2:end-1)*1/2+X5(n-1,2:end-1)*(1/4*(1+2*s)+1/2*(1-s)*ss)+ ...
        X6(n-1,2:end-1)*(s+(1-s)*ss)))-N.*X5(n-1,2:end-1));
    X6(n,2:end-1)=X6(n-1,2:end-1)+dt/(dx)^2*D*(X6(n-1,3:end)-2*X6(n-1,2:end-1)+X6(n-1,1:end-2))+ ...
        dt*((1-s)^2*(1-ss)^2*lambda*f*f./N.*(X2(n-1,2:end-1).*(X2(n-1,2:end-1)/16+X3(n-1,2:end-1)/8+X5(n-1,2:end-1)/8+ ...
        X6(n-1,2:end-1)/4)+X3(n-1,2:end-1).*(X3(n-1,2:end-1)/4+X5(n-1,2:end-1)/4+X6(n-1,2:end-1)/2))-N.*X6(n-1,2:end-1));
end




q=(X2/2+X3/2+X4+X5+X6)./(X1+X2+X3+X4+X5+X6);
qq=q(500,1:floor(end/2));
qqq=q(3000,1:floor(end/2));
a=find(qq>0.2);
b=find(qqq>0.2);
if isempty(a)
    data=0
else
    if isempty(b)
        data=(a(1)-length(x)/2)*dx/25
    else
        data=(a(1)-b(1))*dx/25
    end
end


% if isempty(b)
%     if isempty(a)
%         data=-5/3
%     else
%         data=(a(1)-length(x)/2)*dx/27
%     end
% else
%     data=(a(1)-b(1))*dx/27
% end
