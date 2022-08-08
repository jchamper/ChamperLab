clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    num_points = 20;
    SPEED_x = linspace(0.01,0.1,num_points);
    x_min = SPEED_x(1);
    x_max = SPEED_x(length(SPEED_x));
    x_interval = (x_max-x_min)/(num_points-1);
    wavespeed_y = zeros(1,num_points);
    
    for x = SPEED_x
        x
        y = wave_speed(x,1,0);
        wavespeed_y(round((x-x_min)/x_interval+1)) = y;
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
line_plotter('spatial01 wave speed', SPEED_x,wavespeed_y,'Dispersion', 'Wave speed');