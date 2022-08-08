% subplot(121);
% cifAB_together_perallele_odeplot_(100,0.6,1,1,1,0.4,1);
% subplot(122);
% cifAB_together_perallele_plot(100,0.6,1,1,1,0.4,1);

%%%%%%%%%  NOT PER-ALLELE. NAMES CAN BE DECEIVING
function [generation_list,allele_frequency,carrier_frequency] = cifAB_together_perallele_odeplot_(generations,intro,fitness,ea,eb,dom,drawplot)
    I = intro;
    F = fitness;
    y0 = [I;0;1-I];
    
        function dy = odecalc(t,y)
            [dd,wd,ww] = deal(y(1),y(2),y(3));
            N = dd + wd + ww;
        
            mwd = ea * eb; %male wd genotype, drive(toxin) works, 1
            mdd = (2*ea-ea^2) * (2*eb-eb^2); %male dd genotype, drive(toxin) works, 1
            fwd = 1-ea; %female wd genotype, drive(antidote) doesn't work, 0
            fdd = (1-ea)^2; %female dd genotype, drive(antidote) doesn't work, 0
        
            rdd = dd^2 * (1-mdd*fdd) +...
                1/2 * dd * wd * (2-mdd*fwd-mwd*fdd) +...
                1/4  * wd^2 * (1-mwd*fwd);
            
            rwd = 1/2 * wd^2 * (1-mwd*fwd) +...
                1/2 * wd * dd * (2-mwd*fdd-mdd*fwd) +...
                1/2 * ww * wd * (2-mwd) +...
                ww * dd * (2-mdd);
            
            rww = ww^2 +...
                1/2 * ww * wd * (2-mwd) +...
                1/4 * wd^2 * (1-mwd*fwd);
        
            d_dd = F * rdd *9/(8*N+1)/ N-  dd * N;    
            d_wd = (F*dom+1-dom) * rwd *9/(8*N+1)/ N - wd * N;
            d_ww = rww *9/(8*N+1)/ N -  ww * N;
            dy = [d_dd;d_wd;d_ww];
        end
    
    if isequal(size(generations),[1,1])
        [T,Y] = ode45(@odecalc,1:generations,y0);
    else 
        [T,Y] = ode45(@odecalc,generations,y0);
    end    
    
    % size(Y) = [GENERATIONS 3]
    subpop_size = sum(Y,2);
    Y(:,1) = Y(:,1) ./ subpop_size;
    Y(:,2) = Y(:,2) ./ subpop_size;
    Y(:,3) = Y(:,3) ./ subpop_size;
    
    generation_list = T';
    allele_frequency = (Y(:,1) + 1/2 * Y(:,2))';
    carrier_frequency = (Y(:,1) + Y(:,2))';
    
    if (drawplot == 1)
        plot(generation_list, allele_frequency, generation_list, carrier_frequency);
        legend('allele', 'carrier');
    end
end
