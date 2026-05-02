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
	"--group",
	nargs="+",
	type=str
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

parser.add_argument(
	"--params",
	nargs="+",
	type=float
)

parser.add_argument(
	"--omit_first_param",
	action="store_true"
)

parser.add_argument(
	"--run_path_list",
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
        if x == "TT" or x == "VBFHInv" or x == "Upsilon" or x == "QCD":
                return "%s.txt"%x
        elif x == "Z":
                return "Zmumu_16X.txt"
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
workarea = "/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_16_1_0_pre4/src/RecoVertex/PrimaryVertexProducer/test" # Wbere the interaction files and algorithm scripts are

# Check validity of algorithm and interaction names as arguments
#for i in args.algo:
#	if get_algo_script(i) == None:
#		print("Error: %s is not a valid algorithm name."%i)
#		sys.exit(1)
#	else :
#		print("%s algorithm name valid"%i)
#
#for i in args.inter:
#	if get_inter_file(i) == None:
#		print("Error: %s is not a valid interaction name."%i)
#		sys.exit(1)
#	else :
#		print("%s interaction name valid"%i)

# Read arguments
#inter = []
#for i in args.inter:
#	inter.append(i)
#algo = []
#for i in args.algo:
#	algo.append(i)
#algo_script = []

#rungroup = []
#for i in args.group:
#	rungroup.append(i)

if args.param_min != None or args.param_max != None or args.param_num != None or args.params != None:
	setParam = True
else:
	setParam = False

if setParam == True:
	param_values = []
	if args.params == None:
		if args.param_num == 1:
			param_values.append(args.param_min)
		else:
			dParam = (args.param_max - args.param_min)/(args.param_num - 1)
			for i in range(args.param_num):
				param_values.append(args.param_min + i*dParam)
	else:
		param_values = args.params

if args.omit_first_param == True:
	del param_values[0]

# Make run list
run_list = []
if args.run_path_list != None:
	try:
		with open(args.run_path_list) as list:
			for line in list:
				s = line.split("/")
				rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,s[0],s[1],s[2])
				if s[3] == "I":
					run_tag = str(find_max_run(rungroupPath,"run_")+1)
					run = [s[0], s[1], s[2], s[3], None, run_tag]
				elif s[3] == "P":
					run_tag = "p_%s"%str(s[4])
					run = [s[0], s[1], s[2], s[3], float(s[4]), run_tag]
				run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
				run_list.append(run)
	except:
		sys.exit(1)
else:
	for i in args.inter:
		for a in args.algo:
			for g in args.rungroup:
				if len(args.algo)>1 and  args.group.index(g) != args.inter.index(i)*len(args.algo)+args.algo.index(a):
					continue
				rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,i,a,g)
				if setParam == True:
					run_type = "P"
				else:
					run_type = "I"
				if run_type == "I":
					run_tag = str(find_max_run(rungroupPath,"run_")+1)
					run = [i, a, g, run_type, None, run_tag]
					run.append("%s/%s/RUNS_%s/run_%"%(run[0],run[1],run[2],run[5]))
					run_list.append(run)
				elif run_type == "P":
					for p in param_values:
						run_tag = "p_%s"%str(p)
						run = [i, a, g, run_type, p, run_tag]
						run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
						run_list.append(run)

# Make harvest lists
for r in run_list:
	runPath = "%s/%s"%(mainpath,r[6])
	subprocess.run(["python3","%s/makeHarvestList_new.py"%workarea, "%s"%runPath, "%s"%runPath])
# Harvest
cmssw_path = "/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_16_1_0_pre4/src"
for r in run_list:
	runPath = "%s/%s/%s/RUNS_%s/run_%s"%(mainpath,r[0],r[1],r[2],r[5])
	hlist = "HarvestList.txt"
	cmd = f"""
	cd {cmssw_path}
	eval "$(scramv1 runtime -sh)"
	cd {runPath}
	cmsRun {workarea}/harvester.py inputFileList={hlist}
	"""
	try:
		subprocess.run(cmd, shell=True, executable="/bin/bash", check=True)
	except:
		pass
