clc;clear;close all;
% addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    F = 1;
    D = 0.03;
    num_points = 200;
    precision = 1024;
    r0_x = linspace(0,0.3,num_points);
    d_y = linspace(0,0.3,num_points);
    height_list = linspace(0,99,precision);
    x_min = r0_x(1);
    x_max = r0_x(length(r0_x));
    x_interval = (x_max-x_min)/(num_points-1);
    y_min = d_y(1);
    y_max = d_y(length(d_y));
    y_interval = (y_max-y_min)/(num_points-1);
    critical_height= zeros(num_points);

    dx = 0.05;
    radius = 5;
    x = 0:dx:radius;

    for r0 = r0_x
        r0
        for d = d_y
            if r0+d > 0.5
                critical_height(round((d-y_min)/y_interval+1),round((r0-x_min)/x_interval+1)) = 0;
                continue;
            end


            lo = 1; hi = length(height_list);
            while lo < hi
                mid = lo + floor((hi-lo) / 2);
                h = height_list(mid);
                wd = zeros(1,length(x));
                ww = ones(1,length(x));
                dd = zeros(1,length(x));
                dd((floor(2*r0*(length(x)-1)+1)):(floor(2*(r0+d)*(length(x)-1)+1))) = h;
                expands = circle_expands(dd,wd,ww,dx,D,F,0);

                if expands
                    hi = mid;
                else
                    lo = mid + 1;
                end
            end
            critical_height(round((d-y_min)/y_interval+1),round((r0-x_min)/x_interval+1)) = height_list(lo);
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

for i = 1:num_points
    for j = 1:num_points
        h = critical_height(i,j);
        if h == max(height_list)
            critical_height(i,j) = nan;
            continue
        end
        d = d_y(i);
        r0 = r0_x(j);
        critical_height(i,j) = h*pi*(2*r0*d + d^2);
%         %%%%%%%%%%%  0.7742 critical height
%         if (i==115 & j==70)
%             critical_height
%         end
%         if (critical_height(i,j) < 0.2383) && (0.001<critical_height(i,j))
%             r0
%             d
%         end
    end
end
critical_height(1,1) = nan;
minvalue = 1;
maxvalue = 0;
colormap_ = colormap(othercolor('Accent4')); 
close;
colormap_(end,:) = [1,1,1];
min(min(critical_height(critical_height>0.001)))
heatmap_plotter('spatial05 ringdrop critical volume', r0_x, d_y, critical_height,'r_0', 'd',5,2,5,2,[minvalue,maxvalue],false,colormap_,0);