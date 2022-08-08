clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots');
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 1000;
    criterion = 0.7;
    num_points = 500;
    
    efficiency_x = linspace(0.2,1,num_points);
    x_min = efficiency_x(1);
    x_max = efficiency_x(length(efficiency_x));
    x_interval = (x_max-x_min)/(num_points-1);
    
    intro_y = linspace(0.3,0.8,num_points);
    y_min = intro_y(1);
    y_max = intro_y(length(intro_y));
    y_interval = (y_max-y_min)/(num_points-1);
    threshold = ones(1,num_points);
    
    [eq_allele, eq_carrier] = deal(zeros(num_points));
    for ea = efficiency_x
        ea
        for intro = intro_y
            [gen,allele,carrier] = cifAB_together_odeplot(linspace(0,GENERATIONS,3),intro,1,ea,ea,0);
            %find threshold
            if (carrier(length(carrier)) > criterion & threshold(round((ea-x_min)/x_interval+1)) == 1)
                threshold(round((ea-x_min)/x_interval+1)) = intro;
            end
            eq_allele(round((intro-y_min)/y_interval+1), round((ea-x_min)/x_interval+1)) = allele(length(allele));
            eq_carrier(round((intro-y_min)/y_interval+1), round((ea-x_min)/x_interval+1)) = carrier(length(carrier));
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

%find first point where threshold <1
idx = find(threshold<1,1);
efficiency_x(idx)


line_plotter('03 efficiency threshold',efficiency_x,threshold,'Drive efficiency','Introduction threshold');
heatmap_plotter('03 equilibrium allele frequency',efficiency_x,intro_y,eq_allele,'Drive efficiency','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('03 equilibrium carrier frequency',efficiency_x,intro_y,eq_carrier,'Drive efficiency','Introduction frequency',5,2,6,2,[0,1],false);