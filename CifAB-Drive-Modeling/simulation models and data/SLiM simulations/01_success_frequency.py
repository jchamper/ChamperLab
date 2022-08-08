from argparse import ArgumentParser
import subprocess
import math

REPEATS=200

num = 0
filenum = 0

#defaults (can be changed by command line)
SUBPOP_SIZE = 1000
FITNESS = 1.0
INTRODUCTION_FREQUENCY = 0.0
INTRODUCTION_A = 0.0
INTRODUCTION_B = 0.0
AB_TOGETHER = False
SAME_LOCI = False
SAME_LOCI_HETEROZYGOTE = False
DIFFERENT_LOCI = False
B_TOXIN = False
NOT_PER_ALLELE_FITNESS = False
DOMINANCE_COEFFICIENT = 1
EFFICIENCY_A = 1
EFFICIENCY_B = 1
MIGRATION = False
MIGRATION_RATE = 0.0

filename="panmictic.slim"
csvname = None

def parse_slim(slim_string):
    ret = "0"
    lines = slim_string.split('\n')
    for line in lines:
        if line.startswith("FIXED") or line.startswith("AFIXED"):
            ret = "1"
        elif line.startswith("LOST") or line.startswith("ALOST"):
            ret = "0"
    return ret
    
    


def run_slim(command_line_args):
    slim = subprocess.Popen(command_line_args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
    out, err = slim.communicate()
    if err:
        print(err)
    return out


def configure_slim_command_line(args_dict):
    clargs = "slim "
    source = args_dict.pop("source")
    for arg in args_dict:
        if isinstance(args_dict[arg], bool):
            clargs += f"-d {arg}={'T' if args_dict[arg] else 'F'} "
        else:
            clargs += f"-d {arg}={args_dict[arg]} "
    clargs += source
    return clargs.split()


def main():
    parser = ArgumentParser()
    def add(name,default_,type_):
        if type_ == bool:
            parser.add_argument("-"+name,action="store_true")
        else:
            parser.add_argument("-"+name,"--"+name, default = default_, type = type_)
        
    parser.add_argument("-PRINT_FREQUENCIES",action="store_false")
    add("source",filename,str)
    add("FITNESS",FITNESS,float)
    add("INTRODUCTION_FREQUENCY",INTRODUCTION_FREQUENCY,float)
    add("INTRODUCTION_A",INTRODUCTION_A,float)
    add("INTRODUCTION_B",INTRODUCTION_B,float)
    add("SUBPOP_SIZE",SUBPOP_SIZE,float)
    add("AB_TOGETHER",AB_TOGETHER,bool)
    add("SAME_LOCI",SAME_LOCI,bool)
    add("SAME_LOCI_HETEROZYGOTE",SAME_LOCI_HETEROZYGOTE,bool)
    add("DIFFERENT_LOCI",DIFFERENT_LOCI,bool)
    add("B_TOXIN",B_TOXIN,bool)
    add("NOT_PER_ALLELE_FITNESS",NOT_PER_ALLELE_FITNESS,bool)
    add("DOMINANCE_COEFFICIENT",DOMINANCE_COEFFICIENT,float)
    add("EFFICIENCY_A",EFFICIENCY_A,float)
    add("EFFICIENCY_B",EFFICIENCY_B,float)
    add("EFFICIENCY_FOR_BOTH",None,float)
    add("MIGRATION",MIGRATION,bool)
    add("MIGRATION_RATE",MIGRATION_RATE,float)
    add("num",0,int)
    add("filenum",0,int)
    
    #############################
    #CSV columns: 0.SUBPOP_SIZE 1.INTRO 2.fixed or not (1/0)
    #############################

    args_dict = vars(parser.parse_args())
    global num, csvname, filenum
    a = args_dict.pop("EFFICIENCY_FOR_BOTH")
    if a is not None:
        args_dict["EFFICIENCY_A"] = a
        args_dict["EFFICIENCY_B"] = a
    num = args_dict.pop("num")
    filenum = args_dict.pop("filenum")
    csvname = str(filenum)+"/"+str(num)+".csv"
    clargs = configure_slim_command_line(args_dict)
    for _ in range(REPEATS):
        slim_result = run_slim(clargs)
        parsed_result = parse_slim(slim_result)
        
        with open(csvname, "a") as f:
            def write(string):
                f.write(str(args_dict[string])+",")
            write("SUBPOP_SIZE")
            write("INTRODUCTION_FREQUENCY")
            f.write(parsed_result)
            f.write("\n")
main()
