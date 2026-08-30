from jobScriptsConfig import user, mainpath, workarea
import subprocess
import os 
import sys
import argparse
import time
import shutil
from pathlib import Path
import re
import glob

movelist=[]
for p in Path(workarea).iterdir():
	x = p.name
	if x.startswith("batchlogs"):
		tag = x.split("batchlogs")[1]
	elif x.startswith("exec"):
		tag = x.split("exec")[1]
	elif x.startswith("tmp"):
		tag = x.split("tmp")[1]
	else:
		continue
	s = tag.split("_")
	if s[0]=="":
		del s[0]
	print(s)
	if s[3] == "p":
		runType = "P"
		runTag = s[3]+'_'+str(s[4])
		param = float(s[4])
	elif s[3] == "True" or s[3]== "False":
		runType = "B2"
		runTag = str(s[3])+'_'+str(s[4])
		param = [s[3],s[4]]
	else:
		runType = "I"
		runTag = str(s[3])
		param = None
	run = [s[0], s[1], s[2], runType, param, runTag]
	print(run)
	run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
	movelist.append([tag, run])

for p in Path(workarea).iterdir():
	x = p.name
	if x.startswith("batchlogs"):
		tag = x.split("batchlogs")[1]
	elif x.startswith("exec"):
		tag = x.split("exec")[1]
	elif x.startswith("tmp"):
		tag = x.split("tmp")[1]
	else:
		continue
	for m in movelist:
		if m[0]==tag:
			destpath = "%s/%s"%(mainpath,m[1][6])
			print(destpath)
			result = subprocess.run(["ls", destpath], capture_output=True)
			if result.returncode == 0:
				destpath2 = f"{destpath}/{x}"
				result2 = subprocess.run(["ls", destpath2], capture_output=True)
				if result2.returncode == 0:
					shutil.move("%s/%s"%(workarea,x), "%s/lostlogs"%mainpath)
					print(x, " moved to ", "%s/lostlogs"%mainpath, " (Could not find appropriate run directory)")
				else:
					shutil.move("%s/%s"%(workarea,x), destpath)
					print(x, " moved to ", destpath)
				break
			else:
				try:
					shutil.move("%s/%s"%(workarea,x), "%s/lostlogs"%mainpath)
					print(x, " moved to ", "%s/lostlogs"%mainpath, " (Could not find appropriate run directory)")
					break
				except:
					continue
