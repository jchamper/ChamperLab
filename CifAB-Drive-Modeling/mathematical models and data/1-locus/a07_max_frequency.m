clc;clear;close all;
[path,name]=fileparts(mfilename('fullpath'));
addpath('../../plots/')
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 300;
    A_FITNESS = 0.95; %homozygote cifA is 0.95 fitness
    WINDOW = 100;
    num_points = 500;
    min_protection_frequency = 0.8;
    
    afreq_x = linspace(0.3,0.8,num_points);
    x_min = afreq_x(1);
    x_max = afreq_x(length(afreq_x));
    x_interval = (x_max-x_min)/(num_points-1);
    bfreq_y = linspace(0,0.6,num_points);
    y_min = bfreq_y(1);
    y_max = bfreq_y(length(bfreq_y));
    y_interval = (y_max-y_min)/(num_points-1);
    s = length(bfreq_y);
    [max_alfreq,max_algen,max_cafreq,max_cagen,avg_allele,avg_carrier,protection_time] = deal(nan(s));
    for a = afreq_x
        a
        for b = bfreq_y
            if (a+b>1)
                break
            else
                [gen,a_al,~,a_ca,~] = same_loci_double_homozygotes_odeplot([0,GENERATIONS],a,b,A_FITNESS,0);
                [maxal,maxalgen] = findmax(a_al);
                [maxca,maxcagen] = findmax(a_ca);
                max_alfreq(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = maxal;
                max_algen(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = maxalgen;
                max_cafreq(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = maxca;
                max_cagen(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = maxcagen;
                avg_allele(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),a_al(gen<=WINDOW))/WINDOW;
                avg_carrier(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = trapz(gen(gen<=WINDOW),a_ca(gen<=WINDOW))/WINDOW;
                protection_time(round((b-y_min)/y_interval+1), round((a-x_min)/x_interval+1)) = trapz(gen,a_ca>=min_protection_frequency);
            end
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
colormap_ = colormap('parula');






close;
heatmap_plotter('07 max allele frequency',afreq_x,bfreq_y,max_alfreq,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0.3,1],false,2,'w');
heatmap_plotter('07 max allele generation',afreq_x,bfreq_y,max_algen,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,300],false,3,'w');
heatmap_plotter('07 max carrier frequency',afreq_x,bfreq_y,max_cafreq,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0.3,1],false,2,'w');
heatmap_plotter('07 max carrier generation',afreq_x,bfreq_y,max_cagen,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,300],false,3,'w');
heatmap_plotter('07 average allele frequency in gen 1-100',afreq_x,bfreq_y,avg_allele,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,1],false,colormap_,'w');
heatmap_plotter('07 average carrier frequency in gen 1-100',afreq_x,bfreq_y,avg_carrier,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,1],false,colormap_,'w');
colormap_(1,:) = [164,172,167]/255;
heatmap_plotter('07 cifA protection time',afreq_x,bfreq_y,protection_time,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,300],false,colormap_,'w');
heatmap_plotter('colormap_protection_time',afreq_x,bfreq_y,protection_time,'CifA introduction frequency','CifB introduction frequency',6,2,7,2,[0,300],true,1,0);
