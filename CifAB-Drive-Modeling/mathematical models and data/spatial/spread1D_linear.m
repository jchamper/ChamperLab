function [ndd,nwd,nww] = spread1D_linear_(dd,wd,ww,dt,dx,D,F,e)
    %input: array of dd,wd,ww in last status, size is 1*len(x)
    %       dt,dx
    %       dispersal coefficient D
    %       homozygote fitness F
    %                                     
    %output: array of dd,wd,ww in next status, size is 1*len(x)
    if nargin == 7
        e = 1;
    end
    mwd = e; %male wd genotype, drive(toxin) works, 1
    mdd = 2*e-e^2; %male dd genotype, drive(toxin) works, 1
    fwd = 1-e; %female wd genotype, drive(antidote) doesn't work, 0
    fdd = (1-e)^2; %female dd genotype, drive(antidote) doesn't work, 0

    lambda = 10; %low density growth rate
    lenx = length(dd);
    [ndd,nwd,nww] = deal(zeros(1,lenx));
    nww(end) = 1; %right edge is all wild type
    ndd(1) = 1; %left edge is all drive homozygotes
    N = dd(2:end-1) + wd(2:end-1) + ww(2:end-1);
    nww(2:end-1)=ww(2:end-1)+dt/(dx)^2*D*(ww(3:end)-2*ww(2:end-1)+ww(1:end-2))+ ...
        dt*((lambda-1)./((lambda-2)*N+1) .*(ww(2:end-1).^2 + 1/2 * ww(2:end-1) .* wd(2:end-1) * (2-mwd) + 1/4 * wd(2:end-1).^2 * (1-mwd*fwd))-N.*ww(2:end-1));
    nwd(2:end-1)=wd(2:end-1)+dt/(dx)^2*D*(wd(3:end)-2*wd(2:end-1)+wd(1:end-2))+ ...
        dt*((lambda-1)./((lambda-2)*N+1).*(1/2 * wd(2:end-1).^2 * (1-mwd*fwd) + 1/2*wd(2:end-1) .* dd(2:end-1) * (2-mwd*fdd-mdd*fwd) + 1/2 * ww(2:end-1) .* wd(2:end-1)* (2-mwd) + ww(2:end-1) .* dd(2:end-1)* (2-mdd)) * F-N.*wd(2:end-1));
    ndd(2:end-1)=dd(2:end-1)+dt/(dx)^2*D*(dd(3:end)-2*dd(2:end-1)+dd(1:end-2))+ ...
        dt*((lambda-1)./((lambda-2)*N+1).*(dd(2:end-1).^2 * (1-mdd*fdd) + 1/2*dd(2:end-1) .* wd(2:end-1)* (2-mdd*fwd-mwd*fdd) + 1/4 * wd(2:end-1).^2* (1-mwd*fwd)) * F^2-N.*dd(2:end-1));
end