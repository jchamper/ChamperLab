clc;clear;close all;
addpath('../../plots');
[path,name]=fileparts(mfilename('fullpath'));
if exist(['tempdata' name '.mat'],'file') == 0
    GENERATIONS = 1000;
    num_points = 500;
    criterion = 0.7;
    
    anss = ones(1,num_points);
    fitness_x = linspace(0.6,1,num_points);
    x_min = fitness_x(1);
    x_max = fitness_x(length(fitness_x));
    x_interval = (x_max-x_min)/(num_points-1);
    intro_y = linspace(0.3,0.8,num_points);

    for fitness = fitness_x
        fitness
        for intro = intro_y
            [gen,allele,carrier] = cifAB_together_odeplot(linspace(0,GENERATIONS,3),intro,fitness,1,1,0);
            if (carrier(length(carrier)) > criterion)
                anss(round((fitness-x_min)/x_interval+1)) = intro;
                break
            end
        end
    end
    save(['tempdata' name '.mat']);
end
load(['tempdata' name '.mat']);

%find first point that is below 1
idx = find(anss<1,1);
fitness_x(idx)
line_plotter('01 cifAB threshold', fitness_x,anss,'Drive homozygote fitness', 'Introduction threshold');