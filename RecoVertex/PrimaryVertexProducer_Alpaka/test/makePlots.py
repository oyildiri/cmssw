import subprocess
import os 
import sys
import argparse
import time
import shutil
from pathlib import Path
import re

user = "oyildiri"

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
	"--run_list",
	type=str,
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
        if x == "TT" or x == "Z" or x == "VBFHInv" or x == "Upsilon":
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
if args.run_list==None:
	inter = []
	for i in args.inter:
		inter.append(i)
	algo = []
	for i in args.algo:
		algo.append(i)
else:
	run_paths = []
	with open("run_p_list.txt", 'r') as file:
		for line in file:
			run_paths.append(line.strip())
	inter_0 = []
	for r in run_paths:
		main_pos = r.split("/").index("OldNewCF")
		inter_0.append(r.split("/")[main_pos+1])
	inter = sorted(set(inter_0))

	algo_0 = []
	for r in run_paths:
		main_pos = r.split("/").index("OldNewCF")
		algo_0.append(r.split("/")[main_pos+2])
	algo = sorted(set(algo_0))

	params_0 = []
	for r in run_paths:
		main_pos = r.split("/").index("OldNewCF")
		params_0.append(float(r.split("/")[main_pos+4].removeprefix("run_p_")))
	params = sorted(set(params_0))

# Check validity of algorithm and interaction names as arguments

if args.run_list==None:
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

	for i in inter:
		paths = []
		for a in algo:
			outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
			runPath1 = "%s/run_%s"%(outPath1, str(find_max_run(outPath1,"run_")))
			paths.append("%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%runPath1)
			print(paths)
		scriptpath="/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/bin/el9_amd64_gcc12/makeTrackValidationPlots.py"
		cmd = ["python3", "%s"%scriptpath] + paths + ["--png", "--extended"]
		subprocess.run(cmd)

else:
	paths = []
	for i in inter:
		for a in algo:
			for p in params:
				outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
				runPath1 = "%s/run_p_%s"%(outPath1, p)
				paths.append("%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%runPath1)
				print(paths)
	scriptpath="/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/bin/el9_amd64_gcc12/makeTrackValidationPlots.py"
	cmd = ["python3", "%s"%scriptpath] + paths + ["--png", "--extended"]
	subprocess.run(cmd)
