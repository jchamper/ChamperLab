clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    num_points = 200;
    intro = 0.8;
    precision = 1024;
    fitness_x = linspace(0.9,1,num_points);
    dispersion_y = linspace(0.01,0.04,num_points);
    radius_list = linspace(0.01,0.3,precision);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    y_min = dispersion_y(1);
    y_max = dispersion_y(length(dispersion_y));
    y_interval = (y_max-y_min)/(num_points-1);
    critical_radius = zeros(num_points);

    dx = 0.1;
    radius = 5;
    x = 0:dx:radius;

    for F = fitness_x
        F
        for D = dispersion_y
            lo = 1; hi = length(radius_list);
            while lo < hi
                mid = lo + floor((hi-lo) / 2);
                R = radius_list(mid);
                [dd,wd] = deal(zeros(1,length(x)));
                ww = ones(1,length(x));
                dd(1:round(length(dd)*R*2)) = intro/(1-intro);
                expands = circle_expands(dd,wd,ww,dx,D,F,0);
                if expands
                    hi = mid;
                else
                    lo = mid + 1;
                end
            end
            critical_radius(round((D-y_min)/y_interval+1),round((F-x_min)/x_interval+1)) = radius_list(lo);
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

%transform radius into volume
critical_radius = pi * critical_radius.^2 * intro/(1-intro);
minvalue = 1;
maxvalue = 0;
colormap_ = colormap(othercolor('Accent4')); 
close;
heatmap_plotter('spatial03 fitness dispersion radius', fitness_x, dispersion_y, critical_radius,'Drive homozygote fitness', 'Dispersion',6,2,4,2,[minvalue,maxvalue],false,colormap_);
min(min(critical_radius)) %0.0916