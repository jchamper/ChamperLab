% clc;clear;close all;
% answer = wave_speed_(0.01,1,1);

function answer = wave_speed_(D,F,drawplot,e) %answer is bool
    if nargin == 3
        e = 1;
    end
    
    detect_generations = 100:10:10000; %detect if drive is retreating
    last_detected_frequency = 0;
    F = sqrt(F);
    boundary_x = 0.2;
    line1 = 0.5;
    line2 = 0.7;

    xylen = 10;GENERATIONS = 10000;
    line1_ = line1;line2_ = line2;
    
    dx = 0.1; dt = 0.0005/D;
    x=-xylen/2:dx:2*xylen/2;
    realx = -xylen/2:dx:xylen/2;
    t=0:dt:GENERATIONS;
    
    [ww,wd,dd]=deal(zeros(1,length(x))); 

    exceeded_line1 = false;
    boundary_x = round(1 + xylen*boundary_x/dx);
    line1 = round(1 + xylen*line1/dx);
    line2 = round(1 + xylen*line2/dx);
    
    %drop drives in the area
    ww(boundary_x+1:end)=1;
    dd(1:boundary_x)=1;
    
    D = D^2 * xylen^2/2;

    %calculate start carrier frequency
    detect_idx = round(1+detect_generations/dt);
    for n = 2:length(t) %nth time point
        [dd,wd,ww] = spread1D_linear(dd,wd,ww,dt,dx,D,F,e);
        
        %detect if drive is going to get lost
        if any(n == detect_idx)
            subpop_size = sum(ww(1:length(realx)) + wd(1:length(realx)) + dd(1:length(realx)));
            carrier_frequency = sum(wd(1:length(realx)) + dd(1:length(realx))) / subpop_size;
            if carrier_frequency < last_detected_frequency
                answer = nan;
                return;
            end
            if abs(carrier_frequency - last_detected_frequency) < 1e-60
                answer = 0;
%                 figure;
%                 plot(x,dd,x,ww);
                return;
            else
                last_detected_frequency = carrier_frequency;
            end
        end
        
        %detect if reaches line
        if rem(n,round(0.1/dt)) == 0
            num_inds_line1 = ww(line1) + wd(line1) + dd(line1);
            num_inds_line2 = ww(line2) + wd(line2) + dd(line2);
            line1_cafreq = (dd(line1) + wd(line1))/num_inds_line1;
            line2_cafreq = (dd(line2) + wd(line2))/num_inds_line2;


            if ~exceeded_line1
                if drawplot
                    disp(['gen ' num2str(n*dt) ' line1: ' num2str(line1_cafreq)]);

                end
                if line1_cafreq>0.5
                    exceeded_line1 = true;
                    tag = n*dt;
                end
            else
                if drawplot
                    disp(['gen ',num2str(n*dt),' line2: ',num2str(line2_cafreq)]);
                end
                if line2_cafreq>0.5
                    if drawplot
                        disp(['took ' num2str(n*dt-tag) ' generations to travel '  num2str(line2_-line1_) ', average wave speed '  num2str((line2_-line1_)/(n*dt-tag))]);
                    end
                    answer = (line2_-line1_)/(n*dt-tag);
                    return;
                end
            end
        end
    end
    answer = 0;
end