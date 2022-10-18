"""
Writes a new bash file (fix.sh) containing the necessary missing lines from the excel output.
Runs the following line on the command line:
python Fixer.py [name of damaged csv file] [original bash file]

For example, writes a new bash file on the high computing clusters for the
damaged array_with_python1.csv file:
e.g. python3 Fixer.py array_with_python1.csv try1.sh

Be sure to this file and the other necessary files including the original bash file,
the minimal_slim_driver.py file and the space_TA.slim file to the specific py_data folder.

The algorithm of this file relies on the ordinality of the original bash file (the format),
please make sure that the specific parameter is listed in order.
(e.g. first we have -eRes 1.0, then we have -eRes 0.95, but not the other direction)

Author: Yutong Zhu (yz2676@cornell.edu)
Date: 2022-1-20
"""
import sys


def detect(line):
    """
    Returns: A sorted list containing the paired missing information of radius
    and fraction (or embryo_cut_rate and fraction (look out the order is not the same!))
    from the original csvfile.
    A comma is used to separate these two values.

    Sorts the list in a descending order. Because the template for selecting the
    necessary paramters is written in descending order, and to avoid neglecting
    some of the potential data before examining the next line, we need the list
    also to be in a descending order.

    Parameter line: the list of the original dataset.
    Precondition: line is a list.
    """
    ls = []
    underdominance = False
    for i in line:
        if i.find("embryo_resistance_rate") != -1: # need to reformat the list if it is a
                                                      # underdominance file. See reasoning at
                                                      # function write() else part.
            underdominance = True
            break

    for i in range(len(line)):
        if len(line[i]) < 37: # minimal length of a well-generated line
            data = line[i].split(",")
            if not underdominance:
                if data[1] == "1":
                    ls.append(data[0] + "," + "1.0") # format for future searching
                else:
                    ls.append(data[0] + "," + data[1])
            else:
                if data[1] == "1":
                    ls.append("1.0" + "," + data[0]) # format for future searching
                else:
                    ls.append(data[1] + "," + data[0])
    # print(ls)
    ls.sort(key = lambda x: (float(x.split(",")[0]), float(x.split(",")[1])), reverse = True)
    return ls


def write(ls, output, format):
    """
    Writes the new fix.sh file.

    Parameter ls: the complete paired missing data (radius+fraction or fraction+embryo_cut_rate)
    Precondition: ls is a list.

    Parameter output: the fix.sh bash file.
    Precondition: output is a writable bash file.

    Parameter format: the list of original bash file.
    Precondition: format is a list.
    """
    # if ls is empty, we simply returns
    if len(ls) == 0:
        return
    dir = ""
    version = 0 # 0 for radius+fraction pair, 1 for fraction+embryo_cut_rate pair, 2 for migration+growth pair
    subversion = 0 # 0 for single release in underdominance drive, 1 for repeat release in underdominance drive
    count = 0
    output.write("#!/bin/bash\n")
    for i in range(len(format)): # Save the folder name.
        if format[i].find("mkdir") != -1:
            output.write(format[i])
            dir = format[i][16:] # the folder_name
            # print(format[i+1])
            if format[i+1][47:50] == "1.0": # parse the string and check if -eRes == 1.0
                                            # the difference between the perfect drive file
                                            # which needs fixing and the underdominance drive file
                                            # that needs fixing is that the perfect drive sets embryo_cut_rate
                                            # to 0.0, but underdominance drive varies this parameter and starts
                                            # with 1.0.
                version = 1 # the underdominance file
                if format[i+1].find("5000") != -1:
                    subversion = 1 # underdominance repeat release
            if format[i+1][61:65] == "0.38" or format[i+1][59:63] == "0.38": # we specified the appropriate radius for left edge release
                                             # is 0.38.
                version = 2
            break

    # Start searching in the original ordered and complete bash file, if certain
    # conditions are met, then copy that line into the new bash file.
    for i in range(len(format)):
        if version == 0: # this is for dealing with missing radius and fraction parameters
            radius = ls[count].split(",")[0]
            fraction = ls[count].split(",")[1]
            findR = format[i].find(radius)
            if findR != -1 and format[i][findR - 3] != "u": # Making sure that the number is right behind "-radius".
                findR = format[i].find(radius, findR+1) # Only need to worry about confusing the number with
                                                    # the "-eRes" (could also be in the range of the radius)
            findF = format[i].find(fraction)
            if findF == findR and findR != -1: # Avoid situations where string radius contains the fraction part.
                findF = format[i].find(fraction, findR+1)
            if findR != -1 and findF != -1:
                # Making sure it's not partially overlapped.
                if format[i][findR + len(radius)] == " " and format[i][findF + len(fraction)] == " ":
                    output.write(format[i])
                    count += 1
                    if count == len(ls): # Stop the iteration before index out of range.
                        print("Finished writing the file. Length of: " + str(count))
                        break

        elif version == 1: # dealing with missing fraction and embryo_cut_rate parameters
            embryo_cut_rate = ls[count].split(",")[0]
            findE = format[i].find(embryo_cut_rate) # This algorithm relies on searching specific parameter that
                                                    # is the same order as in the format file. Because fisrtly you
                                                    # searched every character in this line to identify whether the first
                                                    # varying parameter is in this file, if not, move to the next line.
                                                    # But in this situation you might not be able to copy this "bigger"
                                                    # data (because we wrote the original bash file in a descending order)
                                                    # if it does appear somewhere later in the need_to_copy_list.
                                                    # So we need to search the embryo_cut_rate first,
                                                    # so the input of the list should also first
                                                    # sort the embryo_cut_rate, then the fraction parameter.

            if findE != -1 and format[i][findE - 5] != "e": # Making sure that the number is right behind "-eRes".
                findE = format[i].find(embryo_cut_rate, findE+1) # Only need to worry about confusing the number with
                                                          # the "-gRes" (could also be in the range of the fraction)

            if subversion == 0:
                fraction = ls[count].split(",")[1]
                if findE == findF and findE != -1: # Avoid situations where string eRes contains the fraction part.
                    findF = format[i].find(fraction, findF+1)
                if findF != -1 and findE != -1:
                    # Making sure it's not partially overlapped.
                    if format[i][findF + len(fraction)] == " " and format[i][findE + len(embryo_cut_rate)] == " ":
                        output.write(format[i])
                        count += 1
                        if count == len(ls): # Stop the iteration before index out of range.
                            print("Finished writing the file. Length of: " + str(count))
                            break
            else: # for simplification, we still use the term fraction. But it's actually release size.
                fraction = str(int(float(ls[count].split(",")[1])*50000))
                findF = format[i].find(fraction)
                if findF != -1 and (format[i][findF-1] != " " or format[i][findF+len(fraction)] != " "): # Avoid situations where the original file contains parts of the desired fraction
                                                              # (e.g. 500 but stop at 2500 line, or 250 but stopped at 2500 line)
                    # print(format[i])
                    # print("oh never here")
                    findF = format[i].find(fraction, findF+1)
                if findF != -1 and findE != -1:
                    # print(embryo_cut_rate)
                    # print(fraction)
                    output.write(format[i])
                    count += 1
                    if count == len(ls): # Stop the iteration before index out of range.
                        print("Finished writing the file. Length of: " + str(count))
                        break
        else: # the low density parameter release file, dealing with missing migration and growth rate
            migration = ls[count].split(",")[0]
            growth = ls[count].split(",")[1]
            if growth[-1] == "0": # strip the ".0" in the end
                growth = growth[:-2]

            findM = format[i].find(migration)
            while findM != -1 and format[i][findM - 2] != "n": # Making sure that the number is right behind "-migration".
                findM = format[i].find(migration, findM+1) # Only need to worry about confusing the number with
                                                        # the "-eRes" (could also be in the range of the migration)
            while findM != -1 and format[i][findM+len(migration)] != " ": # Avoid situations where the original file contains parts of the desired value
                                                                           # (e.g. 0.05 but stop at 0.0575 line)
                findM = format[i].find(migration, findM+1) # We still need to check if it is the right part so we use while-loop
            findG = format[i].find(growth)
            while findG != -1 and format[i][findG-1] != " ": # Avoid situations where the original file contains parts of the desired value
                                                          # (e.g. -eRes 0.99 but we want -growth 9)
                findG = format[i].find(growth, findG+1)

            while findG != -1 and format[i][findG+len(growth)] != " ": # Avoid situation where the original file contains parts of the desired value
                                                                            # (e.g. 10 but stop at 10.5 line)
                findG = format[i].find(growth, findG+1)
                while findG != -1 and format[i][findG-1] != " ":
                    findG = format[i].find(growth, findG+1)
            if findM != -1 and findG != -1:
                output.write(format[i])
                count += 1
                if count == len(ls): # Stop the iteration before index out of range.
                    print("Finished writing the file. Length of: " + str(count))
                    break




    output.write("wait\ncd py_data" + dir + "cat *.part > array_with_python0.csv\nrm *.part")


def main():
    """
    Opens the damaged csv file and original bash file, uses the bash file as a
    template for copying the specific lines into the new bash file fix.sh.
    """
    csvfile = open(sys.argv[1],"r")
    bashfile = open(sys.argv[2], "r")
    output = open("fix.sh","w")
    lines = csvfile.readlines()
    format = bashfile.readlines()
    list = detect(lines)

    # Help with expliciting what to expect.
    print(list)
    print("\nlength of file = " + str(len(list)))

    write(list, output, format)
    output.close()
    bashfile.close()
    csvfile.close()


if __name__ == "__main__":
    main()
