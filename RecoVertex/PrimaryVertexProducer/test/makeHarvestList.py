import os
import sys

tag = str(sys.argv[1])
path = str(sys.argv[2])
file_list = str(sys.argv[3])
files_all = os.listdir(file_list)
files = [x for x in files_all if x.endswith("output_DQM.root")]
in_eos = True

print(len(files))

if in_eos == True:
	eospath = "root://eosuser.cern.ch/" + file_list
	with open("%s/%s_HarvestList.txt"%(path,tag), "w") as file:
		for f in files :
			if f == files[-1] :
				file.writelines("%s/%s\n"%(eospath, f))
				print("%s/%s"%(eospath, f))
				print(files.index(f))
			else :
				file.writelines("%s/%s\n"%(eospath, f))
				print("%s/%s"%(eospath, f))
				print(files.index(f))
else :
	with open("%s/%s_HarvestList.txt"%(path,tag), "w") as file:
                for f in files :
                        if f == files[-1] :
                                file.writelines("%s/%s\n"%(file_list, f))
                                print("%s/%s"%(file_list, f))
                                print(files.index(f))
                        else :
                                file.writelines("%s/%s\n"%(file_list, f))
                                print("%s/%s"%(file_list, f))
                                print(files.index(f))



