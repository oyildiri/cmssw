import ROOT
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import os
from pathlib import Path
import shutil
import json
ROOT.gROOT.SetBatch(False)

parser = argparse.ArgumentParser()
parser.add_argument(
	"--run_path_list",
	type=str,
)

parser.add_argument(
	"--outputfile",
	type=str
)
args = parser.parse_args()

mainpath="/eos/user/o/oyildiri/OldNewCF"
workarea="/afs/cern.ch/user/o/oyildiri/private/CMS/CMSSW_15_0_4/src/RecoVertex/PrimaryVertexProducer_Alpaka/test"

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

# HISTOGRAMS

HIST = [
    "GenAllAssoc2RecoMatched_NumTracks",
    "effic_vs_NumTracks",
    "RecoAllAssoc2Gen_NumTracks",
    "fakerate_vs_NumTracks",
    "TruePVLocationIndexCumulative",
    "RecoPVAssoc2GenPVMatched_ResolZ",
    "RecoPVAssoc2GenPVMatched_ResolX",
    "RecoPVAssoc2GenPVMatched_ResolY",
    "RecoAllAssoc2GenMatched_ResolZ",
    "RecoAllAssoc2GenMatched_ResolX",
    "RecoAllAssoc2GenMatched_ResolY",
    "RecoAllAssoc2GenMatchedMerged_ResolZ",
    "RecoAllAssoc2GenMatchedMerged_ResolX",
    "RecoAllAssoc2GenMatchedMerged_ResolY",
    "RecoAllAssoc2Gen_X",
    "RecoAllAssoc2Gen_Y"
]

HIST_P = [
    "GenAllAssoc2RecoMatched_NumTracks",
    "effic_vs_NumTracks",
    "RecoAllAssoc2Gen_NumTracks",
    "fakerate_vs_NumTracks",
    "TruePVLocationIndexCumulative",
    "RecoPVAssoc2GenPVMatched_ResolZ",
    "RecoPVAssoc2GenPVMatched_ResolX",
    "RecoPVAssoc2GenPVMatched_ResolY",
    "RecoAllAssoc2GenMatched_ResolZ",
    "RecoAllAssoc2GenMatched_ResolX",
    "RecoAllAssoc2GenMatched_ResolY",
    "RecoAllAssoc2GenMatchedMerged_ResolZ",
    "RecoAllAssoc2GenMatchedMerged_ResolX",
    "RecoAllAssoc2GenMatchedMerged_ResolY"
]

P_PLOTS_BLOCK = [
    "e_glob",
    "f_glob",
    "f_glob_lowntrk_highntrk",
    "pv_tag",
    "res"
]

# Don't forget to add the functions

# Runs
run_list = []

with open(args.run_path_list) as list:
	for line in list:
		s = line.rstrip().split("/")
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

def sum_in_bins(H,runs):
	h_run_list = []
	for r in runs:
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%r[6])
		if r[1] == "4D" or r[1] == "4DinBlocks":
			h_run = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices4D/%s"%H)
		else:
			h_run = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/%s"%H)
		h_run.SetDirectory(0)
		h_run_list.append(h_run)
	sums = []
	for i in range(1, h_run_list[0].GetNbinsX()+1):
		ysum = 0
		for j in range(len(h_run_list)):
			ysum = ysum + h_run_list[j].GetBinContent(i)
		sums.append(ysum)
	return sums

def min_index(list,index_left, index_right,nonzero=True):
	for i in enumerate(list):
		if i[0]<index_left or i[0]>index_right:
			del list[i[0]]
	if nonzero == True:
		min_list = min(x for x in list if x > 0)
	else:
		min_list = min(list)
	min_index = list.index(min_list)
	return min_index

RUN_HISTP_RESULTS = []
for r in run_list:
	print("run: ",r)
	f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%str(r[6]))
	runHists = []
	for HP in enumerate(HIST_P):
		print(HP[1])
		if r[1] == "4D" or r[1] == "4DinBlocks":
			h = f.Get(f"DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices4D/{HP[1]}")
		else:
			h = f.Get(f"DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/{HP[1]}")
		h.SetDirectory(0)
		runHists.append([HP[1],h])
	runResults = []
	for v in enumerate(P_PLOTS_BLOCK):
		if v[1]=="e_glob":
			h_N = runHists[HIST_P.index("GenAllAssoc2RecoMatched_NumTracks")][1]
			h_eff = runHists[HIST_P.index("effic_vs_NumTracks")][1]
			num = 0
			denom = 0
			for j in range(0, h_N.GetNbinsX()+2):
				N =  h_N.GetBinContent(j)
				eff = h_eff.GetBinContent(j)
				if eff == 0:
					continue
				num = num + N
				denom = denom + N/eff
			result = num/denom
		elif v[1]=="f_glob":
			h_Nrec = runHists[HIST_P.index("RecoAllAssoc2Gen_NumTracks")][1]
			h_fake = runHists[HIST_P.index("fakerate_vs_NumTracks")][1]
			num = 0
			denom = 0
			for j in range(1, h_Nrec.GetNbinsX()+1):
				Nrec = h_Nrec.GetBinContent(j)
				fake = h_fake.GetBinContent(j)
				if fake == 0:
					continue
				num = num + fake * Nrec
				denom = denom + Nrec
			result = num/denom
		elif v[1]=="f_glob_lowntrk_highntrk":
			sums = sum_in_bins("fakerate_vs_NumTracks", run_list)
			minindex = min_index(sums,0,100) + 1
#			print("min_index = ", minindex)
			h_Nrec = runHists[HIST_P.index("RecoAllAssoc2Gen_NumTracks")][1]
			h_fake = runHists[HIST_P.index("fakerate_vs_NumTracks")][1]
			num = 0
			denom = 0
			for j in range(1, minindex+1):
				Nrec = h_Nrec.GetBinContent(j)
				fake = h_fake.GetBinContent(j)
				if fake == 0:
					continue
				num = num + fake * Nrec
				denom = denom + Nrec
			result1 = num/denom
			num = 0
			denom = 0
			for j in range(minindex, h_Nrec.GetNbinsX()+1):
				Nrec = h_Nrec.GetBinContent(j)
				fake = h_fake.GetBinContent(j)
				if fake == 0:
					continue
				num = num + fake * Nrec
				denom = denom + Nrec
			result2 = num/denom
			result = [result1, result2]
		elif v[1]=="pv_tag":
			h_PV_tag = runHists[HIST_P.index("TruePVLocationIndexCumulative")][1]
			no_rec = h_PV_tag.GetBinContent(1)
			rec_id = h_PV_tag.GetBinContent(2)
			rec_noid = h_PV_tag.GetBinContent(3)
			total_events = no_rec + rec_id + rec_noid
			no_rec_frac = no_rec / total_events
			rec_id_frac = rec_id / total_events
			rec_noid_frac = rec_noid / total_events
			result = [no_rec_frac, rec_id_frac, rec_noid_frac]
		elif v[1]=="res":
			h_res_PV_Z = runHists[HIST_P.index("RecoPVAssoc2GenPVMatched_ResolZ")][1]
			h_res_PV_X = runHists[HIST_P.index("RecoPVAssoc2GenPVMatched_ResolX")][1]
			h_res_PV_Y = runHists[HIST_P.index("RecoPVAssoc2GenPVMatched_ResolY")][1]
			h_res_All_Z = runHists[HIST_P.index("RecoAllAssoc2GenMatched_ResolZ")][1]
			h_res_All_X = runHists[HIST_P.index("RecoAllAssoc2GenMatched_ResolX")][1]
			h_res_All_Y = runHists[HIST_P.index("RecoAllAssoc2GenMatched_ResolY")][1]
			h_res_merged_Z = runHists[HIST_P.index("RecoAllAssoc2GenMatchedMerged_ResolZ")][1]
			h_res_merged_X = runHists[HIST_P.index("RecoAllAssoc2GenMatchedMerged_ResolX")][1]
			h_res_merged_Y = runHists[HIST_P.index("RecoAllAssoc2GenMatchedMerged_ResolY")][1]
			h_res_PV_Z.Fit("gaus", "Q0")
			h_res_PV_X.Fit("gaus", "Q0")
			h_res_PV_Y.Fit("gaus", "Q0")
			h_res_All_Z.Fit("gaus", "Q0")
			h_res_All_X.Fit("gaus", "Q0")
			h_res_All_Y.Fit("gaus", "Q0")
			h_res_merged_Z.Fit("gaus", "Q0")
			h_res_merged_X.Fit("gaus", "Q0")
			h_res_merged_Y.Fit("gaus", "Q0")
			f_res_PV_Z = h_res_PV_Z.GetFunction("gaus")
			f_res_PV_X = h_res_PV_X.GetFunction("gaus")
			f_res_PV_Y = h_res_PV_Y.GetFunction("gaus")
			f_res_All_Z = h_res_All_Z.GetFunction("gaus")
			f_res_All_X = h_res_All_X.GetFunction("gaus")
			f_res_All_Y = h_res_All_Y.GetFunction("gaus")
			f_res_merged_Z = h_res_merged_Z.GetFunction("gaus")
			f_res_merged_X = h_res_merged_X.GetFunction("gaus")
			f_res_merged_Y = h_res_merged_Y.GetFunction("gaus")
			mean_res_PV_Z = f_res_PV_Z.GetParameter(1)
			mean_res_PV_X = f_res_PV_X.GetParameter(1)
			mean_res_PV_Y = f_res_PV_Y.GetParameter(1)
			mean_res_All_Z = f_res_All_Z.GetParameter(1)
			mean_res_All_X = f_res_All_X.GetParameter(1)
			mean_res_All_Y = f_res_All_Y.GetParameter(1)
			mean_res_merged_Z = f_res_merged_Z.GetParameter(1)
			mean_res_merged_X = f_res_merged_X.GetParameter(1)
			mean_res_merged_Y = f_res_merged_Y.GetParameter(1)
			sigma_res_PV_Z = f_res_PV_Z.GetParameter(2)
			sigma_res_PV_X = f_res_PV_X.GetParameter(2)
			sigma_res_PV_Y = f_res_PV_Y.GetParameter(2)
			sigma_res_All_Z = f_res_All_Z.GetParameter(2)
			sigma_res_All_X = f_res_All_X.GetParameter(2)
			sigma_res_All_Y = f_res_All_Y.GetParameter(2)
			sigma_res_merged_Z = f_res_merged_Z.GetParameter(2)
			sigma_res_merged_X = f_res_merged_X.GetParameter(2)
			sigma_res_merged_Y = f_res_merged_Y.GetParameter(2)
			resultPV = [[sigma_res_PV_Z, mean_res_PV_Z], [sigma_res_PV_X, mean_res_PV_X], [sigma_res_PV_Y, mean_res_PV_Y]]
			resultAll = [[sigma_res_All_Z, mean_res_All_Z], [sigma_res_All_X, mean_res_All_X], [sigma_res_All_Y, mean_res_All_Y]]
			resultMerged = [[sigma_res_merged_Z, mean_res_merged_Z], [sigma_res_merged_X, mean_res_merged_X], [sigma_res_merged_Y, mean_res_merged_Y]]
			result = [resultPV, resultAll, resultMerged]
		runResults.append(result)
	RUN_HISTP_RESULTS.append([r,runResults])

print("")
print("RUN_HISTP_RESULTS")
print("")
print(RUN_HISTP_RESULTS[0])

with open(f"{args.outputfile}.json", "w") as f:
	json.dump(RUN_HISTP_RESULTS,f)
