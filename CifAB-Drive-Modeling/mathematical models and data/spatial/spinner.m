% clc;clear;close all;
% num = 100;
% f = [linspace(1,2,num) zeros(1,100)];
% ret = spinner_(f);
% mesh(ret);



function ret = spinner_(f)
    %Returns square arena. Returns 0 for places that are out of the circle.
    len = length(f);
    num_points = 2*len-1;
    ret = zeros(num_points);
    for i = 1:num_points
        for j = 1:num_points
            dist = sqrt((i-len)^2 + (j-len)^2);
            if floor(dist)+1 > len
                continue;
            end
            ret(i,j) = f(floor(dist)+1);
        end
    end
end