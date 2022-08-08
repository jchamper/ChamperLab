clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots');
if exist(['tempdata' name '.mat'],'file') == 0
    min_protection_frequency = 0.8;
    num_points = 500;
    GENERATIONS = 300;
    
    fitness_x = linspace(0.6,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    intro_y = linspace(0.3,0.8,num_points);
    y_min = intro_y(1);
    y_max = intro_y(length(intro_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(intro_y);
    WINDOW = 100; %protection window 100 generations
    [average_a_al,average_b_al,average_a_ca,average_b_ca,max_alfreq, max_algen, max_cafreq, max_cagen,protection_time] = deal(zeros(s));
    %protection time: time cifB is above threshold
    for intro = intro_y
        intro
        for f = fitness_x
            [gen,a_al,b_al,a_ca,b_ca] = same_loci_heterozygotes_odeplot([0,GENERATIONS],intro,f,0);
            average_a_al(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),a_al(gen<=WINDOW))/WINDOW;
            average_b_al(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),b_al(gen<=WINDOW))/WINDOW;
            average_a_ca(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),a_ca(gen<=WINDOW))/WINDOW;
            average_b_ca(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),b_ca(gen<=WINDOW))/WINDOW;
            [maxal,maxalgen] = findmax(a_al);
            [maxca,maxcagen] = findmax(a_ca);
            max_alfreq(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = maxal;
            max_algen(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = maxalgen;
            max_cafreq(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = maxca;
            max_cagen(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = maxcagen;      
            protection_time(round((intro-y_min)/y_interval+1), round((f-x_min)/x_interval+1)) = trapz(gen,a_ca>=min_protection_frequency);
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

protection_time(protection_time==0) = nan;
heatmap_plotter('09 average cifA allele',fitness_x,intro_y,average_a_al,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('09 average cifB allele',fitness_x,intro_y,average_b_al,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('09 average cifA carrier',fitness_x,intro_y,average_a_ca,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('09 average cifB carrier',fitness_x,intro_y,average_b_ca,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,1],false);
heatmap_plotter('09 max cifA allele frequency', fitness_x,intro_y,max_alfreq,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0.3,1],false,2);
heatmap_plotter('09 max cifA allele generation', fitness_x,intro_y,max_algen,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,300],false,3);
heatmap_plotter('09 max cifA carrier frequency', fitness_x,intro_y,max_cafreq,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0.3,1],false,2);
heatmap_plotter('09 max cifA carrier generation', fitness_x,intro_y,max_cagen,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,300],false,3);
heatmap_plotter('09 cifA protection time', fitness_x,intro_y,protection_time,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,300],false,1,0);

%colormap
heatmap_plotter('colorbar_max_freq', fitness_x,intro_y,max_cafreq,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0.3,1],true,2);
heatmap_plotter('colorbar_max_freq_generation', fitness_x,intro_y,max_cagen,'CifA homozygote fitness','Introduction frequency',5,2,6,2,[0,300],true,3);

