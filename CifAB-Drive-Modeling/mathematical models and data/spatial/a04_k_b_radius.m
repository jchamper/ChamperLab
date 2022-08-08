clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    F = 1;
    D = 0.03;
    num_points = 200;
    precision = 1024;
    k_x = linspace(0,2,num_points);
    b_y = linspace(0,3,num_points);
    radius_list = linspace(0.01,0.5,precision);
    x_min = k_x(1);
    x_max = k_x(length(k_x));
    x_interval = (x_max-x_min)/(num_points-1);
    y_min = b_y(1);
    y_max = b_y(length(b_y));
    y_interval = (y_max-y_min)/(num_points-1);
    critical_radius = zeros(num_points);

    dx = 0.05;
    radius = 5;
    x = 0:dx:radius;

    for k = k_x
        k
        for b = b_y
            lo = 1; hi = length(radius_list);
            while lo < hi
                mid = lo + floor((hi-lo) / 2);
                R = radius_list(mid);
                wd = zeros(1,length(x));
                ww = ones(1,length(x));
                dd = zeros(1,length(x));
                dd = k*(linspace(0,radius,length(dd)))+b;
                dd(floor((length(dd)-1)*R*2+2):end) = 0;
                expands = circle_expands(dd,wd,ww,dx,D,F,0);
                if expands
                    hi = mid;
                else
                    lo = mid + 1;
                end
            end
            critical_radius(round((b-y_min)/y_interval+1),round((k-x_min)/x_interval+1)) = radius_list(lo);
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);
for i = 1:num_points
    for j = 1:num_points
        r = critical_radius(i,j);
        if r == 0.5
            critical_radius(i,j) = nan;
            continue
        end
        b = b_y(i);
        k = k_x(j);
%         %%%%%%%% r=0.2754
%         if (i==3 & j==55)
%             r
%         end
        critical_radius(i,j) = 20/3*k*pi*r^3 + b*pi*r^2;
%         if critical_radius(i,j) < 0.2445
%             k = 10*k
%             b
%         end
    end
end
colormap_ = colormap(othercolor('Accent4')); 
close;
minvalue = 1;
maxvalue = 0;
min(min(critical_radius))
heatmap_plotter('spatial04 kb critical volume', 10*k_x, b_y, critical_radius,'k', 'b',5,0,4,0,[minvalue,maxvalue],false,colormap_,0);