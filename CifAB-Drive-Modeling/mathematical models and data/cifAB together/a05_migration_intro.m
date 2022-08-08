clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../plots')
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 300;
    WINDOW = 100; %protection window 100 generations
    criterion = 0.7;
    FITNESS = 0.95; %homozygote fitness is 0.95. 
    num_points = 500;
    
    migration_x = linspace(0.01,0.1,num_points);
    x_min = migration_x(1);
    x_max = migration_x(length(migration_x));
    x_interval = (x_max-x_min)/(num_points-1);
    intro_y = linspace(0.3,0.8,num_points);
    y_min = intro_y(1);
    y_max = intro_y(length(intro_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(intro_y);
    [avg_al_intro, avg_ca_intro, avg_al_linked, avg_ca_linked, gen_intro, gen_linked] = deal(zeros(num_points));
    
    for intro = intro_y
        intro
        for mig = migration_x
            [gen,al_intro,ca_intro,al_linked,ca_linked] = migration_odeplot([0,GENERATIONS],FITNESS,intro,mig,0);
            avg_al_intro(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),al_intro(gen<=WINDOW))/WINDOW;
            avg_ca_intro(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),ca_intro(gen<=WINDOW))/WINDOW;
            avg_al_linked(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),al_linked(gen<=WINDOW))/WINDOW;
            avg_ca_linked(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),ca_linked(gen<=WINDOW))/WINDOW;
            
            if (ca_intro(length(ca_intro)) > criterion)
                gen_intro(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = gen(find(ca_intro>criterion,1,'first'));
            else
                gen_intro(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = GENERATIONS;
            end
    
            if (ca_linked(length(ca_linked)) > criterion)
                gen_linked(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = gen(find(ca_linked>criterion,1,'first'));
            else
                gen_linked(round((intro-y_min)/y_interval+1), round((mig-x_min)/x_interval+1)) = GENERATIONS;
            end
        end
    end  
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

crit = 50;
gen_intro(gen_intro>=crit) = nan;
gen_linked(gen_linked>=crit) = nan;
nancolor = '#a4aca7';
heatmap_plotter('05 introduction deme allele frequency',migration_x,intro_y,avg_al_intro,'Migration rate','Introduction frequency',4,2,6,2,[0,1],false);
heatmap_plotter('05 introduction deme carrier frequency',migration_x,intro_y,avg_ca_intro,'Migration rate','Introduction frequency',4,2,6,2,[0,1],false);
heatmap_plotter('05 linked deme allele frequency',migration_x,intro_y,avg_al_linked,'Migration rate','Introduction frequency',4,2,6,2,[0,1],false);
heatmap_plotter('05 linked deme carrier frequency',migration_x,intro_y,avg_ca_linked,'Migration rate','Introduction frequency',4,2,6,2,[0,1],false);
heatmap_plotter('05 introduction deme fixed generation',migration_x,intro_y,gen_intro,'Migration rate','Introduction frequency',4,2,6,2,[crit,0],false,0,nancolor);
heatmap_plotter('05 linked deme fixed generation',migration_x,intro_y,gen_linked,'Migration rate','Introduction frequency',4,2,6,2,[crit,0],false,0,nancolor);
heatmap_plotter('colorbar_migration_generation',migration_x,intro_y,gen_linked,'Migration rate','Introduction frequency',4,2,6,2,[crit,0],true,0,nancolor);

