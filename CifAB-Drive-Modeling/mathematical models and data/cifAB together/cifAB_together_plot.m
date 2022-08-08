cifAB_together_plot_([0,100],0.36455,1,1,1,1);
function [generation_list,allele_frequency,carrier_frequency] = cifAB_together_plot_(generations,intro,fitness,et,er,drawplot)
    %If it's 1*1, generate discrete time
    %format long;
    I = intro;
    F = sqrt(fitness);
    dd = I;wd = 0;ww = 1-I;

    function [ndd,nwd,nww] = odecalc(dd,wd,ww)
        dd = dd*F^2;
        wd = wd*F;
        mwd = et; %male wd genotype, drive(toxin) works, 1
        mdd = 1-(1-et)^2; %male dd genotype, drive(toxin) works, 1
        fwd = 1-er; %female wd genotype, drive(antidote) doesn't work, 0
        fdd = (1-er)^2; %female dd genotype, drive(antidote) doesn't work, 0
        ndd = dd^2 * (1-mdd*fdd) +...
            1/2 * dd * wd * (2-mdd*fwd-mwd*fdd) +...
            1/4  * wd^2 * (1-mwd*fwd);
        
        nwd = 1/2 * wd^2 * (1-mwd*fwd) +...
            1/2 * wd * dd * (2-mwd*fdd-mdd*fwd) +...
            1/2 * ww * wd * (2-mwd) +...
            ww * dd * (2-mdd);
        
        nww = ww^2 +...
            1/2 * ww * wd * (2-mwd) +...
            1/4 * wd^2 * (1-mwd*fwd);
        N = ndd + nwd + nww;
        ndd = ndd/N;
        nwd = nwd/N;
        nww = nww/N;
    end

    generation_list = generations(1):generations(2);
    [allele_frequency,carrier_frequency] = deal(zeros(1,(length(generation_list))));
    for t = 1:length(generation_list)
        allele_frequency(t) = dd+1/2*wd;
        carrier_frequency(t) = dd + wd;
        [dd,wd,ww] = odecalc(dd,wd,ww);
    end
    if (drawplot == 1)
        figure;
        plot(generation_list, allele_frequency, generation_list, carrier_frequency,"LineWidth",2);
        legend('allele', 'carrier');
    end
end
