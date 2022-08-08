csv_name = "01.csv"
num_popsizes = 4

with open(csv_name,"r") as f:
    lines = [i.strip() for i in f.readlines()]

d = {}
for line in lines:
    num_inds, intro, fixed = line.split(",")
    if (num_inds,intro) not in d:
        d[(num_inds,intro)] = []
    d[(num_inds,intro)].append(fixed)

for key in d:
    d[key] = d[key].count("1")/len(d[key])
lt = list(d.items())
lt.sort(key = lambda i:float(i[0][1]))
lt.sort(key = lambda i:float(i[0][0]))
# print(lt,len(lt))
items = [i[1] for i in lt]
length_for_each = round(len(lt)/num_popsizes)
prob_1 = items[0:length_for_each]
prob_2 = items[length_for_each:2*length_for_each]
prob_3 = items[2*length_for_each:3*length_for_each]
prob_4 = items[3*length_for_each:4*length_for_each]
print(prob_1)
print(prob_2)
print(prob_3)
print(prob_4)