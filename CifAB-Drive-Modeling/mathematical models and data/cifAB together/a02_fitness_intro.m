%collect:average in generations 1-100 (10 years)  (through integral calculation), fixed generation
clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots');
if exist(['tempdata' name '.mat'],'file') == 0
    criterion = 0.7;
    num_points = 500;
    GENERATIONS = 1000;    
    fitness_x = linspace(0.6,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    intro_y = linspace(0.3,0.8,num_points);
    y_min = intro_y(1);
    y_max = intro_y(length(intro_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(intro_y);
    [avg_allele,avg_carrier,fixed_gen,eq_allele,eq_carrier] = deal(zeros(s));
    WINDOW = 100; %protection window 100 generations
    
    for fitness = fitness_x
        fitness
        for intro = intro_y
            [generations,allele,carrier] = cifAB_together_odeplot([0,GENERATIONS],intro,fitness,1,1,0);
            if (carrier(length(carrier)) > criterion)
                fixed_gen(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = generations(find(carrier>criterion,1,'first'));
            else 
                fixed_gen(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = GENERATIONS;
            end    
            eq_allele(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = allele(GENERATIONS);
            eq_carrier(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = carrier(GENERATIONS);
            avg_allele(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = trapz(generations(generations<WINDOW),allele(generations<WINDOW))/WINDOW;
            avg_carrier(round((intro-y_min)/y_interval+1), round((fitness-x_min)/x_interval+1)) = trapz(generations(generations<WINDOW),carrier(generations<WINDOW))/WINDOW;
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
crit = 20;
fixed_gen(fixed_gen>=crit) = nan;
eq_allele(eq_allele<=1e-4) = nan;
eq_carrier(eq_carrier<=1e-3) = nan;
nancolor = '#a4aca7';
heatmap_plotter('02 average allele in generations 1-100',fitness_x,intro_y,avg_allele,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('02 average carrier in generations 1-100',fitness_x,intro_y,avg_carrier,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('02 fixed generation',fitness_x,intro_y,fixed_gen,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[crit,0],false,0,nancolor);
heatmap_plotter('02 equilibrium allele frequency',fitness_x,intro_y,eq_allele,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[0,1],true,1,nancolor);
heatmap_plotter('02 equilibrium carrier frequency',fitness_x,intro_y,eq_carrier,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false,1,nancolor);

%%for plotting colorbars
heatmap_plotter('02 average allele in generations 1-100',fitness_x,intro_y,avg_allele,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[0,1],true);
heatmap_plotter('colorbar_fixed_generation',fitness_x,intro_y,fixed_gen,'Drive homozygote fitness','Introduction frequency',5,2,6,2,[crit,0],true,0,nancolor);
