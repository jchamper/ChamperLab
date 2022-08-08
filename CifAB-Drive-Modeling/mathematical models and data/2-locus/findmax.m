% [maxvalue,maxidx] = findmax_([1,3,2])
function [maxvalue,maxidx] = findmax_(lt)
   [r,c] = size(lt);
   [maxvalue_,maxidx_] = deal(0);
   for i = 1:c
       if lt(i) > maxvalue_
           maxvalue_ = lt(i);
           maxidx_ = i;
       end
       
   end 
   maxvalue = maxvalue_;
   maxidx = maxidx_;
end