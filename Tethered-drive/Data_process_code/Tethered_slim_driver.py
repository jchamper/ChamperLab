#Author: Ruobing Feng, Yiran Liu, Sam Champer and Isabel Kim
'''This script will use Python as a driver for SLiM and do the chase checking at the same time.'''
from argparse import ArgumentParser
import numpy as np
import subprocess
import sys




def parse_slim(slim_string):
    i = str(slim_string)
    line_space = i.split('\n')


    confined_chased = 0
    confined_gen_chase_started = 10000
    confined_gen_chase_ended = 0
    confined_gc_average = 10000
    confined_gc_variance = 10000
    confined_avg_pop_during_chase = 1000000
    confined_var_pop_during_chase = 1000000
    confined_avg_carrier_frequency_during_chase = 1000000
    confined_duration_of_chasing = 10000
    confined_drive_lost = 0
    confined_drive_success = 0
    gen_confined_drive_success = 10000
    gen_confined_drive_lost = 10000
    #equilibrium = 0
    #gen_equilibrium = 10000
    r1_resistance = 0
    gen_r1_resistance = 10000
    capacity = 10000
    confined_drive_frequency = []
    confined_drive_avg_frequency_in_last_100_generations = 10000
    confined_check_chasing = False

    suppressed = 0
    gen_suppressed = 10000
    suppression_chased = 0
    suppression_gen_chase_started = 10000
    suppression_gen_chase_ended = 0
    suppression_gc_average = 10000
    suppression_gc_variance = 10000
    suppression_avg_pop_during_chase = 1000000
    suppression_var_pop_during_chase = 1000000
    suppression_avg_carrier_frequency_during_chase = 1000000
    suppression_duration_of_chasing = 10000
    suppression_drive_lost = 0
    gen_suppression_drive_lost = 10000
    #equilibrium = 0
    #gen_equilibrium = 10000
    stopped_1000 = 0
    rate_at_stop = 10000
    hrate_at_stop = 10000
    hr1_resistance = 0
    gen_hr1_resistance = 10000
    capacity = 10000
    suppression_drive_frequency = []
    suppression_drive_avg_frequency_in_last_100_generations = 10000
    suppression_check_chasing = False
    avg_female_fertile = 1000000
    number_of_fertile_females = []


    



    

    for line in line_space:
    
        if line.startswith("HOMS_EMBRYO_CUT:: "):
            spaced_line = line.split()
            HOMSembryocut = float(spaced_line[1])
            
        if line.startswith("HOMS_CONVERSION_RATE:: "):
            spaced_line = line.split()
            HOMSconversionrate = float(spaced_line[1])

        if line.startswith("LOW_DENSITY_GROWTH_RATE:: "):
            spaced_line = line.split()
            Lowdensitygrowthrate = float(spaced_line[1])
            
        if line.startswith("AVERAGE_DISTANCE:: "):
            spaced_line = line.split()
            Averagedistance = float(spaced_line[1])
            
        if line.startswith("FERTILE_FEMALE:: "):
            spaced_line = line.split()
            number_of_fertile_females.append(int(spaced_line[1]))

        if line.startswith("TARE_DRIVE_PREDICTION:: "):
            spaced_line = line.split()
            TAREprediction = float(spaced_line[1])
            
        if line.startswith("HOMS_DRIVE_PREDICTION:: "):
            spaced_line = line.split()
            HOMSprediction = float(spaced_line[1])

        if line.startswith("HOMS_DROP_GEN:: "):
            spaced_line = line.split()
            HOMSdropgen = float(spaced_line[1])

    
        if line.startswith("CONFINED_DRIVE_SUCCESS:: "):  #confined drive success occurs, end
            spaced_line = line.split()
            confined_drive_success = 1
            gen_confined_drive_success = int(spaced_line[1])
            
        if line.startswith("CONFINED_DRIVE_LOST:: "):  #confined drive lost occurs, end
            spaced_line = line.split()
            confined_drive_lost = 1
            gen_confined_drive_lost = int(spaced_line[1])
            
        if line.startswith("CONFINED_RESISTANCE:: "): #resistance allele formation
            spaced_line = line.split()
            r1_resistance = 1
            gen_r1_resistance = int(spaced_line[1])
            
        if line.startswith("CONFINED_DRIVE_FREQUENCY:: "):
            spaced_line = line.split()
            confined_drive_frequency.append(float(spaced_line[1]))
            
        if line.startswith("CONFINED_POTENTIAL_CHASE:: "):
            confined_check_chasing = True
            
            
            
        if line.startswith("SUPPRESSED:: "):  #suppression occurs
            spaced_line = line.split()
            suppressed = 1
            gen_suppressed = int(spaced_line[1])
            
        if line.startswith("SUPPRESSION_DRIVE_LOST:: "):  #confined drive lost occurs, end
            spaced_line = line.split()
            suppression_drive_lost = 1
            gen_suppression_drive_lost = int(spaced_line[1])
            
        if line.startswith("SUPPRESSION_DRIVE_FREQUENCY:: "):
            spaced_line = line.split()
            suppression_drive_frequency.append(float(spaced_line[1]))
            
        if line.startswith("SUPPRESSION_POTENTIAL_CHASE:: "):
            suppression_check_chasing = True
            
        if line.startswith("ENDING_AFTER_1000:: "):
            spaced_line = line.split()
            stopped_1000 = 1
            rate_at_stop = float(spaced_line[1])
            hrate_at_stop = float(spaced_line[2])#show the rate of individuals with drive
            confined_drive_frequency_of_interest = confined_drive_frequency[-100:]
            confined_drive_avg_frequency_in_last_100_generations = np.average(confined_drive_frequency_of_interest)
            suppression_drive_frequency_of_interest= suppression_drive_frequency[-100:]
            suppression_drive_avg_frequency_in_last_100_generations = np.average(suppression_drive_frequency_of_interest)
            
            
            
        if line.startswith("SUPPRESSION_RESISTANCE:: "): #resistance allele formation
            spaced_line = line.split()
            hr1_resistance = 1
            gen_hr1_resistance = int(spaced_line[1])


            
            
    if (confined_check_chasing):
        # only will have chasing if we find a wt allele minimum and a green's
        # coefficient maximum
        wt_min = False
        eq_check = 0.8 * 2 * capacity
        wt = []
        gen = []
        pops = []
        gcs = []
        carrier_frequency = []
        #overall_gcs = []
        for line in line_space:
            if line.startswith("CONFINED_WT_ALLELES:: "):
                spaced_line = line.split()
                num_wt_alleles = int(spaced_line[1])
                this_gen = int(spaced_line[2])
                this_popsize = int(spaced_line[3])
                this_gc = float(spaced_line[5])# gc space here
                this_carrier_frequency = float(spaced_line[6])
                #this_overall_gc = float(spaced_line[5])
                wt.append(num_wt_alleles)
                gen.append(this_gen)  # Creates a generations list
                pops.append(this_popsize)
                gcs.append(this_gc)
                carrier_frequency.append(this_carrier_frequency)
                #overall_gcs.append(this_overall_gc)

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
                            confined_chased = 1
                            gen_gc_max = gen[i]
                            confined_gen_chase_started = min(gen_gc_max, gen_wt_min)
                            pos = gen.index(confined_gen_chase_started)
                            # summary stats of chase:
                            gcs_of_interest = gcs[(pos + 3):-2]
                            confined_gc_average = np.average(gcs_of_interest)
                            confined_gc_variance = np.var(gcs_of_interest)
                            popsizes_of_interest = pops[(pos + 3):-2]
                            carrier_frequency_of_interest = carrier_frequency[(pos + 3):-2]
                            confined_avg_carrier_frequency_during_chase = np.average(carrier_frequency_of_interest)
                            #female_fertile_of_interest = number_of_fertile_females[(pos + 3):-2]
                            confined_avg_pop_during_chase = np.average(popsizes_of_interest)
                            confined_var_pop_during_chase = np.var(popsizes_of_interest)
                            
                            #avg_female_fertile = 10000 if len(female_fertile_of_interest) == 0 else np.average(female_fertile_of_interest)
                            #overall_gcs_of_interest = overall_gcs[(pos + 3):-2]
                            #overall_gc_average = np.average(overall_gcs_of_interest)
                            #overall_gc_variance = np.var(overall_gcs_of_interest)
                            confined_gen_chase_ended = gen[-1]
                            confined_duration_of_chasing = gen[-1] - confined_gen_chase_started  # index of the last generation - confined_gen_chase_started
                        
                            break
                            
                            
    if (suppression_check_chasing):
        # only will have chasing if we find a wt allele minimum and a green's
        # coefficient maximum
        wt_min = False
        eq_check = 0.8 * 2 * capacity
        wt = []
        gen = []
        pops = []
        gcs = []
        carrier_frequency = []
        #overall_gcs = []
        for line in line_space:
            if line.startswith("SUPPRESSION_WT_ALLELES:: "):
                spaced_line = line.split()
                num_wt_alleles = int(spaced_line[1])
                this_gen = int(spaced_line[2])
                this_popsize = int(spaced_line[3])
                this_gc = float(spaced_line[5])  # gc space here
                this_carrier_frequency = float(spaced_line[6])
                #this_overall_gc = float(spaced_line[5])
                wt.append(num_wt_alleles)
                gen.append(this_gen)  # Creates a generations list
                pops.append(this_popsize)
                gcs.append(this_gc)
                carrier_frequency.append(this_carrier_frequency)
                #overall_gcs.append(this_overall_gc)

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
                            suppression_chased = 1
                            gen_gc_max = gen[i]
                            suppression_gen_chase_started = min(gen_gc_max, gen_wt_min)
                            pos = gen.index(suppression_gen_chase_started)
                            # summary stats of chase:
                            gcs_of_interest = gcs[(pos + 3):-2]
                            suppression_gc_average = np.average(gcs_of_interest)
                            suppression_gc_variance = np.var(gcs_of_interest)
                            popsizes_of_interest = pops[(pos + 3):-2]
                            female_fertile_of_interest = number_of_fertile_females[(pos + 3):-2]
                            #female_fertile_of_interest_1 = (",".join(map(str,female_fertile_of_interest))).replace(","," ")
                            #popsizes_of_interest_1 = (",".join(map(str,popsizes_of_interest))).replace(","," ")
                            #number_of_fertile_females_1= (",".join(map(str,number_of_fertile_females))).replace(","," ")
                            suppression_avg_pop_during_chase = np.average(popsizes_of_interest)
                            suppression_var_pop_during_chase = np.var(popsizes_of_interest)
                            avg_female_fertile = np.average(female_fertile_of_interest)
                            carrier_frequency_of_interest = carrier_frequency[(pos + 3):-2]
                            suppression_avg_carrier_frequency_during_chase = np.average(carrier_frequency_of_interest)
                            #overall_gcs_of_interest = overall_gcs[(pos + 3):-2]
                            #overall_gc_average = np.average(overall_gcs_of_interest)
                            #overall_gc_variance = np.var(overall_gcs_of_interest)
                            suppression_gen_chase_ended = gen[-1]
                            suppression_duration_of_chasing = gen[-1] - suppression_gen_chase_started  # index of the last generation - suppression_gen_chase_started
                            break
                  
    
    return HOMSembryocut, HOMSconversionrate, Lowdensitygrowthrate, Averagedistance, suppressed, gen_suppressed, TAREprediction, HOMSprediction, HOMSdropgen, confined_chased, confined_gen_chase_started, confined_gen_chase_ended, confined_duration_of_chasing, confined_gc_average, confined_gc_variance, confined_avg_pop_during_chase, confined_var_pop_during_chase, confined_avg_carrier_frequency_during_chase, confined_drive_success, gen_confined_drive_success, confined_drive_lost, gen_confined_drive_lost, r1_resistance, gen_r1_resistance, suppression_chased, suppression_gen_chase_started, suppression_gen_chase_ended, suppression_duration_of_chasing, suppression_gc_average, suppression_gc_variance, suppression_avg_pop_during_chase, suppression_var_pop_during_chase, suppression_avg_carrier_frequency_during_chase, suppression_drive_lost, gen_suppression_drive_lost, hr1_resistance, gen_hr1_resistance, avg_female_fertile, stopped_1000, rate_at_stop, hrate_at_stop, confined_drive_avg_frequency_in_last_100_generations, suppression_drive_avg_frequency_in_last_100_generations 
    
def run_slim(command_line_args,record_file_name):#new record_file_name
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
    lines = out.split("\n")
    with open(record_file_name,'a') as f:
        # get the change of drive frequency with generation
        for line in lines:
            if line.startswith("SLICE:: "):
                f.write(line.replace("SLICE:: ","")+"\n")
                # print(line)
            '''
            if line.startswith("PYTHON::"):
                f.write(line.replace("PYTHON:: ","")+"\n")
            '''
    return out
    #return
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
# Add each argument from arg parser to the command line arguemnts for SLiM: parameter remarks
    for arg in args_dict:
        #print(arg)
        if isinstance(args_dict[arg], bool):
            clargs += f"-d {arg}={'T' if args_dict[arg] else 'F'} "
        else:
            clargs += f"-d {arg}={args_dict[arg]} "
        #print(clargs)
# Add the source file, and return the string split into a list.
    clargs += source
    return clargs.split()
def main():
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default="Tethered_drive_1D_middle.slim", type=str,
    help=r"SLiM file to be run. Default 'Tethered_drive_1D_middle.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
    help='If this is set, python prints a header for a csv file.')
    parser.add_argument('-HOMSembryocut','--EMBRYO_RESISTANCE_CUT_RATE_HOM', default=0.00, type=float)
    parser.add_argument('-HOMSconversionrate','--HOMING_PHASE_CUT_RATE', default=1.00, type=float)
    parser.add_argument('-r','--recordfile',type=str) #new line/ another output
    #parser.add_argument('-Lowdensitygrowthrate','--GROWTH_AT_ZERO_DENSITY', default=6.00, type=float)
    #parser.add_argument('-Averagedistance','--AVERAGE_DISTANCE', default=0.05, type=float)
    #parser.add_argument('-TAREembryocut','--EMBRYO_RESISTANCE_RATE_TARE', default=1.00, type=float)
    #parser.add_argument('-migrationvalue','--SPEED', default=0.04, type=float)
    #parser.add_argument('-lowdensity','--GROWTH_AT_ZERO_DENSTITY', default=6.0, type=float)
    #parser.add_argument('-fitness','--DRIVE_FITNESS_VALUE', default=1.0, type=float)
    #parser.add_argument('-conversion','--DRIVE_CONVERSION_RATE', default=0.95, type=float)
    args_dict = vars(parser.parse_args())
    #record_file_name = options.record_arg or record_file_name_init #new line/ another output
# The '-header' argument prints a header for the output. This can
# help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("HOMSembryocut, HOMSconversionrate, Lowdensitygrowthrate, Averagedistance, suppressed, gen_suppressed, TAREprediction, HOMSprediction, HOMSdropgen, confined_chased, confined_gen_chase_started, confined_gen_chase_ended, confined_duration_of_chasing, confined_gc_average, confined_gc_variance, confined_avg_pop_during_chase, confined_var_pop_during_chase, confined_avg_carrier_frequency_during_chase, confined_drive_success, gen_confined_drive_success, confined_drive_lost, gen_confined_drive_lost, r1_resistance, gen_r1_resistance, suppression_chased, suppression_gen_chase_started, suppression_gen_chase_ended, suppression_duration_of_chasing, suppression_gc_average, suppression_gc_variance, suppression_avg_pop_during_chase, suppression_var_pop_during_chase, suppression_avg_carrier_frequency_during_chase, suppression_drive_lost, gen_suppression_drive_lost, hr1_resistance, gen_hr1_resistance, avg_female_fertile, stopped_1000, rate_at_stop, hrate_at_stop, confined_drive_avg_frequency_in_last_100_generations, suppression_drive_avg_frequency_in_last_100_generations")
    
    # unified argument and option; new line
    record_file_name=args_dict.pop("recordfile")
    if record_file_name == None:
        record_file_name = "record_file.csv"
# Next, assemble the command line arguments in the way we want to for SLiM:
    clargs = configure_slim_command_line(args_dict)
# Run the file with the desired arguments.
    slim_result = run_slim(clargs,record_file_name)#new record_file_name
# Parse and analyze the result.
    parsed_result = parse_slim(slim_result)
    print(parsed_result)   


if __name__ == "__main__":
    main()
