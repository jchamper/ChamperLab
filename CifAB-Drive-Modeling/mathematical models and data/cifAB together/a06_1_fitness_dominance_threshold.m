clc;clear;close all;
[~,name]=fileparts(mfilename('fullpath'));
addpath('../../plots')
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 1000;    
    criterion = 0.7;
    num_points = 41;
    precision = 512;
    
    fitness_x = linspace(0.6,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    coeff_y = linspace(0,1,num_points);
    y_min = coeff_y(1);
    y_max = coeff_y(length(coeff_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(coeff_y);
    intro_list = linspace(0,1,precision);
    
    threshold = ones(s);
    for f = fitness_x
        f
        for c = coeff_y
            %bisect
            lo = 1; hi = length(intro_list);
            while lo < hi
                mid = lo + floor((hi-lo) / 2);
                [~,~,carrier] = cifAB_together_perallele_odeplot([0,GENERATIONS],intro_list(mid),f,1,1,c,0);        
                if carrier(end) > criterion
                    hi = mid;
                else
                    lo = mid+1;
                end
            end
            threshold(round((c-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = intro_list(lo);
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
threshold(threshold==1) = nan;
heatmap_plotter('06 threshold',fitness_x,coeff_y,threshold,'Drive homozygote fitness','Dominance coefficient',5,2,6,2,[1.01,0.29],false,1,0);
%min(min(threshold)) is 0.3607