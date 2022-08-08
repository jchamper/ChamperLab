clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    num_points = 200;
    efficiency_x = linspace(0.7,1,num_points);
    x_min = efficiency_x(1);
    x_max = efficiency_x(length(efficiency_x));
    x_interval = (x_max-x_min)/(num_points-1);
    dispersion_y = linspace(0.01,0.1,num_points);
    y_min = dispersion_y(1);
    y_max = dispersion_y(length(dispersion_y));
    y_interval = (y_max-y_min)/(num_points-1);
    wavespeed = zeros(num_points);
    
    for efficiency = efficiency_x
        efficiency %homozygote fitness
        for dispersion = dispersion_y
            w = wave_speed(dispersion,1,0,efficiency);
            wavespeed(round((dispersion-y_min)/y_interval+1),round((efficiency-x_min)/x_interval+1)) = w;
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
heatmap_plotter('spatial06 dispersion efficiency wavespeed', efficiency_x, dispersion_y, wavespeed,'Drive efficiency', 'Dispersion',4,2,4,2,[0,8e-3],false,colormap_,0);