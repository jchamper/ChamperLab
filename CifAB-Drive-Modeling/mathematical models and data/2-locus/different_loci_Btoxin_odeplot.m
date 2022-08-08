% 
% different_loci_Btoxin_odeplot_(100,0.78,0.94,1);
% figure;
% different_loci_Btoxin_plot(100,0.78,0.94,1);

function [generation_list,cifa_allele,cifb_allele,cifa_carrier,cifb_carrier] = different_loci_Btoxin_odeplot_(gen,I,F,drawplot)
    %w1w1w2w2,w1w1bw2,w1w1bb,aw1w2w2,aw1bw2,aw1bb,aaw2w2,aabw2,aabb
    y0 = [1-I;0;0;0;0;0;0;0;I];
    F = sqrt(F);
    function dy = odecalc(t,y)
        [w1w1w2w2,w1w1bw2,w1w1bb,aw1w2w2,aw1bw2,aw1bb,aaw2w2,aabw2,aabb] = deal(y(1),y(2),y(3),y(4),y(5),y(6),y(7),y(8),y(9));
        N = w1w1w2w2+w1w1bw2+w1w1bb+aw1w2w2+aw1bw2+aw1bb+aaw2w2+aabw2+aabb;
        %w1w1w2w2 w1w1bw2 w1w1bb aw1w2w2 aw1bw2 aw1bb aaw2w2 aabw2 aabb   male female
    mat = [1.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1w2w2 w1w1w2w2
        0.500 0.500 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1w2w2 w1w1bw2
        0.000 1.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1w2w2 w1w1bb
        0.500 0.000 0.000 0.500 0.000 0.000 0.000 0.000 0.000 %w1w1w2w2 aw1w2w2
        0.250 0.250 0.000 0.250 0.250 0.000 0.000 0.000 0.000 %w1w1w2w2 aw1bw2
        0.000 0.500 0.000 0.000 0.500 0.000 0.000 0.000 0.000 %w1w1w2w2 aw1bb
        0.000 0.000 0.000 1.000 0.000 0.000 0.000 0.000 0.000 %w1w1w2w2 aaw2w2
        0.000 0.000 0.000 0.500 0.500 0.000 0.000 0.000 0.000 %w1w1w2w2 aabw2
        0.000 0.000 0.000 0.000 1.000 0.000 0.000 0.000 0.000 %w1w1w2w2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bw2 w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bw2 w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bw2 w1w1bb----
        0.250 0.250 0.000 0.250 0.250 0.000 0.000 0.000 0.000 %w1w1bw2 aw1w2w2
        0.125 0.250 0.125 0.125 0.250 0.125 0.000 0.000 0.000 %w1w1bw2 aw1bw2
        0.000 0.250 0.250 0.000 0.250 0.250 0.000 0.000 0.000 %w1w1bw2 aw1bb
        0.000 0.000 0.000 0.500 0.500 0.000 0.000 0.000 0.000 %w1w1bw2 aaw2w2
        0.000 0.000 0.000 0.250 0.500 0.250 0.000 0.000 0.000 %w1w1bw2 aabw2
        0.000 0.000 0.000 0.000 0.500 0.500 0.000 0.000 0.000 %w1w1bw2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bb w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bb w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %w1w1bb w1w1bb----
        0.000 0.500 0.000 0.000 0.500 0.000 0.000 0.000 0.000 %w1w1bb aw1w2w2
        0.000 0.250 0.250 0.000 0.250 0.250 0.000 0.000 0.000 %w1w1bb aw1bw2
        0.000 0.000 0.500 0.000 0.000 0.500 0.000 0.000 0.000 %w1w1bb aw1bb
        0.000 0.000 0.000 0.000 1.000 0.000 0.000 0.000 0.000 %w1w1bb aaw2w2
        0.000 0.000 0.000 0.000 0.500 0.500 0.000 0.000 0.000 %w1w1bb aabw2
        0.000 0.000 0.000 0.000 0.000 1.000 0.000 0.000 0.000 %w1w1bb aabb
        0.500 0.000 0.000 0.500 0.000 0.000 0.000 0.000 0.000 %aw1w2w2 w1w1w2w2
        0.250 0.250 0.000 0.250 0.250 0.000 0.000 0.000 0.000 %aw1w2w2 w1w1bw2
        0.000 0.500 0.000 0.000 0.500 0.000 0.000 0.000 0.000 %aw1w2w2 w1w1bb
        0.250 0.000 0.000 0.500 0.000 0.000 0.250 0.000 0.000 %aw1w2w2 aw1w2w2
        0.125 0.125 0.000 0.250 0.250 0.000 0.125 0.125 0.000 %aw1w2w2 aw1bw2
        0.000 0.250 0.000 0.000 0.500 0.000 0.000 0.250 0.000 %aw1w2w2 aw1bb
        0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 0.000 %aw1w2w2 aaw2w2
        0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 0.000 %aw1w2w2 aabw2
        0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 %aw1w2w2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bw2 w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bw2 w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bw2 w1w1bb----
        0.125 0.125 0.000 0.250 0.250 0.000 0.125 0.125 0.000 %aw1bw2 aw1w2w2
        0.062 0.125 0.062 0.125 0.250 0.125 0.062 0.125 0.062 %aw1bw2 aw1bw2
        0.000 0.125 0.125 0.000 0.250 0.250 0.000 0.125 0.125 %aw1bw2 aw1bb
        0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 0.000 %aw1bw2 aaw2w2
        0.000 0.000 0.000 0.125 0.250 0.125 0.125 0.250 0.125 %aw1bw2 aabw2
        0.000 0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 %aw1bw2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bb w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bb w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aw1bb w1w1bb----
        0.000 0.250 0.000 0.000 0.500 0.000 0.000 0.250 0.000 %aw1bb aw1w2w2
        0.000 0.125 0.125 0.000 0.250 0.250 0.000 0.125 0.125 %aw1bb aw1bw2
        0.000 0.000 0.250 0.000 0.000 0.500 0.000 0.000 0.250 %aw1bb aw1bb
        0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 %aw1bb aaw2w2
        0.000 0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 %aw1bb aabw2
        0.000 0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 %aw1bb aabb
        0.000 0.000 0.000 1.000 0.000 0.000 0.000 0.000 0.000 %aaw2w2 w1w1w2w2
        0.000 0.000 0.000 0.500 0.500 0.000 0.000 0.000 0.000 %aaw2w2 w1w1bw2
        0.000 0.000 0.000 0.000 1.000 0.000 0.000 0.000 0.000 %aaw2w2 w1w1bb
        0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 0.000 %aaw2w2 aw1w2w2
        0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 0.000 %aaw2w2 aw1bw2
        0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 %aaw2w2 aw1bb
        0.000 0.000 0.000 0.000 0.000 0.000 1.000 0.000 0.000 %aaw2w2 aaw2w2
        0.000 0.000 0.000 0.000 0.000 0.000 0.500 0.500 0.000 %aaw2w2 aabw2
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 1.000 0.000 %aaw2w2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabw2 w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabw2 w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabw2 w1w1bb----
        0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 0.000 %aabw2 aw1w2w2
        0.000 0.000 0.000 0.125 0.250 0.125 0.125 0.250 0.125 %aabw2 aw1bw2
        0.000 0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 %aabw2 aw1bb
        0.000 0.000 0.000 0.000 0.000 0.000 0.500 0.500 0.000 %aabw2 aaw2w2
        0.000 0.000 0.000 0.000 0.000 0.000 0.250 0.500 0.250 %aabw2 aabw2
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.500 0.500 %aabw2 aabb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabb w1w1w2w2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabb w1w1bw2----
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 %aabb w1w1bb----
        0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 0.000 %aabb aw1w2w2
        0.000 0.000 0.000 0.000 0.250 0.250 0.000 0.250 0.250 %aabb aw1bw2
        0.000 0.000 0.000 0.000 0.000 0.500 0.000 0.000 0.500 %aabb aw1bb
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 1.000 0.000 %aabb aaw2w2
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.500 0.500 %aabb aabw2
        0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 1.000]; %aabb aabb
    
        function anss = calc(col)
            anss = w1w1w2w2 * w1w1w2w2 * mat(1,col)+w1w1w2w2 * w1w1bw2 * mat(2,col)+w1w1w2w2 * w1w1bb * mat(3,col)+w1w1w2w2 * aw1w2w2 * mat(4,col)+w1w1w2w2 * aw1bw2 * mat(5,col)+w1w1w2w2 * aw1bb * mat(6,col)+w1w1w2w2 * aaw2w2 * mat(7,col)+w1w1w2w2 * aabw2 * mat(8,col)+w1w1w2w2 * aabb * mat(9,col)+w1w1bw2 * w1w1w2w2 * mat(10,col)+w1w1bw2 * w1w1bw2 * mat(11,col)+w1w1bw2 * w1w1bb * mat(12,col)+w1w1bw2 * aw1w2w2 * mat(13,col)+w1w1bw2 * aw1bw2 * mat(14,col)+w1w1bw2 * aw1bb * mat(15,col)+w1w1bw2 * aaw2w2 * mat(16,col)+w1w1bw2 * aabw2 * mat(17,col)+w1w1bw2 * aabb * mat(18,col)+w1w1bb * w1w1w2w2 * mat(19,col)+w1w1bb * w1w1bw2 * mat(20,col)+w1w1bb * w1w1bb * mat(21,col)+w1w1bb * aw1w2w2 * mat(22,col)+w1w1bb * aw1bw2 * mat(23,col)+w1w1bb * aw1bb * mat(24,col)+w1w1bb * aaw2w2 * mat(25,col)+w1w1bb * aabw2 * mat(26,col)+w1w1bb * aabb * mat(27,col)+aw1w2w2 * w1w1w2w2 * mat(28,col)+aw1w2w2 * w1w1bw2 * mat(29,col)+aw1w2w2 * w1w1bb * mat(30,col)+aw1w2w2 * aw1w2w2 * mat(31,col)+aw1w2w2 * aw1bw2 * mat(32,col)+aw1w2w2 * aw1bb * mat(33,col)+aw1w2w2 * aaw2w2 * mat(34,col)+aw1w2w2 * aabw2 * mat(35,col)+aw1w2w2 * aabb * mat(36,col)+aw1bw2 * w1w1w2w2 * mat(37,col)+aw1bw2 * w1w1bw2 * mat(38,col)+aw1bw2 * w1w1bb * mat(39,col)+aw1bw2 * aw1w2w2 * mat(40,col)+aw1bw2 * aw1bw2 * mat(41,col)+aw1bw2 * aw1bb * mat(42,col)+aw1bw2 * aaw2w2 * mat(43,col)+aw1bw2 * aabw2 * mat(44,col)+aw1bw2 * aabb * mat(45,col)+aw1bb * w1w1w2w2 * mat(46,col)+aw1bb * w1w1bw2 * mat(47,col)+aw1bb * w1w1bb * mat(48,col)+aw1bb * aw1w2w2 * mat(49,col)+aw1bb * aw1bw2 * mat(50,col)+aw1bb * aw1bb * mat(51,col)+aw1bb * aaw2w2 * mat(52,col)+aw1bb * aabw2 * mat(53,col)+aw1bb * aabb * mat(54,col)+aaw2w2 * w1w1w2w2 * mat(55,col)+aaw2w2 * w1w1bw2 * mat(56,col)+aaw2w2 * w1w1bb * mat(57,col)+aaw2w2 * aw1w2w2 * mat(58,col)+aaw2w2 * aw1bw2 * mat(59,col)+aaw2w2 * aw1bb * mat(60,col)+aaw2w2 * aaw2w2 * mat(61,col)+aaw2w2 * aabw2 * mat(62,col)+aaw2w2 * aabb * mat(63,col)+aabw2 * w1w1w2w2 * mat(64,col)+aabw2 * w1w1bw2 * mat(65,col)+aabw2 * w1w1bb * mat(66,col)+aabw2 * aw1w2w2 * mat(67,col)+aabw2 * aw1bw2 * mat(68,col)+aabw2 * aw1bb * mat(69,col)+aabw2 * aaw2w2 * mat(70,col)+aabw2 * aabw2 * mat(71,col)+aabw2 * aabb * mat(72,col)+aabb * w1w1w2w2 * mat(73,col)+aabb * w1w1bw2 * mat(74,col)+aabb * w1w1bb * mat(75,col)+aabb * aw1w2w2 * mat(76,col)+aabb * aw1bw2 * mat(77,col)+aabb * aw1bb * mat(78,col)+aabb * aaw2w2 * mat(79,col)+aabb * aabw2 * mat(80,col)+aabb * aabb * mat(81,col);
        end

        rw1w1w2w2 = calc(1);
        rw1w1bw2 = calc(2);
        rw1w1bb = calc(3);
        raw1w2w2 = calc(4);
        raw1bw2 = calc(5);
        raw1bb = calc(6);
        raaw2w2 = calc(7);
        raabw2 = calc(8);
        raabb = calc(9);
     
        d_w1w1w2w2 = rw1w1w2w2 *9/(8*N+1)/N - w1w1w2w2 * N;
        d_w1w1bw2 = rw1w1bw2 *9/(8*N+1)/N - w1w1bw2 * N;
        d_w1w1bb = rw1w1bb *9/(8*N+1)/N - w1w1bb * N;
        d_aw1w2w2 = F*raw1w2w2 *9/(8*N+1)/N - aw1w2w2 * N;
        d_aw1bw2 = F*raw1bw2 *9/(8*N+1)/N - aw1bw2 * N;
        d_aw1bb = F*raw1bb *9/(8*N+1)/N - aw1bb * N;
        d_aaw2w2 = F^2*raaw2w2 *9/(8*N+1)/N - aaw2w2 * N;
        d_aabw2 = F^2*raabw2 *9/(8*N+1)/N - aabw2 * N;
        d_aabb = F^2*raabb *9/(8*N+1)/N - aabb * N;
        dy = [d_w1w1w2w2;d_w1w1bw2;d_w1w1bb;d_aw1w2w2;d_aw1bw2;d_aw1bb;d_aaw2w2;d_aabw2;d_aabb];
    end
    if isequal(size(gen),[1,1])
        [T,Y] = ode45(@odecalc,1:gen,y0);
    else
        [T,Y] = ode45(@odecalc,gen,y0);
    end
    subpop_size = sum(Y,2);
    for i = 1:9
        Y(:,i) = Y(:,i) ./ subpop_size;
    end
    generation_list = T';
    cifa_allele = (1/2*Y(:,4) + 1/2*Y(:,5) + 1/2*Y(:,6) + Y(:,7) + Y(:,8) + Y(:,9))'; %[0,0,0,1/2,1/2,1/2,1,1,1]
    cifb_allele = (1/2*Y(:,2) + 1/2*Y(:,5) + 1/2*Y(:,8) + Y(:,3) + Y(:,6) + Y(:,9))'; %[0,1/2,1,0,1/2,1,0,1/2,1],2)
    cifa_carrier = (Y(:,4) + Y(:,5) + Y(:,6) + Y(:,7) + Y(:,8) + Y(:,9))'; %[0,0,0,1,1,1,1,1,1]
    cifb_carrier = (Y(:,2) + Y(:,5) + Y(:,8) + Y(:,3) + Y(:,6) + Y(:,9))'; %[0,1,1,0,1,1,0,1,1]

    if (drawplot)
    subplot(121);
    plot(generation_list, cifa_allele, generation_list, cifa_carrier);
    legend('cifa allele','cifa carrier');
    subplot(122);
    plot(generation_list, cifb_allele, generation_list, cifb_carrier);
    legend('cifb allele', 'cifb carrier');
    end
end