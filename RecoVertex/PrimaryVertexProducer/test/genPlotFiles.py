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

# Make the output directories and submit jobs
batch_nums = []
a_i = []
for i in inter:
	Path("%s/%s"%(mainpath,i)).mkdir(parents=True, exist_ok=True)
	for a in algo:
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

# Wait for all jobs to be finished
try:
	while True:
		time.sleep(15)
		result = subprocess.run(["condor_q",user], capture_output=True, text=True)
		if "0 idle, 0 running" in result.stdout:
			print("Jobs finished")
			break
		subprocess.run(["condor_q",user])
except KeyboardInterrupt:
	print("\nInterrupted: Moving to the next step.")

# Move the batchlogs exec and tmp folders
for i in inter:
	for a in algo:
		outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
		runPath1 = "%s/run_%s"%(outPath1, str(find_max_run(outPath1,"run_")))
		shutil.move("%s/batchlogs%s_%s"%(workarea,a,i), "%s"%runPath1)
		shutil.move("%s/exec%s_%s"%(workarea,a,i), "%s"%runPath1)
		shutil.move("%s/tmp%s_%s"%(workarea,a,i), "%s"%runPath1)

# Make a report of the jobs
reportPath = "%s/jobreports"%mainpath
jobReport = open("%s/report_%s.txt"%(reportPath, (str(find_max_file(reportPath,"report_",".txt") + 1))), "w")

n_a = len(algo)
for i in inter:
	for a in algo:
		nI = inter.index(i) + 1
		nA = algo.index(a) + 1
		nB = (nI - 1) * n_a + nA
		sub_count = int(count_lines("%s/%s"%(workarea,get_inter_file(i))))
		result = subprocess.run(["condor_q",user], capture_output=True, text=True)
		result1 = result.stdout
		done_count_str = get_word_in_a_line(result1, "ID: ", 5)
		if done_count_str.isdigit():
			done_count = int(done_count_str)
		else:
			done_count = 0
		if sub_count == done_count:
			comp = "Completed"
		else:
			comp = "Not Completed"
		jobReport.write("%s %s_%s %i %i %s\n"%(batch_nums[nB-1], a, i, sub_count, done_count, comp))

# Make harvest lists
for i in inter:
	for a in algo:
		outPath1 = "%s/%s/%s/outputfiles"%(mainpath,i,a)
		runPath1 = "%s/run_%s"%(outPath1, str(find_max_run(outPath1,"run_")))
		subprocess.run(["python3","%s/makeHarvestList.py"%workarea, "%s_%s"%(a,i), "%s"%runPath1, "%s"%runPath1])
# Harvest
cmssw_path = "/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src"
for i in inter:
	for a in algo:
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
			hfile = "%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%workarea
