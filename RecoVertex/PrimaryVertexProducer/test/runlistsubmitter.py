import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
	"--run_path_list",
	type=str
)
parser.add_argument(
	"--script",
	type=str
)
args = parser.parse_args()

script = args.script
run_path_list = args.run_path_list

N = 2
n = 13
foldernames = ["Hinv", "QCD", "TT", "TTto2l2nu", "Upsilon", "Wprimetolnu", "Wtolnu", "Wtomunu", "Zprimetoee", "Zprimetomm", "Ztoee", "Ztomm", "Ztott"]


firstlines = []
lastlines = []
j = 0
while j < n:
	firstlines.append(j*N+1)
	lastlines.append((j+1)*N)
	j = j+1
for i, f in enumerate(firstlines):
	l = lastlines[i]
	foldername = foldernames[i]
	subprocess.run(["python3", f"{script}", "--run_path_list", f"{run_path_list}", "--foldername", f"{foldername}", "--firstline", f"{f}", "--lastline", f"{l}"])
