% close all;clc;clear all;
% migration_odeplot_(200,0.975,0.7,0.05,1);
function [generation_list,al,ca,lal,lca] = migration_odeplot_(generations,F,intro,mig,drawplot)
    F = sqrt(F);
    y0 = [intro;0;1-intro;0;0;1];
    function dy = odemig(t,y)
        [dd,wd,ww,ldd,lwd,lww] = deal(y(1),y(2),y(3),y(4),y(5),y(6));
        rdd = dd^2 + dd * wd + 1/4 * wd^2;
        rwd = 1/2 * wd^2 + wd * dd + 1/2 * ww * wd + ww * dd;
        rww = ww^2 + 1/2 * ww * wd + 1/4 * wd^2;
        
        rldd = ldd^2 + ldd * lwd + 1/4 * lwd^2;
        rlwd = 1/2 * lwd^2 + lwd * ldd + 1/2 * lww * lwd + lww * ldd;
        rlww = lww^2 + 1/2 * lww * lwd + 1/4 * lwd^2;
        [rdd,rldd] = deal((1-mig)*rdd + mig*rldd, (1-mig)*rldd + mig*rdd);
        [rwd,rlwd] = deal((1-mig)*rwd + mig*rlwd, (1-mig)*rlwd + mig*rwd);
        [rww,rlww] = deal((1-mig)*rww + mig*rlww, (1-mig)*rlww + mig*rww);
        N = dd + wd + ww;
        d_dd = F^2 * rdd *9/(8*N+1)/ N- dd * N; 
        d_wd = F * rwd *9/(8*N+1)/ N - wd * N;
        d_ww = rww *9/(8*N+1)/ N - ww * N;

        N = ldd + lwd + lww;
        d_ldd = F^2 * rldd *9/(8*N+1)/ N- ldd * N; 
        d_lwd = F * rlwd *9/(8*N+1)/ N - lwd * N;
        d_lww = rlww*9/(8*N+1) / N - lww * N;
        dy = [d_dd;d_wd;d_ww;d_ldd;d_lwd;d_lww];
    end
    if isequal(size(generations),[1,1])
        [T,Y] = ode45(@odemig,1:generations,y0);
    else [T,Y] = ode45(@odemig,generations,y0);

    
    end
    generation_list = T';
    intro_size = Y(:,1) + Y(:,2) + Y(:,3);
    linked_size = Y(:,4) + Y(:,5) + Y(:,6);
    Y(:,1) = Y(:,1) ./ intro_size;
    Y(:,2) = Y(:,2) ./ intro_size;
    Y(:,3) = Y(:,3) ./ intro_size;
    Y(:,4) = Y(:,4) ./ linked_size;
    Y(:,5) = Y(:,5) ./ linked_size;
    Y(:,6) = Y(:,6) ./ linked_size;
    al = (Y(:,1) + 1/2*Y(:,2))';
    ca = (Y(:,1) + Y(:,2))';
    lal = (Y(:,4) + 1/2*Y(:,5))';
    lca = (Y(:,4) + Y(:,5))';
    if (drawplot == 1)
        plot(generation_list,al,generation_list,ca,generation_list,lal,generation_list,lca);
    end
end

