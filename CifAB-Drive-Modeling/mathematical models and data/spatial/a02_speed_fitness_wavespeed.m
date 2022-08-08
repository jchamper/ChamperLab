clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    num_points = 200;
    fitness_x = linspace(0.9,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    dispersion_y = linspace(0.01,0.1,num_points);
    y_min = dispersion_y(1);
    y_max = dispersion_y(length(dispersion_y));
    y_interval = (y_max-y_min)/(num_points-1);
    wavespeed = zeros(num_points);
    
    for fitness = fitness_x
        fitness %homozygote fitness
        for dispersion = dispersion_y
            w = wave_speed(dispersion,fitness,0);
            wavespeed(round((dispersion-y_min)/y_interval+1),round((fitness-x_min)/x_interval+1)) = w;
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

minvalue = min(min(wavespeed));
maxvalue = max(max(wavespeed));
colormap_ = colormap('cool');
close;
wavespeed(wavespeed==0) = nan;
min(wavespeed(wavespeed>0))
heatmap_plotter('spatial02 dispersion fitness wavespeed', fitness_x, dispersion_y, wavespeed,'Drive homozygote fitness', 'Dispersion',4,2,5,2,[0,8e-3],false,colormap_,0);