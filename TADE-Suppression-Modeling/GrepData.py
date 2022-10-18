"""
Grep the specific parameters from 20 files.

Columns of interest:
[invasiveness, suppressed_without_chase, suppressed_after_chase, drive_lost_without_chase,
drive_lost_after_chase, long_term_chasing, ending_generation, rate_of_drive,
rate_of_drive_individuals, rate_of_r2_resistance_alleles, ending_population,
ending_generation, generation_chasing_starts, duration_of_chasing,
average_population_during_chasing, average_fertile_female_during_chasing, slow_drive_growth]

e.g.
python3 GrepData.py invasiveness

Author: Yutong Zhu (yz2676@cornell.edu)
Date: 2022-3-27
"""
import sys
import pandas as pd
from glob import glob


### Constants
INVASIVENESS = 2
SUPPRESSED_WITHOUT_CHASE = 3
DRIVE_LOST_WITHOUT_CHASE = 4
SUPPRESSED_AFTER_CHASE = 5
DRIVE_LOST_AFTER_CHASE = 6
LONG_TERM_CHASING = 7
ENDING_GENERATION = 8
RATE_OF_DRIVE = 9
RATE_OF_DRIVE_INDIVIDUALS = 10
RATE_OF_R2_RESISTANCE_ALLELES = 11
ENDING_POPULATION = 12
GENERATION_CHASING_BEGINS = 13
AVGERAGE_POPULATION_DURING_CHASING = 14
DURATION_OF_CHASING = 15
AVERAGE_FERTILE_FEMALE_DURING_CHASING = 16
SLOW_DRIVE_GROWTH = 18


def concatenate(input):
    """
    Returns: the name of the new file.
    Generates a new file containing the 20 repeats of specific parameter outcomes.

    Parameter input: a string from the the columns of interest.
    Precondition: input is a string in the list of columns of interest.
    """
    column_of_interest = identifyparameter(input)

    combined_df = pd.concat(
                            [pd.read_csv(csv_file, usecols = [column_of_interest], sep = ",")
                             for csv_file in glob("*.csv")], axis = 1)
    name = sys.argv[1][0].upper() + sys.argv[1][1:]+".csv"
    combined_df.to_csv(name)
    return name


### Helper method
def identifyparameter(input):
    """
    Returns: the desired column_of_interest.

    Parameter input: a string from the the columns of interest.
    Precondition: input is a string in the list of columns of interest.
    """
    if input.startswith("i"):
        column_of_interest = INVASIVENESS
    elif input.startswith("s"):
        if input.find("without") != -1:
            column_of_interest = SUPPRESSED_WITHOUT_CHASE
        elif input.find("after") != -1:
            column_of_interest = SUPPRESSED_AFTER_CHASE
        else:
            column_of_interest = SLOW_DRIVE_GROWTH
    elif input.startswith("d"):
        if input.find("without") != -1:
            column_of_interest = DRIVE_LOST_WITHOUT_CHASE
        elif input.find("chasing") != -1:
            column_of_interest = DURATION_OF_CHASING
        else:
            column_of_interest = DRIVE_LOST_AFTER_CHASE
    elif input.startswith("l"):
        column_of_interest = LONG_TERM_CHASING
    elif input.startswith("e"):
        if input.find("generation") != -1:
            column_of_interest = ENDING_GENERATION
        else:
            column_of_interest = ENDING_POPULATION
    elif input.startswith("r"):
        if input.find("individuals") != -1:
            column_of_interest = RATE_OF_DRIVE_INDIVIDUALS
        elif input.find("r2") != -1:
            column_of_interest = RATE_OF_R2_RESISTANCE_ALLELES
        else:
            column_of_interest = RATE_OF_DRIVE
    elif input.startswith("a"):
        if input.find("population") != -1:
            column_of_interest = AVGERAGE_POPULATION_DURING_CHASING
        else:
            column_of_interest = AVERAGE_FERTILE_FEMALE_DURING_CHASING
    elif input.startswith("g"):
        column_of_interest = GENERATION_CHASING_BEGINS
    # print(column_of_interest)
    return column_of_interest


def main():
    """
    Generates a new file containing the 20 repeats of specific parameter outcomes.
    """
    file = sys.argv[1]
    name = concatenate(file)
    print("File: " + name + " has been generated.")


if __name__ == "__main__":
    main()
