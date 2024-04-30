#!/usr/bin/env python3

#  Created by Sam Champer, 2020.
#  A product of the Messer Lab, http://messerlab.org/slim/

#  Sam Champer, Ben Haller and Philipp Messer, the authors of this code, hereby
#  place the code in this file into the public domain without restriction.
#  If you use this code, please credit SLiM-Extras and provide a link to
#  the SLiM-Extras repository at https://github.com/MesserLab/SLiM-Extras.
#  Thank you.


# This is an example of how to use Python as a driver for SLiM.
# Output is formated as a csv, but just printed to stdout by default.

# In order to reconfigure this file for your research project, the

# run_slim() and configure_slim_command_line() functions do not need to be modified.
# Changes you would likely want to make are to the argument parser in main(),
# in order to pass your desired variables to SLiM, and to the parse_slim()
# function, where you could do your desired operations on the output of SLiM.





from argparse import ArgumentParser
import subprocess
import pandas as pd
from math import ceil

#divide a list into several sub_lists

def chunk(lst, size):
  return list(map(lambda x: lst[x * size:x * size + size],
      list(range(0, ceil(len(lst) / size)))))


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
    lines = slim_string.split('\n')
    drive_carrier=[]
    pop_size=[]
    female=[]
    suppressed=0
    drop_size=[]
    suppress=[]
    for line in lines:
        if line.startswith("SUPPRESSED:"):
            suppressed=1
   
    for line in lines:
        if line.startswith("OUT:"):
            spaced_line = line.split()
            drive_carrier.append(spaced_line[6])
            pop_size.append(spaced_line[2])
            female.append(spaced_line[4])
            drop_size.append(spaced_line[7])
            suppress.append(suppressed)
            #output += line.split(":")[1]  # Discard the "OUT:" from the output line.
    
    #print(drop_size)
    #whole_result = [drive_carrier, pop_size, fertile_fe, drop_size]
    #output=','.join(str(i)for i in whole_result)
    df = pd.DataFrame({
        "drive_carrier": drive_carrier,
        "pop_size": pop_size,
        "fertile_female": female,
        "drop_size": drop_size,
        "suppressed": suppress
        })
    return df


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

# run_slim() and configure_slim_command_line()


def main(x):
    """
    1. Configure using argparse.
    2. Generate the command line list to pass to subprocess through the run_slim() function.
    3. Run SLiM.
    4. Process the output of SLiM to extract the information we want.
    5. Print the results.
    """
    # Get args from arg parser:
    for i in range(x):
      parser = ArgumentParser()
      parser.add_argument('-src', '--source', default="cagesplit0415.slim", type=str,
                          help=r"SLiM file to be run. Default 'dominant_sterile_with_ridl_guoedited(0711).slim'")

      parser.add_argument('-header', '--print_header', action='store_true', default=False,
                          help='If this is set, python prints a header for a csv file.')


# The all caps names of the following arguments must exactly match
# the names of the constants we want to define in SLiM.


#parameters that can vary in different simulations

##what I want from the ridd script:generations, drive frequency and pop size
    
    #parser.add_argument('-homing', '--HOMING_SUCCESS_RATE', default=1.0, type=float,
     #                   help='The drive homing rate. Default 100 percent.')
    #parser.add_argument('-res', '--RESISTANCE_FORMATION_RATE', default=0.0, type=float,
     #                   help='The resistance formation rate. Default 0 percent.')
    #parser.add_argument('-suppression', '--RECESSIVE_FEMALE_STERILE_SUPPRESSION', action='store_true',
     #                   default=False, help='Toggles from modification drive to suppression drive.')

      args_dict = vars(parser.parse_args())

    # The '-header' argument prints a header for the output. This can
    # help generate a nice CSV by adding this argument to the first SLiM run:
      if args_dict.pop("print_header", None):
          print("Drive homing rate,Resistance formation rate,rate wt,rate dr," \
              "rate of function preserving resistance,rate of function disrupting resistance," \
              "rate of inds with at least 1 drive copy,ending pop size")


    # Next, assemble the command line arguments in the way we want to for SLiM:
      clargs = configure_slim_command_line(args_dict)

    # Run the file with the desired arguments.
      slim_result = run_slim(clargs)
      

    # Parse and analyze the result.
      parsed_result = parse_slim(slim_result)
      
     
      filename=("RIDD",str(i), ".csv")
      name_file= "".join(filename)
      parsed_result.to_csv(name_file,encoding = "gbk") 
    


if __name__ == "__main__":
    
    main(20)
