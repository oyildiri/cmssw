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

# Check validity of algorithm and interaction names as arguments

#algo_script = []
#for i in args.algo:
#        if get_algo_script(i) == None:
#                print("Error: %s is not a valid algorithm name."%i)
#                sys.exit(1)
#        else :
#              	print("%s algorithm name valid"%i)
#
#for i in args.inter:
#        if get_inter_file(i) == None:
#                print("Error: %s is not a valid interaction name."%i)
#                sys.exit(1)
#        else :
#              	print("%s interaction name valid"%i)

# Read arguments
if args.run_path_list == None:
	if args.param_min != None or args.param_max != None or args.param_num != None or args.params != None:
		ParamJobs = True 
	else:
		ParamJobs = False
else:
	ParamJobs = False

if args.run_path_list == None and ParamJobs == True:
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
	with open(args.run_path_list) as list:
		for line in list:
			s = line.rstrip().split("/")
			rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,s[0],s[1],s[2])
			if os.path.exists(rungroupPath)!= True:
				Path(rungroupPath).mkdir(parents=True, exist_ok=True)
			if s[3] == "I":
				run_tag = str(find_max_run(rungroupPath,"run_")+1)
				run = [s[0], s[1], s[2], s[3], None, run_tag]
			elif s[3] == "P":
				run_tag = "p_%s"%str(s[4])
				run = [s[0], s[1], s[2], s[3], float(s[4]), run_tag]
			elif s[3] == "B2":
				if s[4]=="True":
					bool1 = True
				elif s[4]=="False":
					bool1 = False
				else:
					sys.exit(1)
				if s[5]=="True":
					bool2 = True
				elif s[5]=="False":
					bool2 = False
				else:
					sys.exit(1)
				run_tag = "%s_%s"%(str(s[4]),str(s[5]))
				run = [s[0], s[1], s[2], s[3], [bool1, bool2], run_tag]
			run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
			run_list.append(run)
else:
	for i in args.inter:
		for n, a in enumerate(args.algo):
			for m,  g in enumerate(args.group):
				if len(args.algo) > 1 and n != m:
					continue
				rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,i,a,g)
				if os.path.exists(rungroupPath)!= True:
					Path(rungroupPath).mkdir(parents=True, exist_ok=True)
				if ParamJobs == True:
					run_type = "P"
				else:
					run_type = "I"
				if run_type == "I":
					run_tag = str(find_max_run(rungroupPath,"run_")+1)
					run = [i, a, g, run_type, None, run_tag]
					run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
					run_list.append(run)
				elif run_type == "P":
					for p in param_values:
						run_tag = "p_%s"%str(p)
						run = [i, a, g, run_type, p, run_tag]
						run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
						run_list.append(run)
# Make directories and run
JOBS = []
batch_nums = []
for r in run_list:
	runPath = "%s/%s"%(mainpath,r[6])
	Path(runPath).mkdir(parents=True, exist_ok=True)
	if r[3] == "P":
		subprocess.run(["python3","jobSubmit.py","%s_%s_%s_%s"%(r[0],r[1],r[2],r[5]), "%s"%workarea, "%s/%s"%(workarea,get_algo_script(r[1])), "%s/%s"%(workarea, get_inter_file(r[0])), runPath, "P", str(r[4])])
	elif r[3] == "I":
		subprocess.run(["python3","jobSubmit.py","%s_%s_%s_%s"%(r[0],r[1],r[2],r[5]), "%s"%workarea, "%s/%s"%(workarea,get_algo_script(r[1])), "%s/%s"%(workarea, get_inter_file(r[0])), runPath,"I"])
	elif r[3] == "B2":
		subprocess.run(["python3","jobSubmit.py","%s_%s_%s_%s"%(r[0],r[1],r[2],r[5]), "%s"%workarea, "%s/%s"%(workarea,get_algo_script(r[1])), "%s/%s"%(workarea, get_inter_file(r[0])), runPath, "B2", str(r[4][0]),  str(r[4][1])])
	result = subprocess.run(["condor_q",user], capture_output=True, text=True)
	print(get_batchnumber(result))
	batch_nums.append(get_batchnumber(result))
	job = [r,get_batchnumber(result)]
	JOBS.append(job)
for j in JOBS:
	print("%s %s %s %s %s %s JOB ID: %s"%(str(j[0][0]), str(j[0][1]), str(j[0][2]), str(j[0][3]), str(j[0][4]), str(j[0][5]), str(j[1]) ))

