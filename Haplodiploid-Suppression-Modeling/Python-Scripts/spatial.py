#Author: Yiran Liu, Sam Champer and Isabel Kim
'''This script will use Python as a driver for SLiM and do the chase checking at the same time.'''
from argparse import ArgumentParser
import numpy as np
import subprocess
import sys

def parse_slim(slim_string):
    i = str(slim_string)
    line_space = i.split('\n')

    suppressed = 0
    gen_suppressed = 10000
    chased = 0
    gen_chase_started = 10000
    gen_chase_ended = 0
    gc_average = 10000
    gc_variance = 10000
    avg_pop_during_chase = 1000000
    var_pop_during_chase = 1000000
    duration_of_chasing = 10000
    pop_persistance = 0
    gen_persistance = 10000
    equilibrium = 0
    gen_equilibrium = 10000
    stopped_1000 = 0
    rate_at_stop = 10000
    r1_resistance = 0
    gen_r1_resistance = 10000
    capacity = 50000
    check_chasing = False
    avg_female_fertile = 1000000
    number_of_fertile_females = []

    for line in line_space:
        if line.startswith("SUPPRESSED:: "):  #suppression occurs
            spaced_line = line.split()
            suppressed = 1
            gen_suppressed = int(spaced_line[1])
        if line.startswith("POTENTIAL_CHASE:: "): 
            check_chasing = True
        if line.startswith("ENDING_AFTER_1000"):
            spaced_line = line.split()
            stopped_1000 = 1
            rate_at_stop = float(spaced_line[1]) #show the rate of individuals with drive
        if line.startswith("POP_PERSISTS:: "): #drive lost and wt population remained
            spaced_line = line.split()
            pop_persistance = 1
            gen_persistance = int(spaced_line[1])
        if line.startswith("EQUILIBRIUM:: "): #equilibrium state attained
            spaced_line = line.split()
            equilibrium = 1
            gen_equilibrium = int(spaced_line[1])
            check_chasing = False #no longer true chasing
        if line.startswith("RESISTANCE:: "): #resistance allele formation
            spaced_line = line.split()
            r1_resistance = 1
            gen_r1_resistance = int(spaced_line[1])
        if line.startswith("FERTILE_FEMALES:: "):
            spaced_line = line.split()
            number_of_fertile_females.append(int(spaced_line[1]))
            
    if (check_chasing):
        # only will have chasing if we find a wt allele minimum and a green's
        # coefficient maximum
        wt_min = False
        eq_check = 0.8 * 2 * capacity
        wt = []
        gen = []
        pops = []
        gcs = []
        overall_gcs = []
        for line in line_space:
            if line.startswith("WT_ALLELES:: "):
                spaced_line = line.split()
                num_wt_alleles = int(spaced_line[1])
                this_gen = int(spaced_line[2])
                this_popsize = int(spaced_line[3])
                this_gc = float(spaced_line[4])  # gc space here
                this_overall_gc = float(spaced_line[5])
                wt.append(num_wt_alleles)
                gen.append(this_gen)  # Creates a generations list
                pops.append(this_popsize)
                gcs.append(this_gc)
                overall_gcs.append(this_overall_gc)

        # determin if there was a wt allele minimum
        last_gen = len(gen) - 1  # index of the last generation
        for i in range(len(wt)):
            # check 1: have at least 5 generations occurred since tracking began
            # or was this at least 5 generations prior to the end of the simulation?
            if (i > 4) and (i < (last_gen - 4)):
                this_count = wt[i]
                # check 2:is the wt count less than 80% of its eq value?
                if (this_count < eq_check):
                    last_count = wt[i - 1]
                    next_count = wt[i + 1]
                    # check3: was the last generation's wt allele count higher
                    # and was the next generation's wt allele count higher?
                    if (last_count > this_count) and (next_count > this_count):
                        prior_three = wt[(i - 3):i]
                        next_three = wt[(i + 1):(i + 4)]
                        prior_avg = np.average(prior_three)
                        next_avg = np.average(next_three)
                        # check 4: was the average of the last 3 generations' wt allele
                        # counts higher and was the average of the next 3 generations'
                        # wt allele counts higher?
                        if (prior_avg > this_count) and (next_avg > this_count):
                            wt_min = True  # found a minimum
                            gen_wt_min = gen[i]
                            break
        # if we've found a wt allele minimum, now check for a gc maximum
        if wt_min:
            for i in range(len(gcs)):
                # check 1: have at least 5 generations occurred since tracking began
                # or was this at least 5 generations prior to the end of the simulation?
                if (i > 4) and (i < (last_gen - 4)):  # need 5 gens on each side
                    this_gc_count = gcs[i]
                    last_gc_count = gcs[i - 1]
                    next_gc_count = gcs[i + 1]
                    # check 2: was the last generation's green's coefficient lower
                    # and was the next generation's green's coefficient count lower?
                    if (last_gc_count < this_gc_count) and (next_gc_count < this_gc_count):
                        prior_three = gcs[(i - 3):i]
                        next_three = gcs[(i + 1):(i + 4)]
                        prior_avg = np.average(prior_three)
                        next_avg = np.average(next_three)
                        # check 3: was the average of the last 3 generations' green's
                        # coefficients lower and was the average of the next 3 generations'
                        # green's coefficients lower?
                        if (prior_avg < this_gc_count) and (next_avg < this_gc_count):
                            # found both a wt_min and gc_max
                            chased = 1
                            gen_gc_max = gen[i]
                            gen_chase_started = min(gen_gc_max, gen_wt_min)
                            pos = gen.index(gen_chase_started)
                            # summary stats of chase:
                            gcs_of_interest = gcs[(pos + 3):-2]
                            gc_average = np.average(gcs_of_interest)
                            gc_variance = np.var(gcs_of_interest)
                            popsizes_of_interest = pops[(pos + 3):-2]
                            female_fertile_of_interest = number_of_fertile_females[(pos + 3):-2]
                            avg_pop_during_chase = np.average(popsizes_of_interest)
                            var_pop_during_chase = np.var(popsizes_of_interest)
                            avg_female_fertile = np.average(female_fertile_of_interest)
                            overall_gcs_of_interest = overall_gcs[(pos + 3):-2]
                            overall_gc_average = np.average(overall_gcs_of_interest)
                            overall_gc_variance = np.var(overall_gcs_of_interest)
                            gen_chase_ended = gen[-1]
                            duration_of_chasing = gen[-1] - gen_chase_started  # index of the last generation - gen_chase_started
                            break

    return suppressed, gen_suppressed, chased, gen_chase_started, gen_chase_ended, duration_of_chasing, gc_average, gc_variance,\
           avg_pop_during_chase, var_pop_during_chase, pop_persistance, gen_persistance, equilibrium, gen_equilibrium,\
           stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance, avg_female_fertile
def run_slim(command_line_args):
    """
    Runs SLiM using subprocess.
    Args:
        command_line_args: list; a list of command line arguments.
    return: The entire SLiM output as a string.
    """
    slim = subprocess.Popen(command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
    out, err = slim.communicate()
    return out
def configure_slim_command_line(args_dict):
    """
    Sets up a list of command line arguments for running SLiM.
    Args:
        args_dict: a dictionary of arg parser arguments.
    Return
        clargs: A formated list of the arguments.
    """
# We're running SLiM, so the first arg is simple:
    clargs = "slim "
# The filename of the source file must be the last argument:
    source = args_dict.pop("source")
# Add each argument from arg parser to the command line arguemnts for SLiM:
    for arg in args_dict:
        print(arg)
        if isinstance(args_dict[arg], bool):
            clargs += f"-d {arg}={'T' if args_dict[arg] else 'F'} "
        else:
            clargs += f"-d {arg}={args_dict[arg]} "
        print(clargs)
# Add the source file, and return the string split into a list.
    clargs += source
    return clargs.split()
def main():
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="spatial.slim", type=str,
    help=r"SLiM file to be run. Default 'geneticload.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
    help='If this is set, python prints a header for a csv file.')
    parser.add_argument('-migrationvalue','--SPEED', default=0.04, type=float,
    help='value')
    parser.add_argument('-lowdensity','--GROWTH_AT_ZERO_DENSTITY', default=6.0, type=float)
    parser.add_argument('-fitness','--DRIVE_FITNESS_VALUE', default=1.0, type=float)
    parser.add_argument('-conversion','--DRIVE_CONVERSION_RATE', default=0.95, type=float)
    args_dict = vars(parser.parse_args())
# The '-header' argument prints a header for the output. This can
# help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("suppressed, gen_suppressed, chased, gen_chase_started, gen_chase_ended, duration_of_chasing, gc_average, gc_variance,\
           avg_pop_during_chase, var_pop_during_chase, pop_persistance, gen_persistance, equilibrium, gen_equilibrium,\
           stopped_1000, rate_at_stop, r1_resistance, gen_r1_resistance,avg_female_fertile")
# Next, assemble the command line arguments in the way we want to for SLiM:
    clargs = configure_slim_command_line(args_dict)
# Run the file with the desired arguments.
    slim_result = run_slim(clargs)
# Parse and analyze the result.
    parsed_result = parse_slim(slim_result)
    print(parsed_result)


if __name__ == "__main__":
    main()
