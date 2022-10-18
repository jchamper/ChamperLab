#  Created by Sam Champer, 2020.
#  Modified by Yutong Zhu, 2021.
#  Credit to SLiM-Extras: https://github.com/MesserLab/SLiM-Extras,
#  and Isabel Kim's chase_checker.py.
"""
Use python as a driver for running SLiM, analyzing outputs and generating a csv file,
which contains the information of:
    1. Radius of the released drive (between 0 and 1)
    2. The drive fraction (what percent of individuals were turned into drive individuals, between 0 and 1)
    3. Whether the drive has successfully invaded (0 or 1)
       (Underdominance drive has a separate identifier for successful invasiveness
       that is in a separate file)
    4. One of the five outcomes of the simulation:
         suppressed_withoutChase,  drive_lost_withoutChase,  suppressed_afterChase,
         drive_lost_afterChase, long_term_chase (0 or 1)
    5. The rate of drive/r2 alleles frequency, the rate of drive individuals'
    frequency, if the population persists and drives aren't lost.
    6. The ending population size if population persists.

Author: Sam Champer and Yutong Zhu
2021-10-22
"""
from argparse import ArgumentParser
import numpy as np
import subprocess


def parse_slim(slim_string):
    """
    Returns: the desired output we want from the SLiM simulation.

    This function parse the output of SLiM to extract the following data which
    we're looking for:
    1. Radius specified by the bash files
    2. Drive fraction specified by the bash files
    3. Whether the drive has successfully invaded
    4. One of the five outcomes of the simulation:
         suppressed_withoutChase,  drive_lost_withoutChase,  suppressed_afterChase,
         drive_lost_afterChase, long_term_chase (0 or 1)
    5. The rate of drive/wt, r2 alleles frequency, the rate of drive individuals'
    frequency, if the population persists and drives aren't lost.
    6. The ending population size if population persists.

    Parameter slim_string: the entire output of a run of SLiM.
    """
    output = ""
    lines = slim_string.split('\n')
    output += lines[0][12:] + "," + lines[1][9:] + "," # Get the specified radius and fraction

    data = [1]
    chasing = False
    suppressed = 0
    pop_persistance = 0

    for i in range(0,len(lines)):
        if lines[i].startswith("Rates"):
            # When drives are newly added to the population, the population could fluctuate.
            # We mark the 5th generation's rate_dr as the baseline, and if the population rise by
            # 5% ever after, we regard it as successful invasion.
            rate_dr = lines[i+1].split("\t")[0][4:]
            if lines[i].find("generation 15") != -1:
                data[0] = rate_dr
            elif (float(rate_dr) - float(data[0])) > 0.05 and output.count(",") == 2:
                output += "1,"

        if lines[i].startswith("SUPPRESSED:"):
            suppressed = 1
            output = check_invasiveness(output)
            output += "1,0,0,0,0,"
            output += lines[i].split(":: ")[1]
            output += ",0,0,0,0,"
            break
        elif lines[i].startswith("POP_PERSISTS:"):
            pop_persistance = 1
            output = check_invasiveness(output)
            line = lines[i+3].split(" ")[1:]
            output += "0,1,0,0,0,"
            for data in line:
                output += data
                output += ","
            break

        elif lines[i].startswith("POTENTIAL_CHASE:"):
            chasing = True

        elif lines[i].startswith("LONG_TERM_CHASE:"):
            output = check_invasiveness(output)
            line = lines[i+4].split(" ")[1:]
            output += "0,0,0,0,1,"
            for data in line:
                output += data
                output += ","
            break

    if (chasing):
        ls = check_chasing(lines)
        if (len(ls)!= 0):
            if (suppressed == 1):
                output = output.replace("1,0,0,0,0","0,0,1,0,0")
            elif (pop_persistance == 1):
                output = output.replace("0,1,0,0,0", "0,0,0,1,0")
            output += str(ls["gen_chase_started"])
            output += ","
            output += str("{:.0f}".format(ls["avg_pop_during_chase"]))
            output += ","
            output += str(ls["duration_of_chasing"])
            output += ","
            output += str("{:.0f}".format(ls["avg_female_fertile"]))
        else:
            output += "0,0,0,0"
    else:
        output += "0,0,0,0"
    return output

def check_chasing(line_split):
    """
    Returns: a dictionary containing the generation when chasing starts,
    the average population during chase, the number of fertile females during chase,
    and the duration of chasing if the current simulation is a chasing condition;
    an empty dictionary if otherwise.

    This would be a chasing condition only if we find a wt allele minimum and a green's
    coefficient maximum.

    Parameter line_split: the splitted version of the entire output of a run of SLiM.
    """
    CAPACITY = 10000
    wt_min = False
    eq_check = 0.8*2*CAPACITY
    gen_chase_started = 10000
    avg_pop_during_chase = 1000000
    duration_of_chasing = 10000
    wt = []
    gen = []
    pops = []
    gcs = []
    overall_gcs = []
    number_of_fertile_females = []
    output = {}
    for line in line_split:
        if line.startswith("FERTILE_FEMALES::"):
            spaced_line = line.split()
            number_of_fertile_females.append(int(spaced_line[1]))
        if line.startswith("WT_ALLELES::"):
            spaced_line = line.split()
            wt_alleles = int(spaced_line[1])
            this_gen = int(spaced_line[2])
            this_popsize = int(spaced_line[3])
            this_gc = float(spaced_line[5]) #gc space here
            this_overall_gc = float(spaced_line[7])
            wt.append(wt_alleles)
            gen.append(this_gen) # Creates a generations list
            pops.append(this_popsize)
            gcs.append(this_gc)
            overall_gcs.append(this_overall_gc)

    # Determine if there was a wt allele minimum
    last_gen = len(gen) - 1 # index of the last generation
    for i in range(len(wt)):
        #check 1: have at least 5 generations occurred since tracking began
        #or was this at least 5 generations prior to the end of the simulation?
        if (i > 4) and (i < (last_gen - 4)):
            this_count = wt[i]
            #check 2: is the wt count less than 80% of its eq value?
            if (this_count < eq_check):
                last_count = wt[i-1]
                next_count = wt[i+1]
                #check 3: was the last generation's wt allele count higher
                #and was the next generation's wt allele count higher?
                if (last_count > this_count) and (next_count > this_count):
                    prior_three = wt[(i-3):i]
                    next_three = wt[(i+1):(i+4)]
                    prior_avg = np.average(prior_three)
                    next_avg = np.average(next_three)
                    #check 4: was the average of the last 3 generations' wt allele
                    #counts higher and was the average of the next 3 generations'
                    #wt allele counts higher?
                    if (prior_avg > this_count) and (next_avg > this_count):
                        wt_min = True #found a minimum
                        gen_wt_min = gen[i]
                        break

    # If we've found a wt allele minimum, now check for a gc maximum
    if wt_min:
        for i in range(len(gcs)):
            #check 1: have at least 5 generations occurred since tracking began
            #or was this at least 5 generations prior to the end of the simulation?
            if (i > 4) and (i < (last_gen - 4)): #need 5 gens on each side
                this_gc_count = gcs[i]
                last_gc_count = gcs[i-1]
                next_gc_count = gcs[i+1]
                #check 2: was the last generation's green's coefficient lower
                #and was the next generation's green's coefficient count lower?
                if (last_gc_count < this_gc_count) and (next_gc_count < this_gc_count):
                    prior_three = gcs[(i-3):i]
                    next_three = gcs[(i+1):(i+4)]
                    prior_avg = np.average(prior_three)
                    next_avg = np.average(next_three)
                    #check 3: was the average of the last 3 generations' green's
                    #coefficients lower and was the average of the next 3 generations'
                    #green's coefficients lower?
                    if (prior_avg < this_gc_count) and (next_avg < this_gc_count):
                        #found both a wt_min and gc_max
                        gen_gc_max = gen[i]
                        gen_chase_started = min(gen_gc_max, gen_wt_min)
                        pos = gen.index(gen_chase_started)

                        #summary stats of chase:
                        popsizes_of_interest = pops[(pos+3):-2]
                        female_fertile_of_interest = number_of_fertile_females[(pos+3):-2]
                        avg_pop_during_chase = np.average(popsizes_of_interest)
                        var_pop_during_chase = np.var(popsizes_of_interest)
                        avg_female_fertile = np.average(female_fertile_of_interest)
                        #overall_gcs_of_interest = overall_gcs[(pos+3):-2]
                        #overall_gc_average = np.average(overall_gcs_of_interest)
                        #overall_gc_variance = np.var(overall_gcs_of_interest)
                        duration_of_chasing = gen[-1] - gen_chase_started # index of the last generation - gen_chase_started
                        output["gen_chase_started"] = gen_chase_started
                        output["avg_pop_during_chase"] = avg_pop_during_chase
                        output["avg_female_fertile"] = avg_female_fertile
                        output["duration_of_chasing"] = duration_of_chasing
                        break
    #print(output)
    return output


def check_invasiveness(outstr):
    """
    Returns: the partially desired output.

    Add zero to output if the drive did not invade the population.
    By successful invasion, we meant a 5% frequency increase in drive rate. And
    if the drive had already invaded the populaiton, we would do nothing.

    Parameter outstr: a string containing the partially desired output
    we have generated by now.
    """
    if outstr.count(",") == 2:
        outstr += "0,"
    return outstr


def run_slim(command_line_args):
    """
    Returns: the entire SLiM output as a string.

    Runs SLiM using subprocess.

    Parameter command_line_args: a list of command line arguments.
    """
    slim = subprocess.Popen(command_line_args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    out, err = slim.communicate()
    # For debugging purposes:
    # std.out from the subprocess is in slim.communicate()[0]
    # std.error from the subprocess is in slim.communicate()[1]
    # Errors from the process can be printed with:
    # print(err)
    return out


def configure_slim_command_line(args_dict):
    """
    Returns: a formatted list of arguments.

    Sets up a list of command line arguments for running SLiM.

    Parameter args_dict: a dictionary of arg parser arguments.
    """
    # We're running SLiM, so the first arg is simple:
    clargs = "slim "
    # The filename of the source file must be the last argument:
    source = args_dict.pop("source")
    # Add each argument from arg parser to the command line arguemnts for SLiM:
    for arg in args_dict:
        if isinstance(args_dict[arg], bool):
            clargs += f"-d {arg}={'T' if args_dict[arg] else 'F'} "
        else:
            clargs += f"-d {arg}={args_dict[arg]} "
    # Add the source file, and return the string split into a list.
    clargs += source
    return clargs.split()


def main():
    """
    1. Configure using argparse.
    2. Generate the command line list to pass to subprocess through the run_slim() function.
    3. Run SLiM.
    4. Process the output of SLiM to extract the information we want.
    5. Print the results.
    """
    # Get args from arg parser:
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="space_TA.slim", type=str,
                        help="SLiM file to be run. Default 'space_TA.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
                        help='If this is set, python prints a header for a csv file.')

    # The all caps names of the following arguments must exactly match
    # the names of the constants we want to define in SLiM.
    parser.add_argument('-gRes', '--GERMLINE_RESISTANCE_RATE', default=0.99, type=float,
                        help='The germline resistance formation rate. Default 0.99 percent.')
    parser.add_argument('-eRes', '--EMBRYO_RESISTANCE_RATE', default=0.05, type=float,
                        help='The embryo resistance formation rate. Default 0.05 percent.')
    parser.add_argument('-radius', '--DROP_RADIUS', default=0.5, type=float,
                        help='The drop radius of the drive. Default 0.5.')
    parser.add_argument('-fraction', '--FRACTION', default=0.5, type=float,
                        help='The fraction of the drive release. Default 50%.')

    # Four types of drive drops
    parser.add_argument('-drop1', '--CIRCLE_DROP', default=True, type=bool,
                        help='Drop the drive in the middle of the population.')
    parser.add_argument('-drop2', '--UNIFORM_DROP', default=False, type=bool,
                        help='Drop the drive uniformly.')
    parser.add_argument('-drop3', '--CORNER_DROP', default=False, type=bool,
                        help='Drop the drive at the left bottom corner.')
    parser.add_argument('-drop4', '--LEFT_EDGE_HEMICIRCLE_DROP', default=False, type=bool,
                        help='Drop the drive at the middle of the left edge.')
    parser.add_argument('-drop5', '--LEFT_EDGE_DROP', default=False, type=bool,
                        help='Drop the drive along left edge.')

    # Explore the ecology parameters
    parser.add_argument('-migration', '--MOVEMENT_SPEED', default=0.04, type=float,
                        help='The movement speed of individuals.')
    parser.add_argument('-growth', '--LOW_DENSITY_GROWTH_RATE', default=6, type=int,
                        help='The benefits that wt individuals have over the drive individuals.')

    args_dict = vars(parser.parse_args())
    #print(args_dict)

    # The '-header' argument prints a header for the output. This can
    # help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("radius,fraction,invasiveness,suppressed_withoutChase,drive_lost_withoutChase,"\
            "suppressed_afterChase,drive_lost_afterChase,long_term_chase,"\
            "generation,rate_dr,rate_has_drive,rate_r2,ending population size,"\
            "gen_chase_started,avg_pop_during_chase,duration_of_chasing,avg_female_fertile")

    # Next, assemble the command line arguments in the way we want to for SLiM:
    clargs = configure_slim_command_line(args_dict)
    #print(clargs)

    # Run the file with the desired arguments.
    slim_outcome = run_slim(clargs)

    # Parse and analyze the result.
    slim_result = clargs[6] + "\n" + clargs[8] + "\n" + slim_outcome

    parsed_result = parse_slim(slim_result)

    # Print the result.
    print(parsed_result)


if __name__ == "__main__":
    main()
