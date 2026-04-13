import subprocess
import os 
import sys
import argparse
import time
import shutil
from pathlib import Path
import re
import glob

run_paths=[]
with open("run_rm_list.txt", 'r') as file:
	for line in file:
		run_paths.append(line.strip())

inter_0 = []
for r in run_paths:
	main_pos = r.split("/").index("OldNewCF")
	print(main_pos)
	inter_0.append(r.split("/")[main_pos+1])
inter = sorted(set(inter_0))

algo_0 = []
for r in run_paths:
	main_pos = r.split("/").index("OldNewCF")
	algo_0.append(r.split("/")[main_pos+2])
algo = sorted(set(algo_0))

runs_0 = []
for r in run_paths:
	main_pos = r.split("/").index("OldNewCF")
	runs_0.append(float(r.split("/")[main_pos+4].removeprefix("run_")))
runs = sorted(set(runs_0))


for i in inter:
	for a in algo:
		for r in runs:
			dir = "/eos/user/o/oyildiri/OldNewCF/%s/%s/run_%s/outputfiles"%(i,a,r)
			edmFiles =glob.glob(f"{dir}/*output.root")
			dqmFiles = glob.glob(f"{dir}/*DQM.root")
			if edmFiles:
				subprocess.run(["rm",*edmFiles])
			if dqmFiles:
				subprocess.run(["rm",*dqmFiles])
