import json
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

parser = argparse.ArgumentParser()
parser.add_argument(
	"--var_by_tag",
	action="store_true"
)
args = parser.parse_args()

with open("timedata.json", "r") as f:
    TIME_LIST = json.load(f)
pltcolors = plt.rcParams['axes.prop_cycle'].by_key()['color']

INTER_LIST = []
SORTED_INTER_T = []
for T in TIME_LIST:
        inter = T[0][0]
        if inter not in INTER_LIST:
                INTER_LIST.append(inter)
                SORTED_INTER_T.append([inter, [T]])
        elif inter in INTER_LIST:
                loc = INTER_LIST.index(inter)
                SORTED_INTER_T[loc][1].append(T)
print(SORTED_INTER_T[0])
for i, ST in enumerate(SORTED_INTER_T):
        x_value = []
        y_value = []
        for S in ST[1]:
                if args.var_by_tag:
                        x_value.append(S[0][5])
                else:
                        x_value.append(S[0][1])
                y_value.append(S[1])
        plt.plot(x_value,y_value, label = f"{ST[0]}")
plt.xlabel("Algorithm")
plt.ylabel("time (s)")
plt.grid()
plt.legend()
plt.savefig("timeVsAlgo.png")
plt.show()


TAG_LIST = []
SORTED_TAG_T = []
for T in TIME_LIST:
        tag = [T[0][1],T[0][2],T[0][3],T[0][4]]
        if tag not in TAG_LIST:
                TAG_LIST.append(tag)
                SORTED_TAG_T.append([tag, [T]])
        elif tag in TAG_LIST:
                loc = TAG_LIST.index(tag)
                SORTED_TAG_T[loc][1].append(T)


bins = INTER_LIST
for TS in SORTED_TAG_T:
        values = []
        for i in INTER_LIST:
                values.append(None)
        for T in TS[1]:
                inter = T[0][0]
                loc = INTER_LIST.index(inter)
                values[loc] = T[1]
        print(bins)
        print(values)
        if TS[0][3] == None:
                plt.bar(bins, values, label = f"{TS[0][0]}")
        elif TS[0][3] != None:
                plt.bar(bins, values, label = f"{TS[0][0]}/param = {TS[0][3]}")
plt.xlabel("Interaction")
plt.ylabel("time (s)")
plt.legend()
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("timeVsInter.png")
plt.show()
