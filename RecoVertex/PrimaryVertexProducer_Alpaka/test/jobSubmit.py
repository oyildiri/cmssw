#!/usr/bin/env python3
import os
import re
import math
import time
import stat
import sys
print()
print('START')
print()
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization area #########

interval = 1           # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
queue = "workday"      # Queue to use See https://batchdocs.web.cern.ch/local/submit.html#job-flavours 
proxy_path = "/afs/cern.ch/user/o/oyildiri/private/x509up_u188570" # This is where your proxy will be held for access by batch system
doSubmit = True        # Uncomment for testing dry run
NumberOfJobs = -1

#logdir = "/eos/user/o/oyildiri/logfiles"

setParam = True

tag       = str(sys.argv[1]) # To identify the temporary run folder
workarea  = str(sys.argv[2]) # The place where your test scripts are, so we can cd there
script    = str(sys.argv[3]) # The script to execute with cmsRun
file_list = str(sys.argv[4]) # The txt with all input files
output    = str(sys.argv[5]) # Where do we put it
if setParam == True:
	param = str(sys.argv[6]) # Parameter in the algorithm that is set 

########   customization end   #########

# Set up proxy 
if not(os.path.isfile(proxy_path)):
	os.system("voms-proxy-init -voms cms --rfc -valid 192:00 --out %s"%proxy_path)
elif time.time() - os.stat(proxy_path)[stat.ST_MTIME] > 3600*24: # i.e. recreate proxy if it is more than one day old
 	os.system("voms-proxy-init -voms cms --rfc -valid 192:00 --out %s"%proxy_path)

# Get all files from txt
files = []
with open(file_list, 'r') as f:
	for line in f:
		files.append(line.strip())

print(files) 
os.system("mkdir %s"%output)

path = os.getcwd()
print()
print('do not worry about folder creation:')
os.system(f"rm -rf tmp{tag}")
os.system(f"rm -rf exec{tag}")
os.system(f"rm -rf batchlogs{tag}")
os.system(f"mkdir -p tmp{tag}")
os.system(f"mkdir -p exec{tag}")
print()

if NumberOfJobs == -1:
	NumberOfJobs = (len(files) + interval) // interval

##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs) + 1):
    ##### creates directory and file list for job #######
	jobFiles = files[max(0, (x - 1) * interval):min(x * interval, len(files))]
	with open(f'exec{tag}/job_{x}.sh', 'w') as fout:
		fout.write("#!/bin/sh\n")
		fout.write("echo\n")
		fout.write("echo\n")
		fout.write("echo 'START---------------'\n")
		fout.write("echo 'WORKDIR ' ${PWD}\n")
		fout.write("export HOME=$PWD\n")
		fout.write("export X509_USER_PROXY=/afs/cern.ch/user/o/oyildiri/private/x509up_u188570\n")
		fout.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		fout.write("cd %s\n"%workarea)
		fout.write("cmsenv\n")
		if setParam == True:
			for f in jobFiles:
				fout.write("cmsRun %s inputFiles=%s outputFile=%s param=%s\n"%(script, f, output + "/" + f.split("/")[-1].replace(".root","_output.root"),param))
		else: 
			for f in jobFiles:
				fout.write("cmsRun %s inputFiles=%s outputFile=%s\n"%(script, f, output + "/" + f.split("/")[-1].replace(".root","_output.root")))
		fout.write("echo 'STOP---------------'\n")
		fout.write("echo\n")
		fout.write("echo\n")
	os.system(f"chmod 755 exec{tag}/job_{x}.sh")

###### create submit.sub file ####
os.mkdir(f"batchlogs{tag}")
with open('submit.sub', 'w') as fout:
	fout.write("executable              = $(filename)\n")
	fout.write("arguments               = $(Proxy_path) $(ClusterId)$(ProcId)\n")
	fout.write(f"output                  = batchlogs{tag}/$(ClusterId).$(ProcId).out\n")
	fout.write(f"error                   = batchlogs{tag}/$(ClusterId).$(ProcId).err\n")
	fout.write(f"log                     = batchlogs{tag}/$(ClusterId).log\n")
	fout.write(f'+JobFlavour = "{queue}"\n')
	fout.write(f"x509userproxy = {proxy_path}\n")
#	fout.write('transfer_output_files = ""\n')
	fout.write("\n")
	fout.write(f"queue filename matching (exec{tag}/job_*sh)\n")

###### sends bjobs ######
os.system("echo submit.sub")
if doSubmit:
	if "eos" in os.getcwd(): # This is needed due to eos asynchronous nature. Spooling means that logs need to be requested instead of being written while running.
		os.system("condor_submit -spool submit.sub")
	else:
		os.system("condor_submit submit.sub")

print()
print("your jobs:")
os.system("condor_q")
print()
print('END')
