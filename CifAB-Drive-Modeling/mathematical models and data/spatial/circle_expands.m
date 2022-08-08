% clc;clear;close all;
% intro = 0.8;
% R = 0.34;
% D = 0.01;
% F = 1;
% 
% radius = 5;
% dx = 0.1;
% x = 0:dx:radius;
% [dd,wd] = deal(zeros(1,length(x)));
% ww = ones(1,length(x));
% dd(1:round(length(dd)*R*2)) = intro/(1-intro);
% expands = circle_expands_(dd,wd,ww,dx,D,F,1)

function expands = circle_expands_(dd,wd,ww,dx,D,F,drawplot)
    %F here is homozygote fitness
    %ww,wd,ww is initial status
    F = sqrt(F);
    GENERATIONS = 15;
    start_detect_generation = 10;
    end_detect_generation = GENERATIONS;
    radius = dx*(length(dd)-1);
    dt = 0.0001/D;
    t = 0:dt:(GENERATIONS+0.4);
    D = D^2 * (2*radius)^2/2;
    detect_indices = round(1+[start_detect_generation,end_detect_generation]/dt); %time points to detect
    freq_list = [];
    for n = 2:length(t)
        [dd,wd,ww] = spread1D_circle(dd,wd,ww,dt,dx,D,F);
        if any(n==detect_indices)
            subpop_size = sum(linspace(0,radius,length(ww)) .* (ww + wd + dd));
            carrier_frequency = sum(linspace(0,radius,length(ww)) .* (wd + dd)) / subpop_size;
            freq_list = [freq_list,carrier_frequency];
        end
        if rem(n,round(0.1/dt)) == 0
            if drawplot
                subpop_size = ww + wd + dd;
                carrier_frequency = wd + dd ./ subpop_size;
                disp(['gen ' num2str(n*dt)]);
                disp(carrier_frequency(round(linspace(1,length(carrier_frequency),8))));
            end
        end
    end
    expands = freq_list(1) < freq_list(2);
end