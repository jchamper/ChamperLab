function [X1_save,X2_save,X4_save]=barrier_snapshot(width,D)
%assume s=1;ss=0;
%so X3=X5=X6=0;
middle=0;
overbarrier=0;
middletime=0;
overbarriertime=0;
beta=8;
tend=150;
dx=0.02;dy=0.02;
dt=.0005;
x=-5:dx:5;y=-6:dy:2;
%set the barrier
placex=find(x<width & x>-width);placey=find(y<-2 & y>-4);
midx=ceil(length(x)/2);
barriermidy=placey(ceil(length(placey)/2));
overbarriery=floor((placey(end)+length(y))/2);
X1=zeros(length(x),length(y));
X2=zeros(length(x),length(y));
X4=zeros(length(x),length(y));
X1_save = cell(30,1);
X2_save = cell(30,1);
X4_save = cell(30,1);
t_save = 1;

N0=1;

%boundary condition
X1(:,1)=N0;
X1(:,end)=N0;
X1(1,:)=N0;
X1(end,:)=N0;
X1(1,placey(1)+1:placey(end)-1)=0;
X1(end,placey(1)+1:placey(end)-1)=0;
X1(placex(1)-1:placex(end)+1,placey(1)+1:placey(end)-1)=N0;
X1(:,placey(1))=N0;
X1(:,placey(end))=N0;

X1X1=X1;X2X2=X2;X4X4=X4;
X1_i=X1;X2_i=X2;X4_i=X4;

%initial condition
xx=x<=5 &x>=-5;yy=y<-4.5 &y>-6;
[X Y]=meshgrid(yy,xx);
a=X&Y;
X1=N0-0.5*N0*a;
X2=0.5*N0*a;
% X1(:,:,1)=N0;
% X2(:,:,1)=0;
X1(:,placey(1)+1:placey(end)-1)=0;
X1(placex(1)-1:placex(end)+1,placey(1)+1:placey(end)-1)=N0;


for n=2:tend/dt+1
    % before barrier
    N=X1(2:end-1,2:placey(1)-1)+X2(2:end-1,2:placey(1)-1)+X4(2:end-1,2:placey(1)-1);
    lambda = (1 - beta) * N + beta;

    X1X1(2:end-1,2:placey(1)-1)=X1(2:end-1,2:placey(1)-1)+dt/(dx)^2*D*(X1(3:end,2:placey(1)-1)-2*X1(2:end-1,2:placey(1)-1)+X1(1:end-2,2:placey(1)-1))+dt/(dy)^2*D*(X1(2:end-1,3:placey(1))-2*X1(2:end-1,2:placey(1)-1)+X1(2:end-1,1:placey(1)-2))+ ...
        dt*(lambda./N.*(X1(2:end-1,2:placey(1)-1).^2)-N.*X1(2:end-1,2:placey(1)-1));
    X2X2(2:end-1,2:placey(1)-1)=X2(2:end-1,2:placey(1)-1)+dt/(dx)^2*D*(X2(3:end,2:placey(1)-1)-2*X2(2:end-1,2:placey(1)-1)+X2(1:end-2,2:placey(1)-1))+dt/(dy)^2*D*(X2(2:end-1,3:placey(1))-2*X2(2:end-1,2:placey(1)-1)+X2(2:end-1,1:placey(1)-2))+ ...
        dt*(lambda./N.*(X1(2:end-1,2:placey(1)-1).*(X2(2:end-1,2:placey(1)-1)+X4(2:end-1,2:placey(1)-1)))-N.*X2(2:end-1,2:placey(1)-1));
    X4X4(2:end-1,2:placey(1)-1)=X4(2:end-1,2:placey(1)-1)+dt/(dx)^2*D*(X4(3:end,2:placey(1)-1)-2*X4(2:end-1,2:placey(1)-1)+X4(1:end-2,2:placey(1)-1))+dt/(dy)^2*D*(X4(2:end-1,3:placey(1))-2*X4(2:end-1,2:placey(1)-1)+X4(2:end-1,1:placey(1)-2))+ ...
        dt*(lambda./N.*X2(2:end-1,2:placey(1)-1).*(X2(2:end-1,2:placey(1)-1)/4+X4(2:end-1,2:placey(1)-1)/2)-N.*X4(2:end-1,2:placey(1)-1));
    
    % in barrier
    N=X1(placex,placey)+X2(placex,placey)+X4(placex,placey);
    lambda = (1 - beta) * N + beta;
    X1X1(placex,placey)=X1(placex,placey)+dt/(dx)^2*D*(X1(placex+1,placey)-2*X1(placex,placey)+X1(placex-1,placey))+dt/(dy)^2*D*(X1(placex,placey+1)-2*X1(placex,placey)+X1(placex,placey-1))+ ...
        dt*(lambda./N.*(X1(placex,placey).^2)-N.*X1(placex,placey));
    X2X2(placex,placey)=X2(placex,placey)+dt/(dx)^2*D*(X2(placex+1,placey)-2*X2(placex,placey)+X2(placex-1,placey))+dt/(dy)^2*D*(X2(placex,placey+1)-2*X2(placex,placey)+X2(placex,placey-1))+ ...
        dt*(lambda./N.*(X1(placex,placey).*(X2(placex,placey)+X4(placex,placey)))-N.*X2(placex,placey));
    X4X4(placex,placey)=X4(placex,placey)+dt/(dx)^2*D*(X4(placex+1,placey)-2*X4(placex,placey)+X4(placex-1,placey))+dt/(dy)^2*D*(X4(placex,placey+1)-2*X4(placex,placey)+X4(placex,placey-1))+ ...
        dt*(lambda./N.*X2(placex,placey).*(X2(placex,placey)/4+X4(placex,placey)/2)-N.*X4(placex,placey));
    
    % after barrier
    N=X1(2:end-1,placey(end)+1:end-1)+X2(2:end-1,placey(end)+1:end-1)+X4(2:end-1,placey(end)+1:end-1);
    lambda = (1 - beta) * N + beta;
    X1X1(2:end-1,placey(end)+1:end-1)=X1(2:end-1,placey(end)+1:end-1)+dt/(dx)^2*D*(X1(3:end,placey(end)+1:end-1)-2*X1(2:end-1,placey(end)+1:end-1)+X1(1:end-2,placey(end)+1:end-1))+dt/(dy)^2*D*(X1(2:end-1,placey(end)+2:end)-2*X1(2:end-1,placey(end)+1:end-1)+X1(2:end-1,placey(end):end-2))+ ...
        dt*(lambda./N.*(X1(2:end-1,placey(end)+1:end-1).^2)-N.*X1(2:end-1,placey(end)+1:end-1));
    X2X2(2:end-1,placey(end)+1:end-1)=X2(2:end-1,placey(end)+1:end-1)+dt/(dx)^2*D*(X2(3:end,placey(end)+1:end-1)-2*X2(2:end-1,placey(end)+1:end-1)+X2(1:end-2,placey(end)+1:end-1))+dt/(dy)^2*D*(X2(2:end-1,placey(end)+2:end)-2*X2(2:end-1,placey(end)+1:end-1)+X2(2:end-1,placey(end):end-2))+ ...
        dt*(lambda./N.*(X1(2:end-1,placey(end)+1:end-1).*(X2(2:end-1,placey(end)+1:end-1)+X4(2:end-1,placey(end)+1:end-1)))-N.*X2(2:end-1,placey(end)+1:end-1));
    X4X4(2:end-1,placey(end)+1:end-1)=X4(2:end-1,placey(end)+1:end-1)+dt/(dx)^2*D*(X4(3:end,placey(end)+1:end-1)-2*X4(2:end-1,placey(end)+1:end-1)+X4(1:end-2,placey(end)+1:end-1))+dt/(dy)^2*D*(X4(2:end-1,placey(end)+2:end)-2*X4(2:end-1,placey(end)+1:end-1)+X4(2:end-1,placey(end):end-2))+ ...
        dt*(lambda./N.*X2(2:end-1,placey(end)+1:end-1).*(X2(2:end-1,placey(end)+1:end-1)/4+X4(2:end-1,placey(end)+1:end-1)/2)-N.*X4(2:end-1,placey(end)+1:end-1));

%     barriermid=(X2(midx,barriermidy)/2+X3(midx,barriermidy)/2+X4(midx,barriermidy)+X5(midx,barriermidy)+X6(midx,barriermidy))./(X1(midx,barriermidy)+X2(midx,barriermidy)+X3(midx,barriermidy)+X4(midx,barriermidy)+X5(midx,barriermidy)+X6(midx,barriermidy));
%     over=(X2(midx,overbarriery)/2+X3(midx,overbarriery)/2+X4(midx,overbarriery)+X5(midx,overbarriery)+X6(midx,overbarriery))./(X1(midx,overbarriery)+X2(midx,overbarriery)+X3(midx,overbarriery)+X4(midx,overbarriery)+X5(midx,overbarriery)+X6(midx,overbarriery));
    X1=X1X1;X2=X2X2;X4=X4X4;
    X1X1=X1_i;X2X2=X2_i;X4X4=X4_i;
    if n>5/dt*t_save
        X1_save{t_save,1} = X1;
        X2_save{t_save,1} = X2;
        X4_save{t_save,1} = X4;
        t_save = t_save + 1;
    end

    if  X1(midx,barriermidy)<0.7 & middle==0
          middle=1;
        middletime=n;
    end
    
    if X1(midx,overbarriery)<0.7
        overbarrier=1;
        overbarriertime=n;
        break
    end
end