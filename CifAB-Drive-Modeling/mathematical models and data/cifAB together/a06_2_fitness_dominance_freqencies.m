clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots')
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 300;
    criterion = 0.7;
    num_points = 500;
    INTRO = 0.6;
    fitness_x = linspace(0.6,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    coeff_y = linspace(0,1,num_points);
    y_min = coeff_y(1);
    y_max = coeff_y(length(coeff_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(coeff_y);
    [avg_allele, avg_carrier, generation] = deal(zeros(s));
    WINDOW = 100; %protection window 100 generations
    
    for f = fitness_x
        f
        for c = coeff_y
            [gen,allele,carrier] = cifAB_together_perallele_odeplot([0,GENERATIONS],INTRO,f,1,1,c,0);        
            if (carrier(length(carrier)) > criterion)
                generation(round((c-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = gen(find(carrier>criterion,1,'first'));
            else
                generation(round((c-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = GENERATIONS;
            end
            avg_allele(round((c-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<WINDOW),allele(gen<WINDOW))/WINDOW;
            avg_carrier(round((c-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<WINDOW),carrier(gen<WINDOW))/WINDOW;
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
crit = 30;
generation(generation > crit) = nan;
heatmap_plotter('06 allele',fitness_x,coeff_y,avg_allele,'Drive homozygote fitness','Dominance coefficient',5,2,6,2,[0,1],false);
heatmap_plotter('06 carrier',fitness_x,coeff_y,avg_carrier,'Drive homozygote fitness','Dominance coefficient',5,2,6,2,[0,1],false);
heatmap_plotter('06 generation',fitness_x,coeff_y,generation, 'Drive homozygote fitness','Dominance coefficient',5,2,6,2,[crit,0],false,0,0);

            
        