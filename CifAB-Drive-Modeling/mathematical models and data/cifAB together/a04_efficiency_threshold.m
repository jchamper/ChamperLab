clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots');
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 1000;
    criterion = 0.7;
    num_points = 500;
    precision = 2048;

    threshold = ones(num_points);
    xy = linspace(0.2,1,num_points);
    x_min = xy(1); y_min = x_min;
    x_max = xy(length(xy)); y_max = x_max;
    x_interval = (x_max-x_min)/(num_points-1); y_interval = x_interval;
    intro_list = linspace(0,1,precision);
    
    for ea = xy
        ea
        for eb = xy
            lo = 1; hi = length(intro_list);
            while lo < hi
                mid = lo + floor((hi-lo) / 2);
                [~,~,carrier] = cifAB_together_odeplot(linspace(0,GENERATIONS,3),intro_list(mid),1,ea,eb,0);
                if carrier(end) > criterion
                    hi = mid;
                else
                    lo = mid+1;
                end
            end
            threshold(round((eb-y_min)/y_interval+1), round((ea-x_min)/x_interval+1)) = intro_list(lo);

        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
threshold(threshold==1) = nan;
heatmap_plotter('04 threshold',xy,xy,threshold,'Toxin efficiency','Antidote efficiency',5,2,5,2,[1,0.3],false,1,0);