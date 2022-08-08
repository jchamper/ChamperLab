% same_loci_heterozygotes_odeplot_(100,0.8,1,1);
% same_loci_heterozygotes_plot(100,0.8,1,1);
function [generation_list,cifa_allele,cifb_allele,cifa_carrier,cifb_carrier] = same_loci_heterozygotes_odeplot_(generations,I,F,drawplot)
    format long;
    F = sqrt(F);
    y0 = [1-I;0;0;0;0;I];
    %ww,wa,wb,aa,bb,ab
    function dy = same_loci_odecalc(t,y)
        [ww,wa,wb,aa,bb,ab] = deal(y(1),y(2),y(3),y(4),y(5),y(6));
        N = ww + wa + wb + aa + bb + ab;
        mat = [1,0,0,0,0,0 %ww ww
            0.5 0.5 0 0 0 0 %ww wa
            0.5 0 0.5 0 0 0 %ww wb
            0 1 0 0 0 0 %ww aa
            0 0 0 0 0 0 %ww ab
            0 0 1 0 0 0 %ww bb
            0.5 0.5 0 0 0 0 %wa ww
            0.25 0.5 0 0.25 0 0 %wa wa
            0.25 0.25 0.25 0 0.25 0 %wa wb
            0 0.5 0 0.5 0 0 %wa aa
            0 0.25 0.25 0.25 0.25 0 %wa ab
            0 0 0.5 0 0.5 0 %wa bb
            0.5 0 0.5 0 0 0 %wb ww
            0.25 0.25 0.25 0 0.25 0 %wb wa
            0.25 0 0.5 0 0 0.25 %wb wb
            0 0.5 0 0 0.5 0 %wb aa
            0 0 0 0 0 0 %wb ab
            0 0 0.5 0 0 0.5 %wb bb
            0 1 0 0 0 0 %aa ww
            0 0.5 0 0.5 0 0 %aa wa
            0 0.5 0 0 0.5 0 %aa wb
            0 0 0 1 0 0 %aa aa
            0 0 0 0.5 0.5 0 %aa ab
            0 0 0 0 1 0 %aa bb
            0 0.5 0.5 0 0 0 %ab ww
            0 0.25 0.25 0.25 0.25 0 %ab wa
            0 0.25 0.25 0 0.25 0.25 %ab wb
            0 0 0 0.5 0.5 0 %ab aa
            0 0 0 0.25 0.5 0.25 %ab ab
            0 0 0 0 0.5 0.5 %ab bb
            0 0 1 0 0 0 %bb ww
            0 0 0.5 0 0.5 0 %bb wa
            0 0 0.5 0 0 0.5 %bb wb
            0 0 0 0 1 0 %bb aa
            0 0 0 0 0 0 %bb ab
            0 0 0 0 0 1]; %bb bb
            
        function anss = calc(col)
            anss = ww * ww * mat(1,col) + ww * wa * mat(2,col) + ww * wb * mat(3,col) + ww * aa * mat(4,col) + ww * ab * mat(5,col) + ww * bb * mat(6,col) + wa * ww * mat(7,col) + wa * wa * mat(8,col) + wa * wb * mat(9,col) + wa * aa * mat(10,col) + wa * ab * mat(11,col) + wa * bb * mat(12,col) + wb * ww * mat(13,col) + wb * wa * mat(14,col) + wb * wb * mat(15,col) + wb * aa * mat(16,col) + wb * ab * mat(17,col) + wb * bb * mat(18,col) + aa * ww * mat(19,col) + aa * wa * mat(20,col) + aa * wb * mat(21,col) + aa * aa * mat(22,col) + aa * ab * mat(23,col) + aa * bb * mat(24,col) + ab * ww * mat(25,col) + ab * wa * mat(26,col) + ab * wb * mat(27,col) + ab * aa * mat(28,col) + ab * ab * mat(29,col) + ab * bb * mat(30,col) + bb * ww * mat(31,col) + bb * wa * mat(32,col) + bb * wb * mat(33,col) + bb * aa * mat(34,col) + bb * ab * mat(35,col) + bb * bb * mat(36,col);            
        end
        
        rww = calc(1);
        rwa = calc(2);
        rwb = calc(3);
        raa = calc(4);
        rab = calc(5);
        rbb = calc(6);
        
        d_ww = rww *9/(8*N+1) / N- ww * N;
        d_wa = F * rwa *9/(8*N+1) / N - wa * N;
        d_wb = rwb *9/(8*N+1) / N - wb * N;
        d_aa = F^2 * raa *9/(8*N+1) / N - aa * N;
        d_ab = F * rab *9/(8*N+1) / N - ab * N;
        d_bb = rbb *9/(8*N+1) / N - bb * N;
        dy = [d_ww;d_wa;d_wb;d_aa;d_bb;d_ab];
    end
    if isequal(size(generations),[1,1])
        [T,Y] = ode45(@same_loci_odecalc,1:generations,y0);
    else 
        if isequal(size(generations),[1,2])
            [T,Y] = ode45(@same_loci_odecalc,generations,y0);
        end
    end
    subpop_size = sum(Y,2);
    for i = 1:6
        Y(:,i) = Y(:,i) ./ subpop_size;
    end
    generation_list = T';

    cifa_allele = (Y(:,4) + 1/2 * Y(:,2) + 1/2 * Y(:,6))';
    cifb_allele = (Y(:,5) + 1/2 * Y(:,3) + 1/2 * Y(:,6))';
    cifa_carrier = (Y(:,4) + Y(:,2) + Y(:,6))';
    cifb_carrier = (Y(:,5) + Y(:,3) + Y(:,6))';

if (drawplot == 1)
subplot(121);
plot(generation_list, cifa_allele, generation_list, cifa_carrier);
legend('cifa allele','cifa carrier');
subplot(122);
plot(generation_list, cifb_allele, generation_list, cifb_carrier);
legend('cifb allele', 'cifb carrier');
end
end