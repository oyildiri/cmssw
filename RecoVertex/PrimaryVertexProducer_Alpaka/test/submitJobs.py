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

if setParam == True:
	param_values = []
	if args.param_num == 1:
		param_values.append(args.param_min)
	else:
		dParam = (args.param_max - args.param_min)/(args.param_num - 1)
		for i in range(args.param_num):
			param_values.append(args.param_min + i*dParam)

# Check validity of algorithm and interaction names as arguments
algo_script = []
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

# Make the output directories and submit jobs
batch_nums = []
a_i = []
for i in inter:
	Path("%s/%s"%(mainpath,i)).mkdir(parents=True, exist_ok=True)
	for a in algo:
		if setParam == True:
			for p in param_values:
				a_i.append("%s_%s"%(a,i))
				# Make the directories
				outPath = "%s/%s/%s/outputfiles"%(mainpath,i,a)
				Path(outPath).mkdir(parents=True, exist_ok=True)
				runPath = "%s/run_p_%s"%(outPath, str(p))
				Path(runPath).mkdir(parents=True, exist_ok=True)
				# Submit the job
				subprocess.run(["python3","jobSubmit.py","%s_%s_p_%s"%(a,i,str(p)), "%s"%workarea, "%s/%s"%(workarea,get_algo_script(a)), "%s/%s"%(workarea, get_inter_file(i)), runPath, str(p)])
				result = subprocess.run(["condor_q",user], capture_output=True, text=True)
				print(get_batchnumber(result))
				batch_nums.append(get_batchnumber(result))
		else:
			a_i.append("%s_%s"%(a,i))
			# Make the directories
			outPath = "%s/%s/%s/outputfiles"%(mainpath,i,a)
			Path(outPath).mkdir(parents=True, exist_ok=True)
			runPath = "%s/run_%s"%(outPath, str(find_max_run(outPath,"run_")+1))
			Path(runPath).mkdir(parents=True, exist_ok=True)
			# Submit the job
			subprocess.run(["python3","jobSubmit.py","%s_%s"%(a,i), "%s"%workarea, "%s/%s"%(workarea,get_algo_script(a)), "%s/%s"%(workarea, get_inter_file(i)), runPath])
			result = subprocess.run(["condor_q",user], capture_output=True, text=True)
			print(get_batchnumber(result))
			batch_nums.append(get_batchnumber(result))
print(batch_nums)

