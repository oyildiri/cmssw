import ROOT
import matplotlib.pyplot as plt
import numpy as np
ROOT.gROOT.SetBatch(False)

print(ROOT.kBlack, type(ROOT.kBlack))


param_min = 0.01
param_max = 0.5
param_num = 10
dp = (param_max - param_min)/(param_num - 1)
params_given = [0.5555555555555556, 0.6111111111111112, 0.6666666666666666, 0.7222222222222222, 0.7777777777777778, 0.8333333333333333, 0.8888888888888888, 0.9444444444444444, 1.0]

param_manual = False
runs_from_list = True

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
    "f_glob_lowntrk",
    "f_glob_highntrk",
    "pv_tag",
    "res"
]


#Parameters

if runs_from_list == True:
	run_paths=[]
	with open("run_p_list.txt", 'r') as file:
		for line in file:
			run_paths.append(line.strip())
	inter_0 = []
	for r in run_paths:
		main_pos = r.split("/").index("OldNewCF")
		print(main_pos)
		inter_0.append(r.split("/")[main_pos+1])
	inter = sorted(set(inter_0))

	params_0 = []
	for r in run_paths:
		main_pos = r.split("/").index("OldNewCF")
		params_0.append(float(r.split("/")[main_pos+4].removeprefix("run_p_")))
	params = sorted(set(params_0))
else:
	inter = ["TT"]
	params=[]
	if param_manual == True:
		params = params_given
	else:
		for i in range(param_num):
			params.append(param_min + i*dp)

print("MINTRKWEIGHT VALUES")
print("")
print(params)
print("")
print("----------------------------------------------")

# vs param plots
#P_PLOTS_Y = []
#for k in P_PLOTS_BLOCK:
#	Y = []
#		for l in run_list:
#			if l[1] == "P":
#				try:
#					f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
#				except:
#					Y.append(np.nan)
#			elif l[1] == "I":


#Efficiency
e_globs = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		except:
			e_globs.append(np.nan)
			continue
		h_N = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/GenAllAssoc2RecoMatched_NumTracks")
		h_N.SetDirectory(0)
		h_eff = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/effic_vs_NumTracks")
		h_eff.SetDirectory(0)
		num = 0
		denom = 0
		print(p)
		for j in range(0, h_N.GetNbinsX()+2):
			N =  h_N.GetBinContent(j)
			eff = h_eff.GetBinContent(j)
			if eff == 0:
				continue
			num = num + N
			denom = denom + N/eff
		e_globs.append(num/denom)
print("")
print("EFFICIENCY")
print("")
print("Global efficiency ", e_globs)
print("")
print("----------------------------------------------")
#Fake rate
f_globs = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		except:
			f_globs.append(np.nan)
			continue
		h_Nrec = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_NumTracks")
		h_Nrec.SetDirectory(0)
		h_fake = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/fakerate_vs_NumTracks")
		h_fake.SetDirectory(0)

		num = 0
		denom = 0
		for j in range(0, h_Nrec.GetNbinsX()+2):
			Nrec = h_Nrec.GetBinContent(j)
			fake = h_fake.GetBinContent(j)
			if fake == 0:
				continue
			num = num + fake * Nrec
			denom = denom + Nrec
		f_globs.append(num/denom)
print("")
print("FAKE RATE")
print("")
print("Global fake rate ", f_globs)
print("")
print("----------------------------------------------")

#Fake rate for low and high NumTracks
Fake = []
FakeRate_Hists = []
N_Hists = []
for i in inter:
	for p in params:
		try:
			f=ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		except:
			continue
		h_fake1 = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/fakerate_vs_NumTracks")
		h_fake1.SetDirectory(0)
		FakeRate_Hists.append(h_fake1)
		h_Nrec1 = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_NumTracks")
		h_Nrec1.SetDirectory(0)
		N_Hists.append(h_Nrec1)

for i in range(0, N_Hists[0].GetNbinsX()+2):
	fakerate1 = 0
	for j in range(len(FakeRate_Hists)):
		fakerate1 = fakerate1 + FakeRate_Hists[j].GetBinContent(i)
	Fake.append(fakerate1)
print(Fake)
min_Fake = min(x for x in Fake if x > 0)
min_fakerate_index = Fake.index(min_Fake) + 2
print(min_fakerate_index)
#low NumTracks
f_globs1 = []
num = 0
denom = 0
for h in range(len(FakeRate_Hists)):
	for i in range(0, min_fakerate_index):
		Nrec = N_Hists[h].GetBinContent(i)
		fake = FakeRate_Hists[h].GetBinContent(i)
		if fake == 0:
			continue
		num = num + fake * Nrec
		denom = denom + Nrec
	if denom == 0:
		f_globs1.append(0)
		continue
	f_globs1.append(num/denom)
print("")
print("FAKE RATE (LOW NUMBER OF TRACKS)")
print("Global fake rate (Low NumTrack) ", f_globs1)
print("")
print("----------------------------------------------")

#Fake rate for high NumTracks
f_globs2 = []
num = 0
denom = 0
for h in range(len(FakeRate_Hists)):
        for i in range(min_fakerate_index, N_Hists[0].GetNbinsX()+2):
                Nrec = N_Hists[h].GetBinContent(i)
                fake = FakeRate_Hists[h].GetBinContent(i)
                if fake == 0:
                        continue
                num = num + fake * Nrec
                denom = denom + Nrec
        f_globs2.append(num/denom)
print("")
print("FAKE RATE (HIGH NUMBER OF TRACKS)")
print("Global fake rate (High NumTrack) ", f_globs2)
print("")
print("----------------------------------------------")

#PV tagging
NoRecFrac =[]
RecAndIdFrac = []
RecNoIdFrac = []

for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		except:
			NoRecFrac.append(np.nan)
			RecAndIdFrac.append(np.nan)
			RecNoIdFrac.append(np.nan)
			continue
		h_PV_tag = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/TruePVLocationIndexCumulative")
		h_PV_tag.SetDirectory(0)

		no_rec = h_PV_tag.GetBinContent(1)
		rec_id = h_PV_tag.GetBinContent(2)
		rec_noid = h_PV_tag.GetBinContent(3)

		total_events = no_rec + rec_id + rec_noid

		no_rec_frac = no_rec / total_events
		rec_id_frac = rec_id / total_events
		rec_noid_frac = rec_noid / total_events

		NoRecFrac.append(no_rec_frac)
		RecAndIdFrac.append(rec_id_frac)
		RecNoIdFrac.append(rec_noid_frac)

print("")
print("PV TAGGING")
print("")
print("Not reconstructed: ",NoRecFrac)
print("Reconstructed and identified: ", RecAndIdFrac)
print("Reconstructed, not identified: ", RecNoIdFrac)
print("")
print("----------------------------------------------")

#Resolution
PV_Z_Res =[]
All_Z_Res =[]
Merged_Z_Res =[]

PV_X_Res = []
All_X_Res = []
Merged_X_Res = []

PV_Y_Res = []
All_Y_Res = []
Merged_Y_Res = []

PV_Z_Mean = []
All_Z_Mean = []
Merged_Z_Mean = []

PV_X_Mean = []
All_X_Mean = []
Merged_X_Mean = []

PV_Y_Mean = []
All_Y_Mean = []
Merged_Y_Mean = []

for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		except:
			PV_Z_Res.append(np.nan)
			All_Z_Res.append(np.nan)
			Merged_Z_Res.append(np.nan)

			PV_X_Res.append(np.nan)
			All_X_Res.append(np.nan)
			Merged_X_Res.append(np.nan)

			PV_Y_Res.append(np.nan)
			All_Y_Res.append(np.nan)
			Merged_Y_Res.append(np.nan)

			PV_Z_Mean.append(np.nan)
			All_Z_Mean.append(np.nan)
			Merged_Z_Mean.append(np.nan)

			PV_X_Mean.append(np.nan)
			All_X_Mean.append(np.nan)
			Merged_X_Mean.append(np.nan)

			PV_Y_Mean.append(np.nan)
			All_Y_Mean.append(np.nan)
			Merged_Y_Mean.append(np.nan)
			continue
		h_res_PV_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolZ")
		h_res_PV_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolX")
		h_res_PV_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolY")
		h_res_PV_Z.SetDirectory(0)
		h_res_PV_X.SetDirectory(0)
		h_res_PV_Y.SetDirectory(0)

		h_res_All_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolZ")
		h_res_All_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolX")
		h_res_All_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolY")
		h_res_All_Z.SetDirectory(0)
		h_res_All_X.SetDirectory(0)
		h_res_All_Y.SetDirectory(0)

		h_res_merged_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolZ")
		h_res_merged_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolX")
		h_res_merged_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolY")
		h_res_merged_Z.SetDirectory(0)
		h_res_merged_X.SetDirectory(0)
		h_res_merged_Y.SetDirectory(0)

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

		PV_Z_Res.append(sigma_res_PV_Z)
		PV_X_Res.append(sigma_res_PV_X)
		PV_Y_Res.append(sigma_res_PV_Y)

		All_Z_Res.append(sigma_res_All_Z)
		All_X_Res.append(sigma_res_All_X)
		All_Y_Res.append(sigma_res_All_Y)

		Merged_Z_Res.append(sigma_res_merged_Z)
		Merged_X_Res.append(sigma_res_merged_X)
		Merged_Y_Res.append(sigma_res_merged_Y)

		PV_Z_Mean.append(mean_res_PV_Z)
		PV_X_Mean.append(mean_res_PV_X)
		PV_Y_Mean.append(mean_res_PV_Y)

		All_Z_Mean.append(mean_res_All_Z)
		All_X_Mean.append(mean_res_All_X)
		All_Y_Mean.append(mean_res_All_Y)

		Merged_Z_Mean.append(mean_res_merged_Z)
		Merged_X_Mean.append(mean_res_merged_X)
		Merged_Y_Mean.append(mean_res_merged_Y)

print("")
print("RESOLUTION")
print("")
print("PV_Z_Res: ", PV_Z_Res)
print("PV_X_Res: ", PV_X_Res)
print("PV_Y_Res: ", PV_Y_Res)
print("")
print("All_Z_Res: ", All_Z_Res)
print("All_X_Res: ", All_X_Res)
print("All_Y_Res: ", All_Y_Res)
print("")
print("Merged_Z_Res: ", Merged_Z_Res)
print("Merged_X_Res: ", Merged_X_Res)
print("Merged_Y_Res: ", Merged_Y_Res)
print("")
print("PV_Z_Mean: ", PV_Z_Mean)
print("PV_X_Mean: ", PV_X_Mean)
print("PV_Y_Mean: ", PV_Y_Mean)
print("")
print("All_Z_Mean: ", All_Z_Mean)
print("All_X_Mean: ", All_X_Mean)
print("All_Y_Mean: ", All_Y_Mean)
print("")
print("Merged_Z_Mean: ", Merged_Z_Mean)
print("Merged_X_Mean: ", Merged_X_Mean)
print("Merged_Y_Mean: ", Merged_Y_Mean)
print("")
print("----------------------------------------------")

##############################################################

# ROOT Histograms

# RecoAllAssoc2Gen_NumTracks

Hist_raa2gnt = []
Hist_raa2gnt_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hraa2gnt = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_NumTracks")
			hraa2gnt.SetDirectory(0)
			Hist_raa2gnt.append(hraa2gnt)
			Hist_raa2gnt_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2Gen_X

Hist_raa2gx = []
Hist_raa2gx_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hraa2gx = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_X")
			hraa2gx.SetDirectory(0)
			Hist_raa2gx.append(hraa2gx)
			Hist_raa2gx_labels.append(f"{i}_{p:.3f}")
		except:
			continue
# RecoAllAssoc2Gen_Y

Hist_raa2gy = []
Hist_raa2gy_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hraa2gy = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_Y")
			hraa2gy.SetDirectory(0)
			Hist_raa2gy.append(hraa2gy)
			Hist_raa2gy_labels.append(f"{i}_{p:.3f}")
		except:
			continue
# effic_vs_NumTracks

Hist_effnumtrk = []
Hist_effnumtrk_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			heffnumtrk = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/effic_vs_NumTracks")
			heffnumtrk.SetDirectory(0)
			Hist_effnumtrk.append(heffnumtrk)
			Hist_effnumtrk_labels.append(f"{i}_{p:.3f}")
		except:
			continue
# fakerate_vs_NumTracks

Hist_fakenumtrk = []
Hist_fakenumtrk_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hfakenumtrk = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/fakerate_vs_NumTracks")
			hfakenumtrk.SetDirectory(0)
			Hist_fakenumtrk.append(hfakenumtrk)
			Hist_fakenumtrk_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoPVAssoc2GenPVMatched_ResolZ

Hist_pvresz = []
Hist_pvresz_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hpvresz = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolZ")
			hpvresz.SetDirectory(0)
			Hist_pvresz.append(hpvresz)
			Hist_pvresz_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoPVAssoc2GenPVMatched_ResolX

Hist_pvresx = []
Hist_pvresx_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hpvresx = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolX")
			hpvresx.SetDirectory(0)
			Hist_pvresx.append(hpvresx)
			Hist_pvresx_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoPVAssoc2GenPVMatched_ResolY

Hist_pvresy = []
Hist_pvresy_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hpvresy = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolY")
			hpvresy.SetDirectory(0)
			Hist_pvresy.append(hpvresy)
			Hist_pvresy_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatched_ResolZ

Hist_allresz = []
Hist_allresz_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hallresz = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolZ")
			hallresz.SetDirectory(0)
			Hist_allresz.append(hallresz)
			Hist_allresz_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatched_ResolX

Hist_allresx = []
Hist_allresx_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hallresx = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolX")
			hallresx.SetDirectory(0)
			Hist_allresx.append(hallresx)
			Hist_allresx_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatched_ResolY

Hist_allresy = []
Hist_allresy_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hallresy = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolY")
			hallresy.SetDirectory(0)
			Hist_allresy.append(hallresy)
			Hist_allresy_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatchedMerged_ResolZ

Hist_mresz = []
Hist_mresz_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hmresz = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolZ")
			hmresz.SetDirectory(0)
			Hist_mresz.append(hmresz)
			Hist_mresz_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatchedMerged_ResolX

Hist_mresx = []
Hist_mresx_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hmresx = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolX")
			hmresx.SetDirectory(0)
			Hist_mresx.append(hmresx)
			Hist_mresx_labels.append(f"{i}_{p:.3f}")
		except:
			continue

# RecoAllAssoc2GenMatchedMerged_ResolY

Hist_mresy = []
Hist_mresy_labels = []
for i in inter:
	for p in params:
		try:
			f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
			hmresy = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolY")
			hmresy.SetDirectory(0)
			Hist_mresy.append(hmresy)
			Hist_mresy_labels.append(f"{i}_{p:.3f}")
		except:
			continue

###############################################################

# Plotting

p_N = len(params)
i_N = len(inter)

plt.plot(params[i*p_N:(i+1)*p_N], e_globs[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Efficiency $\overline{\epsilon}$")
plt.title("Efficiency vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/eff_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], f_globs[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Fake rate $\overline{f}$")
plt.title("Fake rate vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/fakerate_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], f_globs1[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Fake rate $\overline{f}$")
plt.title("Fake rate (Low NumTrack) vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/fakerate_lowntrk_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], f_globs2[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Fake rate $\overline{f}$")
plt.title("Fake rate (High NumTrack) vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/fakerate_highntrk_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], NoRecFrac[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV not reconstructed")
plt.title("Fraction of events with PV not reconstructed vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/NoRecFrac_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], RecAndIdFrac[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV reconstructed and identified")
plt.title("Fraction of events with PV reconstructed and identified vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/RecAndIdFrac_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], RecNoIdFrac[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV reconstructed but not identified")
plt.title("Fraction of events with PV reconstructed but not identified vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/RecNoIdFrac_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], PV_Z_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"PV resolution z (${\mu} m$)")
plt.title("PV resolution z vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/PV_Z_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], All_Z_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"All resolution z (${\mu} m$)")
plt.title("All resolution z vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/All_Z_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], Merged_Z_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Merged resolution z (${\mu} m$)")
plt.title("Merged resolution z vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/Merged_Z_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], PV_X_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"PV resolution x (${\mu} m$)")
plt.title("PV resolution x vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/PV_X_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], All_X_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"All resolution x (${\mu} m$)")
plt.title("All resolution x vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/All_X_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], Merged_X_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Merged resolution x (${\mu} m$)")
plt.title("Merged resolution x vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/Merged_X_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], PV_Y_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"PV resolution y (${\mu} m$)")
plt.title("PV resolution y vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/PV_Y_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], All_Y_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"All resolution y (${\mu} m$)")
plt.title("All resolution y vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/All_Y_Res_mintrkweight.png")
#plt.show()

plt.plot(params[i*p_N:(i+1)*p_N], Merged_Y_Res[i*p_N:(i+1)*p_N],label="%s"%inter[i])
plt.xlabel("mintrkweight")
plt.ylabel(r"Merged resolution y (${\mu} m$)")
plt.title("Merged resolution y vs mintrkweight")
plt.grid()
plt.legend()
plt.savefig("mintrkweightPlots/Merged_Y_Res_mintrkweight.png")
#plt.show()

# Histogram plots
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
## Hist_raa2gnt
c1 = ROOT.TCanvas("c_raa2gnt","c_raa2gnt",800,800)
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

for i, h in enumerate(Hist_raa2gnt):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_raa2gnt)
Hist_raa2gnt[0].SetMaximum(1.2*ymax)
Hist_raa2gnt[0].Draw("HIST")
for h in Hist_raa2gnt:
	if h == Hist_raa2gnt[0]:
		continue
	h.Draw("HIST SAME")
Hist_raa2gnt[0].GetXaxis().SetLabelSize(0)
Hist_raa2gnt[0].GetXaxis().SetTitleSize(0)
Hist_raa2gnt[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.5, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
leg.SetEntrySeparation(0.9)
for i, h in enumerate(Hist_raa2gnt):
	leg.AddEntry(h, Hist_raa2gnt_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_raa2gnt):
	print(i, h, type(h))
	if h == Hist_raa2gnt[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_raa2gnt[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Number of tracks in vertex fit")
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
	Hist_raa2gnt[0].GetXaxis().GetXmin(), 1.0,
	Hist_raa2gnt[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_raa2gnt.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## hraa2gx
c1 = ROOT.TCanvas("c_raa2gx","craa2gx",800,800)
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

for i, h in enumerate(Hist_raa2gx):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_raa2gx)
Hist_raa2gx[0].SetMaximum(1.2*ymax)
Hist_raa2gx[0].Draw("HIST")
for h in Hist_raa2gx:
	if h == Hist_raa2gx[0]:
		continue
	h.Draw("HIST SAME")
Hist_raa2gx[0].GetXaxis().SetLabelSize(0)
Hist_raa2gx[0].GetXaxis().SetTitleSize(0)
Hist_raa2gx[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.6, 0.4, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_raa2gx):
	leg.AddEntry(h, Hist_raa2gx_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_raa2gx):
	print(i, h, type(h))
	if h == Hist_raa2gx[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_raa2gx[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Reco vertex pos x (cm)")
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
	Hist_raa2gx[0].GetXaxis().GetXmin(), 1.0,
	Hist_raa2gx[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_raa2gx.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_raa2gy
c1 = ROOT.TCanvas("c_raa2gy","c_raa2gy",800,800)
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
for i, h in enumerate(Hist_raa2gy):
        color = int(colors[i % len(colors)])
        h.SetLineColor(color)
        h.SetLineWidth(2)
        h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_raa2gy)
Hist_raa2gy[0].SetMaximum(1.2*ymax)
Hist_raa2gy[0].Draw("HIST")
for h in Hist_raa2gy:
        if h == Hist_raa2gy[0]:
                continue
        h.Draw("HIST SAME")
Hist_raa2gy[0].GetXaxis().SetLabelSize(0)
Hist_raa2gy[0].GetXaxis().SetTitleSize(0)
Hist_raa2gy[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.6, 0.4, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_raa2gy):
        leg.AddEntry(h, Hist_raa2gy_labels[i], "l")
leg.Draw()
### ratio
pad2.cd()

Ratios = []
for i, h in enumerate(Hist_raa2gy):
        print(i, h, type(h))
        if h == Hist_raa2gy[0]:
                continue
        r = h.Clone(f"r{i+1}")
        Ratios.append(r)
for i, r in enumerate(Ratios):
        color = int(colors[(i+1) % len(colors)])
        r.Divide(Hist_raa2gy[0])
        r.SetLineColor(color)
        r.SetLineWidth(2)
        r.SetStats(0)
Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Reco vertex pos y (cm)")
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
        Hist_raa2gy[0].GetXaxis().GetXmin(), 1.0,
        Hist_raa2gy[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_raa2gy.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_effnumtrk
c1 = ROOT.TCanvas("c_effnumtrk","c_effnumtrk",800,800)
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

for i, h in enumerate(Hist_effnumtrk):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_effnumtrk)
Hist_effnumtrk[0].SetMaximum(1.2*ymax)
Hist_effnumtrk[0].Draw("HIST")
for h in Hist_effnumtrk:
	if h == Hist_effnumtrk[0]:
		continue
	h.Draw("HIST SAME")
Hist_effnumtrk[0].GetXaxis().SetLabelSize(0)
Hist_effnumtrk[0].GetXaxis().SetTitleSize(0)
Hist_effnumtrk[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.46, 0.29, 0.83, 0.69)
leg.SetTextSize(0.035)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_effnumtrk):
	leg.AddEntry(h, Hist_effnumtrk_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_effnumtrk):
	print(i, h, type(h))
	if h == Hist_effnumtrk[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_effnumtrk[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Number of Tracks")
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
	Hist_effnumtrk[0].GetXaxis().GetXmin(), 1.0,
	Hist_effnumtrk[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_effnumtrk.png")
c1.Draw()
c1.Update()
input("Press Enter to close...")

## Hist_fakenumtrk
c1 = ROOT.TCanvas("c_fakenumtrk","c_fakenumtrk",800,800)
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

for i, h in enumerate(Hist_fakenumtrk):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_fakenumtrk)
Hist_fakenumtrk[0].SetMaximum(1.2*ymax)
Hist_fakenumtrk[0].Draw("HIST")
for h in Hist_fakenumtrk:
	if h == Hist_fakenumtrk[0]:
		continue
	h.Draw("HIST SAME")
Hist_fakenumtrk[0].GetXaxis().SetLabelSize(0)
Hist_fakenumtrk[0].GetXaxis().SetTitleSize(0)
Hist_fakenumtrk[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.5, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_fakenumtrk):
	leg.AddEntry(h, Hist_fakenumtrk_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_fakenumtrk):
	print(i, h, type(h))
	if h == Hist_fakenumtrk[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_fakenumtrk[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Number of Tracks")
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
	Hist_fakenumtrk[0].GetXaxis().GetXmin(), 1.0,
	Hist_fakenumtrk[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_fakenumtrk.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_pvresz
c1 = ROOT.TCanvas("c_pvresz","c_pvresz",800,800)
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

for i, h in enumerate(Hist_pvresz):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_pvresz)
Hist_pvresz[0].SetMaximum(1.2*ymax)
Hist_pvresz[0].Draw("HIST")
for h in Hist_pvresz:
	if h == Hist_pvresz[0]:
		continue
	h.Draw("HIST SAME")
Hist_pvresz[0].GetXaxis().SetLabelSize(0)
Hist_pvresz[0].GetXaxis().SetTitleSize(0)
Hist_pvresz[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_pvresz):
	leg.AddEntry(h, Hist_pvresz_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_pvresz):
	print(i, h, type(h))
	if h == Hist_pvresz[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_pvresz[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in z (#mum)")
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
	Hist_pvresz[0].GetXaxis().GetXmin(), 1.0,
	Hist_pvresz[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_pvresz.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_pvresx
c1 = ROOT.TCanvas("c_pvresx","c_pvresx",800,800)
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

for i, h in enumerate(Hist_pvresx):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_pvresx)
Hist_pvresx[0].SetMaximum(1.2*ymax)
Hist_pvresx[0].Draw("HIST")
for h in Hist_pvresx:
	if h == Hist_pvresx[0]:
		continue
	h.Draw("HIST SAME")
Hist_pvresx[0].GetXaxis().SetLabelSize(0)
Hist_pvresx[0].GetXaxis().SetTitleSize(0)
Hist_pvresx[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_pvresx):
	leg.AddEntry(h, Hist_pvresx_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_pvresx):
	print(i, h, type(h))
	if h == Hist_pvresx[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_pvresx[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in x (#mum)")
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
	Hist_pvresx[0].GetXaxis().GetXmin(), 1.0,
	Hist_pvresx[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_pvresx.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_pvresy
c1 = ROOT.TCanvas("c_pvresy","c_pvresy",800,800)
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

for i, h in enumerate(Hist_pvresy):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_pvresy)
Hist_pvresy[0].SetMaximum(1.2*ymax)
Hist_pvresy[0].Draw("HIST")
for h in Hist_pvresy:
	if h == Hist_pvresy[0]:
		continue
	h.Draw("HIST SAME")
Hist_pvresy[0].GetXaxis().SetLabelSize(0)
Hist_pvresy[0].GetXaxis().SetTitleSize(0)
Hist_pvresy[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_pvresy):
	leg.AddEntry(h, Hist_pvresy_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_pvresy):
	print(i, h, type(h))
	if h == Hist_pvresy[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_pvresy[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in y (#mum)")
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
	Hist_pvresy[0].GetXaxis().GetXmin(), 1.0,
	Hist_pvresy[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_pvresy.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_allresz
c1 = ROOT.TCanvas("c_allresz","c_allresz",800,800)
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

for i, h in enumerate(Hist_allresz):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_allresz)
Hist_allresz[0].SetMaximum(1.2*ymax)
Hist_allresz[0].Draw("HIST")
for h in Hist_allresz:
	if h == Hist_allresz[0]:
		continue
	h.Draw("HIST SAME")
Hist_allresz[0].GetXaxis().SetLabelSize(0)
Hist_allresz[0].GetXaxis().SetTitleSize(0)
Hist_allresz[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_allresz):
	leg.AddEntry(h, Hist_allresz_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_allresz):
	print(i, h, type(h))
	if h == Hist_allresz[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_allresz[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in z (#mum)")
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
	Hist_allresz[0].GetXaxis().GetXmin(), 1.0,
	Hist_allresz[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_allresz.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_allresx
c1 = ROOT.TCanvas("c_allresx","c_allresx",800,800)
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

for i, h in enumerate(Hist_allresx):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_allresx)
Hist_allresx[0].SetMaximum(1.2*ymax)
Hist_allresx[0].Draw("HIST")
for h in Hist_allresx:
	if h == Hist_allresx[0]:
		continue
	h.Draw("HIST SAME")
Hist_allresx[0].GetXaxis().SetLabelSize(0)
Hist_allresx[0].GetXaxis().SetTitleSize(0)
Hist_allresx[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_allresx):
	leg.AddEntry(h, Hist_allresx_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_allresx):
	print(i, h, type(h))
	if h == Hist_allresx[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_allresx[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in x (#mum)")
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
	Hist_allresx[0].GetXaxis().GetXmin(), 1.0,
	Hist_allresx[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_allresx.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_allresy
c1 = ROOT.TCanvas("c_allresy","c_allresy",800,800)
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

for i, h in enumerate(Hist_allresy):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_allresy)
Hist_allresy[0].SetMaximum(1.2*ymax)
Hist_allresy[0].Draw("HIST")
for h in Hist_allresy:
	if h == Hist_allresy[0]:
		continue
	h.Draw("HIST SAME")
Hist_allresy[0].GetXaxis().SetLabelSize(0)
Hist_allresy[0].GetXaxis().SetTitleSize(0)
Hist_allresy[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_allresy):
	leg.AddEntry(h, Hist_allresy_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_allresy):
	print(i, h, type(h))
	if h == Hist_allresy[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_allresy[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in y (#mum)")
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
	Hist_allresy[0].GetXaxis().GetXmin(), 1.0,
	Hist_allresy[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_allresy.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_mresz
c1 = ROOT.TCanvas("c_mresz","c_mresz",800,800)
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

for i, h in enumerate(Hist_mresz):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_mresz)
Hist_mresz[0].SetMaximum(1.2*ymax)
Hist_mresz[0].Draw("HIST")
for h in Hist_mresz:
	if h == Hist_mresz[0]:
		continue
	h.Draw("HIST SAME")
Hist_mresz[0].GetXaxis().SetLabelSize(0)
Hist_mresz[0].GetXaxis().SetTitleSize(0)
Hist_mresz[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_mresz):
	leg.AddEntry(h, Hist_mresz_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_mresz):
	print(i, h, type(h))
	if h == Hist_mresz[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_mresz[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in z (#mum)")
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
	Hist_mresz[0].GetXaxis().GetXmin(), 1.0,
	Hist_mresz[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_mresz.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_mresx
c1 = ROOT.TCanvas("c_mresx","c_mresx",800,800)
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

for i, h in enumerate(Hist_mresx):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_mresx)
Hist_mresx[0].SetMaximum(1.2*ymax)
Hist_mresx[0].Draw("HIST")
for h in Hist_mresz:
	if h == Hist_mresz[0]:
		continue
	h.Draw("HIST SAME")
Hist_mresx[0].GetXaxis().SetLabelSize(0)
Hist_mresx[0].GetXaxis().SetTitleSize(0)
Hist_mresx[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_mresx):
	leg.AddEntry(h, Hist_mresx_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_mresx):
	print(i, h, type(h))
	if h == Hist_mresx[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_mresx[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in x (#mum)")
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
	Hist_mresx[0].GetXaxis().GetXmin(), 1.0,
	Hist_mresx[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_mresx.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")

## Hist_mresy
c1 = ROOT.TCanvas("c_mresy","c_mresy",800,800)
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

for i, h in enumerate(Hist_mresy):
	color = int(colors[i % len(colors)])
	h.SetLineColor(color)
	h.SetLineWidth(2)
	h.SetStats(0)
ymax = max(h.GetMaximum() for h in Hist_mresy)
Hist_mresy[0].SetMaximum(1.2*ymax)
Hist_mresy[0].Draw("HIST")
for h in Hist_mresy:
	if h == Hist_mresy[0]:
		continue
	h.Draw("HIST SAME")
Hist_mresy[0].GetXaxis().SetLabelSize(0)
Hist_mresy[0].GetXaxis().SetTitleSize(0)
Hist_mresy[0].GetYaxis().SetTitle("N")
leg = ROOT.TLegend(0.7, 0.5, 0.92, 0.92)
leg.SetTextSize(0.04)
leg.SetMargin(0.2)
for i, h in enumerate(Hist_mresy):
	leg.AddEntry(h, Hist_mresy_labels[i], "l")
leg.Draw()

### ratio

pad2.cd()

Ratios = []
for i, h in enumerate(Hist_mresy):
	print(i, h, type(h))
	if h == Hist_mresy[0]:
		continue
	r = h.Clone(f"r{i+1}")
	Ratios.append(r)
for i, r in enumerate(Ratios):
	color = int(colors[(i+1) % len(colors)])
	r.Divide(Hist_mresy[0])
	r.SetLineColor(color)
	r.SetLineWidth(2)
	r.SetStats(0)
	Ratios[0].SetTitle("")
Ratios[0].GetYaxis().SetTitle("Ratio")
Ratios[0].GetYaxis().SetNdivisions(505)
Ratios[0].GetYaxis().SetTitleSize(0.08)
Ratios[0].GetYaxis().SetTitleOffset(0.5)
Ratios[0].GetYaxis().SetLabelSize(0.08)

Ratios[0].GetXaxis().SetTitle("Resolution in y (#mum)")
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
	Hist_mresy[0].GetXaxis().GetXmin(), 1.0,
	Hist_mresy[0].GetXaxis().GetXmax(), 1.0
)
line.SetLineStyle(2)
line.Draw()
c1.SaveAs("mintrkweightPlots/Hist_mresy.png")
#c1.Draw()
#c1.Update()
#input("Press Enter to close...")
