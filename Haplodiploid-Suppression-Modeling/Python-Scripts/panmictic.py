#Author: Sam Champer and Yiran Liu
from argparse import ArgumentParser
import subprocess
def parse_slim(slim_string):
    output: str = ""
    lines = slim_string.split('\n')
    for line in lines:
        if line.startswith("DATA:: "):
            output += line.split()[1]
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
    """
    1. Configure using argparse.
    2. Generate the command line list to pass to subprocess through the run_slim() function.
    3. Run SLiM.
    4. Process the output of SLiM to extract the information we want.
    5. Print the results.
    """
# Get args from arg parser:
    parser = ArgumentParser()
    parser.add_argument('-src', '--source', default=" panmictic.slim ", type=str,
    help=r"SLiM file to be run. Default 'panmictic.slim'")
    parser.add_argument('-header', '--print_header', action='store_true', default=False,
    help='If this is set, python prints a header for a csv file.')
    parser.add_argument('-embryores','--DRIVE_HETEROZYGOTE_EMBRYO_RESISTANCE_RATE', default=0.05, type=float)
    args_dict = vars(parser.parse_args())
# The '-header' argument prints a header for the output. This can
# help generate a nice CSV by adding this argument to the first SLiM run:
    if args_dict.pop("print_header", None):
        print("genetic_load,drive allele frequency,drive carrier frequency")
# Next, assemble the command line arguments in the way we want to for SLiM:
    clargs = configure_slim_command_line(args_dict)
# Run the file with the desired arguments.
    slim_result = run_slim(clargs)
# Parse and analyze the result.
    parsed_result = parse_slim(slim_result)
# Print the result.
    print(parsed_result)
if __name__ == "__main__":
    main()
