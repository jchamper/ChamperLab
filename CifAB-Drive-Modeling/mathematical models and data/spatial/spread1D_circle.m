function [ndd,nwd,nww] = spread1D_circle_(dd,wd,ww,dt,dx,D,F)
    %input: array of dd,wd,ww in last status, size is 1*len(x)
    %       dt,dx
    %       dispersal coefficient D
    %       homozygote fitness F
    %output: array of dd,wd,ww in next status, size is 1*len(x)

    %Radius is 5, so length of arena is still 10.
    lambda = 10; %low density growth rate
    lenx = length(dd);
    [ndd,nwd,nww] = deal(zeros(1,lenx));
    N = dd(2:end-1) + wd(2:end-1) + ww(2:end-1);
    
    nww(2:end-1)=ww(2:end-1)+D*dt*(1/(dx)^2*(ww(3:end)-2*ww(2:end-1)+ww(1:end-2)) + 1./[dx:dx:(lenx-2)*dx] .* [ww(2:end-1)-ww(1:end-2)]/dx) + ...
    dt*((lambda-1)./((lambda-2)*N+1) .*(ww(2:end-1).^2 + 1/2 * ww(2:end-1) .* wd(2:end-1) + 1/4 * wd(2:end-1).^2)-N.*ww(2:end-1));
nwd(2:end-1)=wd(2:end-1)+D*dt*(1/(dx)^2*(wd(3:end)-2*wd(2:end-1)+wd(1:end-2)) + 1./[dx:dx:(lenx-2)*dx] .* [wd(2:end-1)-wd(1:end-2)]/dx) + ...
    dt*((lambda-1)./((lambda-2)*N+1).*(1/2 * wd(2:end-1).^2 + wd(2:end-1) .* dd(2:end-1) + 1/2 * ww(2:end-1) .* wd(2:end-1) + ww(2:end-1) .* dd(2:end-1)) * F-N.*wd(2:end-1));
ndd(2:end-1)=dd(2:end-1)+D*dt*(1/(dx)^2*(dd(3:end)-2*dd(2:end-1)+dd(1:end-2)) + 1./[dx:dx:(lenx-2)*dx] .* [dd(2:end-1)-dd(1:end-2)]/dx) + ...
    dt*((lambda-1)./((lambda-2)*N+1).*(dd(2:end-1).^2 + dd(2:end-1) .* wd(2:end-1) + 1/4 * wd(2:end-1).^2) * F^2-N.*dd(2:end-1));
N1 = dd(1) + wd(1) + ww(1);
    nww(1) = ww(1) + dt*((lambda-1)/((lambda-2)*N1+1) *(ww(1)^2 + 1/2 * ww(1) * wd(1) + 1/4 * wd(1)^2)-N1*ww(1));
    nwd(1) = wd(1) + dt*((lambda-1)/((lambda-2)*N1+1) *(1/2 * wd(1)^2 + wd(1) * dd(1) + 1/2 * ww(1) * wd(1) + ww(1) * dd(1)) * F-N1*wd(1));
    ndd(1) = dd(1) + dt*((lambda-1)/((lambda-2)*N1+1) *(dd(1)^2 + dd(1) * wd(1) + 1/4 * wd(1)^2) * F^2-N1*dd(1));
    nww(end) = 1;
end