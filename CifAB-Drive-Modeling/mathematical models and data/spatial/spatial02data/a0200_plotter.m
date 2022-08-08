clc;clear;close all;
addpath('../../plots');
num_points = 200;
num_parts = 10;
points_per_part = num_points / num_parts; %20
wave_speed = zeros(num_points);
[path,name]=fileparts(mfilename('fullpath'));
for num = 1:10
    string = num2str(num);
    if length(string) == 1
        string = ['0' string];
    end
    partname = ['tempdataa02_speed_fitness_wavespeed_' string '.mat'];
    load(partname);
    wave_speed(((num-1)*points_per_part+1):(num*points_per_part),:) = wavespeed(((num-1)*points_per_part+1):(num*points_per_part),:);
end

colormap_ = colormap('cool');
close;
wave_speed(wave_speed==0) = nan;
min(wave_speed(wave_speed>0))
heatmap_plotter('spatial02 dispersion fitness wavespeed', fitness_x, dispersion_y, wave_speed,'Drive homozygote fitness', 'Dispersion',6,2,6,2,[0,8e-3],false,colormap_,0);