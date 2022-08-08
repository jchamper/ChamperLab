from argparse import ArgumentParser
import subprocess

REPEATS=200
num = 0
filenum = 0

#defaults (can be changed by command line)
TOTAL_INDS = 10000
DROP_RADIUS = 0.3
DRIVE_FITNESS = 1.0
INTRODUCTION_FREQUENCY = 0.8
SPEED = 0.03
SPATIAL_LINEAR = False
DENSITY_INTERACTION_DISTANCE = 0.02

filename="spatial.slim"
csvname = None

def parse_slim(slim_string):
    #OUT: gen10 carrier, gen15 carrier
    output = []
    lines = slim_string.split('\n')
    for line in lines:
        if line.startswith("GEN"): #GEN10: 0.2
            output.append(line.split(":")[1])
    return output
    
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
        
    add("source",filename,str)
    add("DRIVE_FITNESS",DRIVE_FITNESS,float)
    add("INTRODUCTION_FREQUENCY",INTRODUCTION_FREQUENCY,float)
    add("TOTAL_INDS",TOTAL_INDS,float)
    add("SPEED",SPEED,float)
    add("DROP_RADIUS",DROP_RADIUS,float)
    add("SPATIAL_LINEAR",SPATIAL_LINEAR,bool)
    add("num",0,int)
    add("filenum",0,int)
    add("DENSITY_INTERACTION_DISTANCE",DENSITY_INTERACTION_DISTANCE,float)
    
    #############################
    #CSV columns: 0.TOTAL_INDS 1. drop radius
    # 2.g(15)-g(10) carrier 3. generation 10 carrier 4.generation 15 carrier 
    #############################

    args_dict = vars(parser.parse_args())
    global num, csvname, filenum
    num = args_dict.pop("num")
    filenum = args_dict.pop("filenum")
    csvname = str(filenum)+"/"+str(num)+".csv"
    clargs = configure_slim_command_line(args_dict)
    for _ in range(REPEATS):
        slim_result = run_slim(clargs)
        parsed_result = parse_slim(slim_result)
        g10,g15 = map(float,parsed_result)
        delta = str(g15-g10)

        
        
        with open(csvname, "a") as f:
            def write(string):
                f.write(str(args_dict[string])+",")
            write("TOTAL_INDS")
            write("DROP_RADIUS")
            f.write(delta+",")
            f.write(",".join(parsed_result))
            f.write("\n")
main()
