import ROOT
import matplotlib.pyplot as plt
import numpy as np

param_min = 0.01
param_max = 0.5
param_num = 10
dp = (param_max - param_min)/(param_num - 1)
params_given = [0.5555555555555556, 0.6111111111111112, 0.6666666666666666, 0.7222222222222222, 0.7777777777777778, 0.8333333333333333, 0.8888888888888888, 0.9444444444444444, 1.0]

param_manual = False

#Paraneter
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

#Efficiency
e_globs = []
for i in inter:
	for p in params:
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		h_N = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/GenAllAssoc2RecoMatched_NumTracks")
		h_eff = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/effic_vs_NumTracks")

		num = 0
		denom = 0
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
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		h_Nrec = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2Gen_NumTracks")
		h_fake = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/fakerate_vs_NumTracks")

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
#PV tagging
NoRecFrac =[]
RecAndIdFrac = []
RecNoIdFrac = []

for i in inter:
	for p in params:
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		h_PV_tag = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/TruePVLocationIndexCumulative")

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
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/new2CnewF/outputfiles/run_p_%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%(i,str(p)))
		h_res_PV_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolZ")
		h_res_PV_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolX")
		h_res_PV_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoPVAssoc2GenPVMatched_ResolY")

		h_res_All_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolZ")
		h_res_All_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolX")
		h_res_All_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatched_ResolY")

		h_res_merged_Z = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolZ")
		h_res_merged_X = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolX")
		h_res_merged_Y = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/RecoAllAssoc2GenMatchedMerged_ResolY")

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

###############################################################

# Plotting

plt.plot(params, e_globs)
plt.xlabel("mintrkweight")
plt.ylabel(r"Efficiency $\overline{\epsilon}$")
plt.title("Efficiency vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, f_globs)
plt.xlabel("mintrkweight")
plt.ylabel(r"Fake rate $\overline{f}$")
plt.title("Fake rate vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, NoRecFrac)
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV not reconstructed")
plt.title("Fraction of events with PV not reconstructed vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, RecAndIdFrac)
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV reconstructed and identified")
plt.title("Fraction of events with PV reconstructed and identified vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, RecNoIdFrac)
plt.xlabel("mintrkweight")
plt.ylabel("Fraction of events with PV reconstructed but not identified")
plt.title("Fraction of events with PV reconstructed but not identified vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, PV_Z_Res)
plt.xlabel("mintrkweight")
plt.ylabel(r"PV resolution z (${\mu} m$)")
plt.title("PV resolution z vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, All_Z_Res)
plt.xlabel("mintrkweight")
plt.ylabel(r"All resolution z (${\mu} m$)")
plt.title("All resolution z vs mintrkweight")
plt.grid()
plt.show()

plt.plot(params, Merged_Z_Res)
plt.xlabel("mintrkweight")
plt.ylabel(r"Merged resolution z (${\mu} m$)")
plt.title("Merged resolution z vs mintrkweight")
plt.grid()
plt.show()
