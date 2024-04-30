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
    gen=[]   
    
    #for target pop
    adult = []
    adult_fe = []
    fertile_fe = []
    rate_dr = []
    has_dr = []
    
    #for neighbor pop
    adult2 = []
    adult_fe2 = []
    fertile_fe2 = []
    rate_dr2 = []
    has_dr2 = []  

#NOT:: 267 2584 859 233 0.271875 0.54375 1345 593 319 0.111656 0.223312 2.0 0.0 0.05
#SUP:: 35  920  24  0   0.5      1.0     1186 537 305 0.228204 0.456407 2.0 1.0 0.05
#OUT1:: 33 950 66 3 0.497404 0.994807 
#OUT2:: 33 1217 560 302 0.224304 0.448609 
       
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
            release = spaced_line[12]
            conversion = spaced_line[13]
            migration=spaced_line[14]

        if line.startswith("NOT:: "):
            not_suppressed = True
            spaced_line = line.split()
            release = spaced_line[12]
            conversion = spaced_line[13]
            migration=spaced_line[14]           
                       
    if(not_suppressed):
        for line in lines:
            if line.startswith("OUT1:: "):               
                spaced_line = line.split()
                
                gen.append(int(spaced_line[1]))
                adult.append(int(spaced_line[2]))
                adult_fe.append(int(spaced_line[3]))               
                fertile_fe.append(int(spaced_line[4]))
                rate_dr.append(float(spaced_line[5]))                
                has_dr.append(float(spaced_line[6]))                
                                                           
                avg_gen = sum(gen[132:267])/135                
                avg_adult = sum(adult[132:267])/135
                avg_adult_fe = sum(adult_fe[132:267])/135
                avg_fertile_fe = sum(fertile_fe[132:267])/135
                avg_rate_dr = sum(rate_dr[132:267])/135
                avg_has_dr = sum(has_dr[132:267])/135
    
    #calculate the maximum drive frequency and minimum pop_size of non-target deme
    for line in lines:                   
        if line.startswith("OUT2:: "):      
            spaced_line = line.split()
            
            adult2.append(int(spaced_line[2]))                               
            adult_fe2.append(int(spaced_line[3]))
            fertile_fe2.append(int(spaced_line[4]))                               
            rate_dr2.append(float(spaced_line[5]))
            has_dr2.append(float(spaced_line[6]))        
            
            min_adult2 = min(adult2)
            min_adult_fe2 = min(adult_fe2)
            min_fertile_fe2 = min(fertile_fe2)
            max_rate_dr2 = max(rate_dr2)
            max_has_dr2 = max(has_dr2)
            
    whole_result = [suppressed,gen_suppressed, avg_gen, 
                    avg_adult, avg_adult_fe, avg_fertile_fe, avg_rate_dr, avg_has_dr,
                    min_adult2, min_adult_fe2, min_fertile_fe2, max_rate_dr2, max_has_dr2, 
                    release,conversion,migration]
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
    parser.add_argument('-src', '--source', default="full0402_RIDD_migration_uni.slim", type=str,
                        help=r"SLiM file to be run. Default 'split.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
                        help='If this is set, python prints a header for a csv file.')

    # The all caps names of the following arguments must exactly match
    # the names of the constants we want to define in SLiM.
    parser.add_argument('-drop', '--RELEASE_RATIO', default=1.0, type=float,
                        help='The drive homing rate. Default 100 percent.')
    parser.add_argument('-conversion', '--DRIVE_CONVERSION_RATE', default=0.0, type=float,
                        help='The resistance formation rate. Default 0 percent.')
    parser.add_argument('-migration', '--M', default=0.01, type=float,
                        help='The resistance formation rate. Default 0 percent.')
    #parser.add_argument('-suppression', '--RECESSIVE_FEMALE_STERILE_SUPPRESSION', action='store_true',
                        #default=False, help='Toggles from modification drive to suppression drive.')

    args_dict = vars(parser.parse_args())

    # The '-header' argument prints a header for the output. This can
    # help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("suppressed,gen_suppressed, avg_gen,avg_adult, avg_adult_fe, avg_fertile_fe, avg_rate_dr, avg_has_dr, min_adult2, min_adult_fe2, min_fertile_fe2, max_rate_dr2, max_has_dr2,release,conversion,migration")
        
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
