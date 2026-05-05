from jobScriptsConfig import user, mainpath, workarea
from myFunctions import *
import subprocess
import os
import sys
import argparse
import time
import shutil
from pathlib import Path
import re

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
	"--omit_last_param",
	action="store_true"
)

parser.add_argument(
	"--run_path_list",
	type=str,
)

args = parser.parse_args()

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
if args.omit_last_param == True:
	del param_values[-1]

# Make run list
run_list = []
if args.run_path_list != None:
	try:
		with open(args.run_path_list) as list:
			for line in list:
				s = line.split("/")
				rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,s[0],s[1],s[2])
				if os.path.exists(rungroupPath)!= True:
					print(rungroupPath, ": Directory does not exist")
					sys.exit(1)
				if s[3] == "I":
					run_tag = str(find_max_run(rungroupPath,"run_"))
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
			for g in args.group:
				if len(args.algo)>1 and  args.group.index(g) != args.inter.index(i)*len(args.algo)+args.algo.index(a):
					continue
				rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,i,a,g)
				if os.path.exists(rungroupPath)!= True:
					print(rungroupPath, ": Directory does not exist")
					sys.exit(1)
				if setParam == True:
					run_type = "P"
				else:
					run_type = "I"
				if run_type == "I":
					run_tag = str(find_max_run(rungroupPath,"run_"))
					run = [i, a, g, run_type, None, run_tag]
					run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
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
