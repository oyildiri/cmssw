import ROOT
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import os
from pathlib import Path
import shutil
ROOT.gROOT.SetBatch(False)

print(ROOT.kBlack, type(ROOT.kBlack))

parser = argparse.ArgumentParser()
parser.add_argument(
	"--run_path_list",
	type=str,
)

parser.add_argument(
	"--only_vs_param",
	action="store_true"
)

parser.add_argument(
	"--only_hist",
	action="store_true"
)
args = parser.parse_args()

param_manual = False
runs_from_list = True

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

HIST_H = [
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
		run.append("%s/%s/RUNS_%s/run_%s"%(run[0],run[1],run[2],run[5]))
		run_list.append(run)

def sum_in_bins(H,runs):
	h_run_list = []
	for r in runs:
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%r[6])
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

def getbinvalue(H,run,bin):
	f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%run[6])
	h_run = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/%s"%H)
	h_run.SetDirectory(0)
	binvalue = h_run.GetBinCenter(bin)
	return binvalue

RUN_HISTP_RESULTS = []
for r in run_list:
	f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%str(r[6]))
	runHists = []
	for HP in enumerate(HIST_P):
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

#for r in RUN_HISTP_RESULTS:
#	print("result:", r)

YPLOT = []
for i in enumerate(P_PLOTS_BLOCK):
	if i[1]=="e_glob":
		e_glob = [] 
		for RH in RUN_HISTP_RESULTS:
			e_glob.append([RH[0],RH[1][i[0]]])
		YPLOT.append(["e_glob",e_glob])
		print("")
		print("EFFICIENCY:")
		print(e_glob)
		print("")
		print("------------------------------------------------")
	elif i[1]=="f_glob":
		f_glob = []
		for RH in RUN_HISTP_RESULTS:
			f_glob.append([RH[0],RH[1][i[0]]])
		YPLOT.append(["f_glob",f_glob])
		print("")
		print("FAKE RATE:")
		print(f_glob)
		print("")
		print("------------------------------------------------")
	elif i[1]=="f_glob_lowntrk_highntrk":
		sums = sum_in_bins("fakerate_vs_NumTracks", run_list)
		minindex = min_index(sums,0,100) + 1
		binvalue = getbinvalue("fakerate_vs_NumTracks", RH[0], minindex)
		f_glob_lowntrk = []
		for RH in RUN_HISTP_RESULTS:
			f_glob_lowntrk.append([RH[0],RH[1][i[0]][0]])
		YPLOT.append(["f_glob_lowntrk",f_glob_lowntrk])
		print("")
		print(f"FAKE RATE FOR LOW NUMTRK: (numtrk <= ~{binvalue})")
		print(f_glob_lowntrk)
		print("")
		print("------------------------------------------------")
		print("")
		f_glob_highntrk = []
		for RH in RUN_HISTP_RESULTS:
			f_glob_highntrk.append([RH[0],RH[1][i[0]][1]])
		YPLOT.append(["f_glob_highntrk",f_glob_highntrk])
		print("")
		print(f"FAKE RATE FOR LOW NUMTRK: (numtrk >= ~{binvalue})")
		print(f_glob_highntrk)
		print("")
		print("------------------------------------------------")
		print("")
	elif i[1]=="pv_tag":
		print("")
		print("PV TAGGING")
		NoRecFrac = []
		for RH in RUN_HISTP_RESULTS:
			NoRecFrac.append([RH[0],RH[1][i[0]][0]])
		YPLOT.append(["NoRecFrac",NoRecFrac])
		print("")
		print("Not reconstructed:")
		print(NoRecFrac)
		RecAndIdFrac = []
		for RH in RUN_HISTP_RESULTS:
			RecAndIdFrac.append([RH[0],RH[1][i[0]][1]])
		YPLOT.append(["RecAndIdFrac",RecAndIdFrac])
		print("")
		print("Reconstructed and identified:")
		print(RecAndIdFrac)
		RecNoIdFrac = []
		for RH in RUN_HISTP_RESULTS:
			RecNoIdFrac.append([RH[0],RH[1][i[0]][2]])
		YPLOT.append(["RecNoIdFrac",RecNoIdFrac])
		print("")
		print("Reconstructed, not identified:")
		print(RecNoIdFrac)
		print("")
		print("------------------------------------------------")
		print("")
	elif i[1]=="res":
		print("")
		print("RESOLUTION")
		print("")
		print("PV resolution:")
		PV_Z_Res = []
		PV_Z_Mean = []
		PV_X_Res = []
		PV_X_Mean = []
		PV_Y_Res = []
		PV_Y_Mean = []
		for RH in RUN_HISTP_RESULTS:
			PV_Z_Res.append([RH[0],RH[1][i[0]][0][0][0]])
			PV_Z_Mean.append([RH[0],RH[1][i[0]][0][0][1]])
			PV_X_Res.append([RH[0],RH[1][i[0]][0][1][0]])
			PV_X_Mean.append([RH[0],RH[1][i[0]][0][1][1]])
			PV_Y_Res.append([RH[0],RH[1][i[0]][0][2][0]])
			PV_Y_Mean.append([RH[0],RH[1][i[0]][0][2][1]])
		YPLOT.append(["PV_Z_Res",PV_Z_Res])
		YPLOT.append(["PV_Z_Mean",PV_Z_Mean])
		YPLOT.append(["PV_X_Res",PV_X_Res])
		YPLOT.append(["PV_X_Mean",PV_X_Mean])
		YPLOT.append(["PV_Y_Res",PV_Y_Res])
		YPLOT.append(["PV_Y_Mean",PV_Y_Mean])
		print("")
		print("Sigma in Z")
		print(PV_Z_Res)
		print("")
		print("Mean in Z")
		print(PV_Z_Mean)
		print("")
		print("Sigma in X")
		print(PV_X_Res)
		print("")
		print("Mean in X")
		print(PV_X_Mean)
		print("")
		print("Sigma in Y")
		print(PV_Y_Res)
		print("")
		print("Mean in Y")
		print(PV_Y_Mean)
		print("")
		print("------------------------------------------------")
		print("")
		print("All resolution:")
		All_Z_Res = []
		All_Z_Mean = []
		All_X_Res = []
		All_X_Mean = []
		All_Y_Res = []
		All_Y_Mean = []
		for RH in RUN_HISTP_RESULTS:
			All_Z_Res.append([RH[0],RH[1][i[0]][1][0][0]])
			All_Z_Mean.append([RH[0],RH[1][i[0]][1][0][1]])
			All_X_Res.append([RH[0],RH[1][i[0]][1][1][0]])
			All_X_Mean.append([RH[0],RH[1][i[0]][1][1][1]])
			All_Y_Res.append([RH[0],RH[1][i[0]][1][2][0]])
			All_Y_Mean.append([RH[0],RH[1][i[0]][1][2][1]])
		YPLOT.append(["All_Z_Res",All_Z_Res])
		YPLOT.append(["All_Z_Mean",All_Z_Mean])
		YPLOT.append(["All_X_Res",All_X_Res])
		YPLOT.append(["All_X_Mean",All_X_Mean])
		YPLOT.append(["All_Y_Res",All_Y_Res])
		YPLOT.append(["All_Y_Mean",All_Y_Mean])
		print("")
		print("Sigma in Z")
		print(All_Z_Res)
		print("")
		print("Mean in Z")
		print(All_Z_Mean)
		print("")
		print("Sigma in X")
		print(All_X_Res)
		print("")
		print("Mean in X")
		print(All_X_Mean)
		print("")
		print("Sigma in Y")
		print(All_Y_Res)
		print("")
		print("Mean in Y")
		print(All_Y_Mean)
		print("")
		print("------------------------------------------------")
		print("")
		print("Merged resolution:")
		Merged_Z_Res = []
		Merged_Z_Mean = []
		Merged_X_Res = []
		Merged_X_Mean = []
		Merged_Y_Res = []
		Merged_Y_Mean = []
		for RH in RUN_HISTP_RESULTS:
			Merged_Z_Res.append([RH[0],RH[1][i[0]][2][0][0]])
			Merged_Z_Mean.append([RH[0],RH[1][i[0]][2][0][1]])
			Merged_X_Res.append([RH[0],RH[1][i[0]][2][1][0]])
			Merged_X_Mean.append([RH[0],RH[1][i[0]][2][1][1]])
			Merged_Y_Res.append([RH[0],RH[1][i[0]][2][2][0]])
			Merged_Y_Mean.append([RH[0],RH[1][i[0]][2][2][1]])
		YPLOT.append(["Merged_Z_Res",Merged_Z_Res])
		YPLOT.append(["Merged_Z_Mean",Merged_Z_Mean])
		YPLOT.append(["Merged_X_Res",Merged_X_Res])
		YPLOT.append(["Merged_X_Mean",Merged_X_Mean])
		YPLOT.append(["Merged_Y_Res",Merged_Y_Res])
		YPLOT.append(["Merged_Y_Mean",Merged_Y_Mean])
		print("")
		print("Sigma in Z")
		print(Merged_Z_Res)
		print("")
		print("Mean in Z")
		print(Merged_Z_Mean)
		print("")
		print("Sigma in X")
		print(Merged_X_Res)
		print("")
		print("Mean in X")
		print(Merged_X_Mean)
		print("")
		print("Sigma in Y")
		print(Merged_Y_Res)
		print("")
		print("Mean in Y")
		print(Merged_Y_Mean)

print("")
print("YPLOT:")
print("")
print(YPLOT[0])

YPLOT_SORTED = []
for Y in YPLOT:
	hist = Y[0]
	TAGS = []
	SORTED_R = []
	for R in Y[1]:
		print("")
		print(Y[0])
		print(R[0])
		tag = [R[0][3],R[0][0],R[0][1],R[0][2]]
		if tag not in TAGS:
			TAGS.append(tag)
			SORTED_R.append([tag, [R]])
		elif tag in TAGS:
			loc = TAGS.index(tag)
			SORTED_R[loc][1].append(R)
	YPLOT_SORTED.append([hist,SORTED_R])

print("")
print("YPLOT_SORTED")
print("")
for Y in YPLOT_SORTED:
	print(Y[0])
	print(Y[1])


pltcolors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for i, YS in enumerate(YPLOT_SORTED):
	ptcolor = pltcolors[i % len(pltcolors)]
	for P in YS[1]:
		if P[0][0] == "P":
			xvalues = []
			yvalues = []
			for P1 in P[1]:
				xvalues.append(P1[0][4])
				yvalues.append(P1[1])
			plt.plot(xvalues,yvalues,color=ptcolor,label = f"{P[0][0]}/{P[0][1]}/{P[0][2]}/{P[0][3]}")
		elif P[0][0] == "I":
			for P1 in P[1]:
				yvalue = P1[1]
				plt.axhline(y=yvalue,color=ptcolor, label = f"{P[0][0]}/{P[0][1]}/{P[0][2]}/{P[0][3]}")


	# Titles, axis labels, plotting
	if YS[0] == "e_glob":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Efficiency $\overline{\epsilon}$")
		plt.title("Efficiency vs mintrkweight")
		plotname = "eff_mintrkweight.png"
	elif YS[0] == "f_glob":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Fake rate $\overline{f}$")
		plt.title("Fake rate vs mintrkweight")
		plotname = "fakerate_mintrkweight.png"
	elif YS[0] == "f_glob_lowntrk":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Fake rate $\overline{f}$")
		plt.title(f"Fake rate for low NumTrack (NumTrak < ~{binvalue}) vs mintrkweight")
		plotname = "fakerate_lowntrk_mintrkweight.png"
	elif YS[0] == "f_glob_highntrk":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Fake rate $\overline{f}$")
		plt.title(f"Fake rate for high NumTrack (NumTrak > ~{binvalue}) vs mintrkweight")
		plotname = "fakerate_highntrk_mintrkweight.png"
	elif YS[0] == "NoRecFrac":
		plt.xlabel("mintrkweight")
		plt.ylabel("Fraction of events with PV not reconstructed")
		plt.title("Fraction of events with PV not reconstructed vs mintrkweight")
		plotname = "NoRecFrac_mintrkweight.png"
	elif YS[0] == "RecAndIdFrac":
		plt.xlabel("mintrkweight")
		plt.ylabel("Fraction of events with PV reconstructed and identified")
		plt.title("Fraction of events with PV reconstructed and identified vs mintrkweight")
		plotname = "RecAndIdFrac_mintrkweight.png"
	elif YS[0] == "RecNoIdFrac":
		plt.xlabel("mintrkweight")
		plt.ylabel("Fraction of events with PV reconstructed but not identified")
		plt.title("Fraction of events with PV reconstructed but not identified vs mintrkweight")
		plotname = "RecNoIdFrac_mintrkweight.png"
	elif YS[0] == "PV_Z_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution z (${\mu} m$)")
		plt.title("PV resolution z vs mintrkweight")
		plotname = "PV_Z_Res_mintrkweight.png"
	elif YS[0] == "PV_X_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution x (${\mu} m$)")
		plt.title("PV resolution x vs mintrkweight")
		plotname = "PV_X_Res_mintrkweight.png"
	elif YS[0] == "PV_Y_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution y (${\mu} m$)")
		plt.title("PV resolution y vs mintrkweight")
		plotname = "PV_Y_Res_mintrkweight.png"
	elif YS[0] == "PV_Z_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution z mean (${\mu} m$)")
		plt.title("PV resolution z mean vs mintrkweight")
		plotname = "PV_Z_Res_mean_mintrkweight.png"
	elif YS[0] == "PV_X_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution x mean (${\mu} m$)")
		plt.title("PV resolution x mean vs mintrkweight")
		plotname = "PV_X_Res_mean_mintrkweight.png"
	elif YS[0] == "PV_Y_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"PV resolution y mean (${\mu} m$)")
		plt.title("PV resolution y mean vs mintrkweight")
		plotname = "PV_Y_Res_mean_mintrkweight.png"
	elif YS[0] == "All_Z_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution z (${\mu} m$)")
		plt.title("All resolution z vs mintrkweight")
		plotname = "All_Z_Res_mintrkweight.png"
	elif YS[0] == "All_X_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution x (${\mu} m$)")
		plt.title("All resolution x vs mintrkweight")
		plotname = "All_X_Res_mintrkweight.png"
	elif YS[0] == "All_Y_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution y (${\mu} m$)")
		plt.title("All resolution y vs mintrkweight")
		plotname = "All_Y_Res_mintrkweight.png"
	elif YS[0] == "All_Z_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution z mean (${\mu} m$)")
		plt.title("All resolution z mean vs mintrkweight")
		plotname = "All_Z_Res_mean_mintrkweight.png"
	elif YS[0] == "All_X_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution x mean (${\mu} m$)")
		plt.title("All resolution x mean vs mintrkweight")
		plotname = "All_X_Res_mean_mintrkweight.png"
	elif YS[0] == "All_Y_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"All resolution y mean (${\mu} m$)")
		plt.title("All resolution y mean vs mintrkweight")
		plotname = "All_Y_Res_mean_mintrkweight.png"
	elif YS[0] == "Merged_Z_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution z (${\mu} m$)")
		plt.title("Merged resolution z vs mintrkweight")
		plotname = "Merged_Z_Res_mintrkweight.png"
	elif YS[0] == "Merged_X_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution x (${\mu} m$)")
		plt.title("Merged resolution x vs mintrkweight")
		plotname = "Merged_X_Res_mintrkweight.png"
	elif YS[0] == "Merged_Y_Res":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution y (${\mu} m$)")
		plt.title("Merged resolution y vs mintrkweight")
		plotname = "Merged_Y_Res_mintrkweight.png"
	elif YS[0] == "Merged_Z_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution z mean (${\mu} m$)")
		plt.title("Merged resolution z mean vs mintrkweight")
		plotname = "Merged_Z_Res_mean_mintrkweight.png"
	elif YS[0] == "Merged_X_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution x mean (${\mu} m$)")
		plt.title("Merged resolution x mean vs mintrkweight")
		plotname = "Merged_X_Res_mean_mintrkweight.png"
	elif YS[0] == "Merged_Y_Mean":
		plt.xlabel("mintrkweight")
		plt.ylabel(r"Merged resolution y mean (${\mu} m$)")
		plt.title("Merged resolution y mean vs mintrkweight")
		plotname = "Merged_Y_Res_mean_mintrkweight.png"
	plt.grid()
	plt.legend()
	plt.savefig("OptPlots/%s"%plotname)
	plt.close()

if not args.only_vs_params == True:
	RUN_HIST_H = []
	for r in run_list:
		print(r)
	for H in HIST_H:
		h_results = []
		for r in run_list:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%str(r[6]))
			h = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/%s"%H)
			h.SetDirectory(0)
			if r[3] == "P":
				label = f"{r[0]}/{r[1]}/{r[2]}/{r[4]:.3f}"
			elif r[3] == "I":
				label = f"{r[0]}/{r[1]}/{r[2]}"
			result = [r,h,label]
			h_results.append(result)
		RUN_HIST_H.append([H, h_results])


	colors = [
		ROOT.kBlack,
		ROOT.kRed,
		ROOT.kBlue,
		ROOT.kGreen+2,
		ROOT.kMagenta,
		ROOT.kOrange+7,
		ROOT.kCyan+2,
		ROOT.kViolet,
		ROOT.kAzure+1,
		ROOT.kPink+7,
		ROOT.kTeal+3,
		ROOT.kSpring+5,
		ROOT.kYellow+2,
		ROOT.kOrange+1,
		ROOT.kRed+2,
		ROOT.kBlue+2,
		ROOT.kGreen+3,
		ROOT.kMagenta+2,
		ROOT.kCyan+3,
		ROOT.kGray+2
	]

	def RootTH1FPlot(hist_name, hist_list,x1,y1,x2,y2,xtitle,ytitle):
		c1 = ROOT.TCanvas(f"c_{hist_name}",f"c_{hist_name}",800,800)
		pad1 = ROOT.TPad("pad1", "top pad", 0, 0.30, 1, 1.0)
		pad2 = ROOT.TPad("pad2", "bottom pad", 0, 0.00, 1, 0.30)
		pad1.SetBottomMargin(0.02)
		pad2.SetTopMargin(0.02)
		pad2.SetBottomMargin(0.30)
		pad1.Draw()
		pad2.Draw()
		pad1.SetGrid()
		pad2.SetGrid()

		pad1.cd()

		for i, h in enumerate(hist_list[1]):
			color = int(colors[i % len(colors)])
			h[1].SetLineColor(color)
			h[1].SetLineWidth(2)
			h[1].SetStats(0)
		ymax = max(h[1].GetMaximum() for h in hist_list[1])
		hist_list[1][0][1].SetMaximum(1.2*ymax)
		hist_list[1][0][1].Draw("HIST")
		for h in hist_list[1]:
			if h[1] == hist_list[1][0][1]:
				continue
			h[1].Draw("HIST SAME")
		hist_list[1][0][1].GetXaxis().SetLabelSize(0)
		hist_list[1][0][1].GetXaxis().SetTitleSize(0)
		hist_list[1][0][1].GetYaxis().SetTitle(ytitle)
		leg = ROOT.TLegend(x1, y1, x2, y2)
		leg.SetTextSize(0.04)
		leg.SetMargin(0.2)
		leg.SetEntrySeparation(0.9)
		for i, h in enumerate(hist_list[1]):
			leg.AddEntry(h[1], h[2], "l")
		leg.Draw()

		### ratio

		pad2.cd()

		Ratios = []
		for i, h in enumerate(hist_list[1]):
			if h[1] == hist_list[1][0][1]:
				continue
			r = h[1].Clone(f"r{i+1}")
			Ratios.append(r)
		for i, r in enumerate(Ratios):
			color = int(colors[(i+1) % len(colors)])
			r.Divide(hist_list[1][0][1])
			r.SetLineColor(color)
			r.SetLineWidth(2)
			r.SetStats(0)
		Ratios[0].SetTitle("")
		Ratios[0].GetYaxis().SetTitle("Ratio")
		Ratios[0].GetYaxis().SetNdivisions(505)
		Ratios[0].GetYaxis().SetTitleSize(0.08)
		Ratios[0].GetYaxis().SetTitleOffset(0.5)
		Ratios[0].GetYaxis().SetLabelSize(0.08)

		Ratios[0].GetXaxis().SetTitle(xtitle)
		Ratios[0].GetXaxis().SetTitleSize(0.10)
		Ratios[0].GetXaxis().SetTitleOffset(1.1)
		Ratios[0].GetXaxis().SetLabelSize(0.08)
		Ratios[0].SetMinimum(0.5)
		Ratios[0].SetMaximum(1.5)
		Ratios[0].Draw("HIST")
		for r in Ratios:
			if r == Ratios[0]:
				continue
			r.Draw("HIST SAME")
		line = ROOT.TLine(
			hist_list[1][0][1].GetXaxis().GetXmin(), 1.0,
			hist_list[1][0][1].GetXaxis().GetXmax(), 1.0
		)
		line.SetLineStyle(2)
		line.Draw()
		c1.SaveAs(f"OptPlots/{hist_name}.png")

	for RH in RUN_HIST_H:
		if RH[0] == "RecoAllAssoc2Gen_NumTracks":
			RootTH1FPlot(RH[0], RH, 0.5, 0.5, 0.92, 0.92, "Number of tracks in vertex fit", "N")
		elif RH[0] == "RecoAllAssoc2Gen_X":
			RootTH1FPlot(RH[0], RH, 0.6, 0.4, 0.92, 0.92, "Reco vertex pos x (cm)", "N")
		elif RH[0] == "RecoAllAssoc2Gen_Y":
			RootTH1FPlot(RH[0], RH, 0.6, 0.4, 0.92, 0.92, "Reco vertex pos y (cm)", "N")
		elif RH[0] == "effic_vs_NumTracks":
			RootTH1FPlot(RH[0], RH, 0.46, 0.29, 0.83, 0.69,"Number of tracks in vertex fit","Efficiency")
		elif RH[0] == "fakerate_vs_NumTracks":
			RootTH1FPlot(RH[0], RH, 0.5, 0.5, 0.92, 0.92, "Number of tracks in vertex fit", "Fake rate")
		elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolZ":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (#mu m)", "N")
		elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolX":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (#mu m)", "N")
		elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolY":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatched_ResolZ":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatched_ResolX":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatched_ResolY":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolZ":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolX":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (#mu m)", "N")
		elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolY":
			RootTH1FPlot(RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (#mu m)", "N")
