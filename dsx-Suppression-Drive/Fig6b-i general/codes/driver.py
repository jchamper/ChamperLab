#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 19:27:31 2024

@author: weizhechen
"""

from argparse import ArgumentParser
import subprocess
#import numpy as np 
#import sys

def parse_slim(slim_string):
    """
    Parse the output of SLiM to extract whatever data we're looking for.
    If we want to do a more complex analysis on the output of the SLiM file,
    this is where we do it.
    Args:
        slim_string: the entire output of a run of SLiM.
    Return
        output: the desired output we want from the SLiM simulation.
    """
    # The example SLiM file has been configured such that all the
    # output we want is printed on lines that start with "OUT:"
    # so we'll discard all other output lines."
    output = ""
    lines = slim_string.split('\n')
    suppressed = 0
    gen_suppressed = 10000
    gen = []
    adult = []
    adult_fe = []
    fertile_fe = []
    rate_dr = []
    has_dr = []
    
    not_suppressed = False
    whole_result=[]
    for line in lines:
        if line.startswith("SUPPRESSED:: "):
            spaced_line = line.split()
            suppressed = 1
            gen_suppressed = int(spaced_line[1])
            avg_gen = 0 
            avg_adult = 0
            avg_adult_fe = 0
            avg_fertile_fe = 0
            avg_rate_dr = 0
            avg_has_dr = 0            
            release = spaced_line[7]
            drive_conversion = spaced_line[8]

        if line.startswith("NOT:: "):
            not_suppressed = True
            spaced_line = line.split()
            release = spaced_line[7]
            drive_conversion = spaced_line[8]
    
    if(not_suppressed):
        for line in lines:
            if line.startswith("OUT:: "):               
                spaced_line = line.split()
                this_gen = int(spaced_line[1])
                gen.append(this_gen)
                sum_check = sum(gen[132:267])
                avg_gen = sum_check/135
                adult.append(int(spaced_line[2]))
                sum_adult = sum(adult[132:267])
                avg_adult = sum_adult/135
                adult_fe.append(int(spaced_line[3]))
                sum_adult_fe = sum(adult_fe[132:267])
                avg_adult_fe = sum_adult_fe/135
                fertile_fe.append(int(spaced_line[4]))
                sum_fertile_fe = sum(fertile_fe[132:267])
                avg_fertile_fe = sum_fertile_fe/135 
                rate_dr.append(float(spaced_line[5]))
                sum_dr = sum(rate_dr[132:267])
                avg_rate_dr = sum_dr/135 
                has_dr.append(float(spaced_line[6]))                
                sum_has_dr = sum(has_dr[132:267])               
                avg_has_dr = sum_has_dr/135
                
                
    whole_result = [suppressed, gen_suppressed, avg_gen, avg_adult, avg_adult_fe, avg_fertile_fe, avg_rate_dr, avg_has_dr, release, drive_conversion]
    output=','.join(str(i)for i in whole_result)
    return output


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
    # For debugging purposes:
    # std.out from the subprocess is in slim.communicate()[0]
    # std.error from the subprocess is in slim.communicate()[1]
    # Errors from the process can be printed with:
    # print(err)
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
    parser.add_argument('-src', '--source', default="fRIDL0402.slim", type=str,
                        help=r"SLiM file to be run. Default 'split.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
                        help='If this is set, python prints a header for a csv file.')

    # The all caps names of the following arguments must exactly match
    # the names of the constants we want to define in SLiM.
    parser.add_argument('-drop', '--RELEASE_RATIO', default= 4.0, type=float,
                        help='The drive homing rate. Default 100 percent.')
    parser.add_argument('-conversion', '--DRIVE_CONVERSION_RATE', default=0.0, type=float,
                        help='The resistance formation rate. Default 0 percent.')
    #parser.add_argument('-suppression', '--RECESSIVE_FEMALE_STERILE_SUPPRESSION', action='store_true',
                        #default=False, help='Toggles from modification drive to suppression drive.')

    args_dict = vars(parser.parse_args())

    # The '-header' argument prints a header for the output. This can
    # help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("suppressed, gen_suppressed, gen, adult, adult_fe, fertile_fe, rate_dr, has_dr, release, drive_conversion") 
        #print("Drive homing rate,Resistance formation rate,rate wt,rate dr," \
            #"rate of function preserving resistance,rate of function disrupting resistance," \
            #"rate of inds with at least 1 drive copy,ending pop size")

    # Next, assemble the command line arguments in the way we want to for SLiM:
    clargs = configure_slim_command_line(args_dict)
    #print(clargs[2])
    #print(clargs[4])
    # Run the file with the desired arguments.
    slim_outcome = run_slim(clargs)
    

    # Parse and analyze the result.
    parsed_result = parse_slim(slim_outcome)   
    slim_result = str(parsed_result)
    print(slim_result)


if __name__ == "__main__":
    main()
