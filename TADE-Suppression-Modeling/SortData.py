"""
Copies the data from the newly generated file to the damaged or unsorted csv file.
Sort the file first by radius (or by migration rate, or by release fraction),
then by fraction (or by low density growth rate, or by embryo cut rate in the underdominance drive),
all in a descending order.

For example:
python3 SortData.py array_with_python.csv

Author: Yutong Zhu (yz2676@cornell.edu)
Date: 2022-1-15
"""
import sys, os
import csv
import copy


def main():
    """
    Sort the file with (or without) the complementary array_with_python0.csv file.
    """
    file = csv.reader(open(sys.argv[1]))
    sortFile = sorted(file, key = lambda x: (x[0], x[1]), reverse = True)
    copyFile = copy.deepcopy(sortFile)
    hint = 0
    for any_row in sortFile:
        if any_row[1].find(".") != -1: # Identify if this (radius & fraction) is varying
                                       # or this (migration & low density) is varying
            hint += 1
    if hint > 1: # This could the file where the varying parameter is low density rate, whose type is int
        print("here at low density file")
        original = sorted(copyFile, key = lambda x: (x[0], float(x[1])) if x[1][0] != "f" and x[1][0] != "l" else (x[0], x[1]), reverse = True)
    else:
        original = copyFile

    if os.path.exists("array_with_python0.csv") == True:
        fix = csv.reader(open("array_with_python0.csv"))
        sortFix = sorted(fix, key = lambda x: (x[0], float(x[1])), reverse = True)
        # print(sortFix)
        if sortFix[0][0] == "radius" or sortFix[0][0] == "migration" or sortFix[0][0] == "fraction" or sortFix[0][0] == "release_fraction":
            count = 1 # Trims the fix file header off
        else:
            count = 0

    with open(sys.argv[1], "w") as f1:
        filewriter = csv.writer(f1)
        for row in original:
            # print(row)
            if row[-1] == "" or len(row) < 17: # Sometimes the damaged file
                                               # doesn't contain the empty space holder.
                filewriter.writerow(sortFix[count])
                count += 1
            else:
                filewriter.writerow(row)
    f1.close()
    print("New file has been generated.")

if __name__ == "__main__":
    main()
