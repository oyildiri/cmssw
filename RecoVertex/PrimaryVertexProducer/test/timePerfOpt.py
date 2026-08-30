from jobScriptsConfig import user, mainpath, workarea
from myFunctions import *
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import os
from pathlib import Path
import shutil
import json

parser = argparse.ArgumentParser()
parser.add_argument(
	"--run_path_list",
	type=str,
)

args = parser.parse_args()

param_manual = False
runs_from_list = True

run_list = []

with open(args.run_path_list) as list:
	for line in list:
		s = line.strip().split("/")
		if line=="\n":
			continue
		rungroupPath = "%s/%s/%s/RUNS_%s"%(mainpath,s[0],s[1],s[2])
		if s[3] == "I":
			run_tag = str(find_max_run(rungroupPath,"run_"))
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
TIME_LIST = []
n = 0
N = len(run_list)
for r in run_list:
	n = n + 1
	runPath = "%s/%s/%s/RUNS_%s/run_%s"%(mainpath,r[0],r[1],r[2],r[5])
	for p in Path(runPath).iterdir():
		if p.name.startswith("batchlogs")==True:
			batchlogdirname = p.name
			break
	batchlogPath = "%s/%s"%(runPath, batchlogdirname)
	errlist = []
	for p in Path(batchlogPath).iterdir():
		if p.name.endswith(".err") == True:
			errlist.append(p.name)
	#with open("%s/%s"%(batchlogPath,errlist[0])) as f:
	#	for line in f:
	#		print(line)
	time_values = []
	for e in errlist:
		with open("%s/%s"%(batchlogPath,e)) as f:
			for line in f:
				if "offlinePrimaryVertices" in line  and "TimeReport" in line:
					parts = line.split()
					time = float(parts[1])
					time_values.append(time)
					break
	time_ave = sum(time_values)/len(time_values)
	frac = f"{n}/{N}"
	print(frac, " ---------- " , r ,"  ----------  ", time_ave)
	TIME_LIST.append([r, time_ave])

with open("timedata.json", "w") as f:
    json.dump(TIME_LIST, f)
