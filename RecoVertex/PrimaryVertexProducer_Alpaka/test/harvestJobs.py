import subprocess
import os 
import sys
import argparse
import time
import shutil
from pathlib import Path
import re

user = "oyildiri"

# Types of jobs
setParam = True # If setting a specific value for a parameter in the algorithm(s) or scanning over that parameter

# Arguments (--inter <inter1> <inter2> --algo <algo1> <algo2>)
parser = argparse.ArgumentParser()

parser.add_argument(
	"--inter",
	nargs="+",
	type=str,
	help="Interactions"
)

parser.add_argument(
	"--algo",
	nargs="+",
	type=str,
	help="Algorithm"
)

parser.add_argument(
        "--param_min",
        type=float,
        help="Minimum value of the set/scanned parameter"
)

parser.add_argument(
        "--param_max",
        type=float,
        help="Maximum value of the set/scanned parameter"
)

parser.add_argument(
        "--param_num",
        type=int,
        help="Number of scanned parameter values"
)
args = parser.parse_args()

# Funtions
def get_algo_script(x):
        if x == "oldColdF":
                return "testCPU_PU200_oldAlgo.py"
        elif x == "oldCnewF":
                return "testCPU_PU200_oldCnewF.py"
        elif x == "newColdF":
                return "testCPU_PU200_newColdF.py"
        elif x == "newCnewF":
                return "testCPU_PU200.py"
        elif x == "new2CnewF":
                return "testCPU_PU200_tkwt0p25.py"
        else:
             	return None

def get_inter_file(x):
        if x == "TT" or x == "Z" or x == "VBFHInv" or x == "Upsilon" or x == "QCD":
                return "%s.txt"%x
        else:
             	return None

def count_ls(dir,word):
	x = subprocess.run(["find","%s"%dir,"-maxdepth","1","-type","d","-name","%s"%word,"|","wc", "-l"],capture_output=True, text=True)
	return int(x) 

def find_max_run(dir,word):
	runs = []
	path = Path(dir)
	for i in path.iterdir():
		if i.name.startswith(word) and i.name.removeprefix(word).isdigit():
			runs.append(int(i.name.removeprefix(word)))
	if len(runs) == 0:
		x = 0
	else :
		x = max(runs)
	return x

def get_batchnumber(x):
	lines = x.stdout.splitlines()
	y = re.search(r"ID:\s+(\d+)", lines[-5])
	if y:
		batchnum = y.group(1)
		return batchnum

def count_lines(file):
	with open(file, "r") as f:
		line_count = sum(1 for _ in f)
	return line_count

def count_files(dir, name):
	direc = Path(dir)
	file_count = sum(1 for f in direc.glob(name) if f.is_file()) 
	return file_count

def find_max_file(dir,word,type):
	runs = []
	path = Path(dir)
	for i in path.iterdir():
		if i.name.startswith(word) and i.name.endswith(type):
			x1 = i.name.removeprefix(word)
			x2 = int(x1.removesuffix(type))
			runs.append(x2)
	if len(runs) == 0:
		x = 0 
	else :
		x = max(runs)
	return x

def get_word_in_a_line(x,key,pos):
	for line in x.splitlines():
		if key in line:
			parts = line.split()
	return parts[pos]
# Paths
mainpath = "/eos/user/o/oyildiri/OldNewCF" # Where the outputs go
workarea = "/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test" # Wbere the interaction files and algorithm scripts are

# Read arguments
inter = []
for i in args.inter:
	inter.append(i)
algo = []
for i in args.algo:
	algo.append(i)
algo_script = []

# Check validity of algorithm and interaction names as arguments
for i in algo:
	if get_algo_script(i) == None:
		print("Error: %s is not a valid algorithm name."%i)
		sys.exit(1)
	else :
		print("%s algorithm name valid"%i)

for i in inter:
	if get_inter_file(i) == None:
		print("Error: %s is not a valid interaction name."%i)
		sys.exit(1)
	else :
		print("%s interaction name valid"%i)

if setParam == True:
        param_values = []
        if args.param_num == 1:
                param_values.append(args.param_min)
        else:
                dParam = (args.param_max - args.param_min)/(args.param_num - 1)
                for i in range(args.param_num):
                        param_values.append(args.param_min + i*dParam)

# Make harvest lists
for i in inter:
	for a in algo:
		if setParam == True:
			for p in param_values:
				outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
				runPath1 = "%s/run_p_%s"%(outPath1, str(p))
				subprocess.run(["python3","%s/makeHarvestList.py"%workarea, "%s_%s_p_%s"%(a,i,str(p)), "%s"%runPath1, "%s"%runPath1])
		else:
			outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
			runPath1 = "%s/run_%s"%(outPath1, str(find_max_run(outPath1,"run_")))
			subprocess.run(["python3","%s/makeHarvestList.py"%workarea, "%s_%s"%(a,i), "%s"%runPath1, "%s"%runPath1])
# Harvest
cmssw_path = "/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src"
for i in inter:
	for a in algo:
		if setParam == True:
			for p in param_values:
				outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
				runPath1 = "%s/run_p_%s"%(outPath1, str(p))
				hlist = "%s/%s_%s_p_%s_HarvestList.txt"%(runPath1,a,i,str(p))
				cmd = f"""
				cd {cmssw_path}
				eval "$(scramv1 runtime -sh)"
				cd {runPath1}
				cmsRun {workarea}/harvester.py inputFileList={hlist}
				"""
				try:
					subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
				except:
					pass
		else:
			outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
			runPath1 = "%s/run_%s"%(outPath1, str(find_max_run(outPath1,"run_")))
			hlist = "%s/%s_%s_HarvestList.txt"%(runPath1,a,i)
			cmd = f"""
			cd {cmssw_path}
			eval "$(scramv1 runtime -sh)"
			cd {runPath1}
			cmsRun {workarea}/harvester.py inputFileList={hlist}
			"""
			try:
				subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
			except:
				pass
