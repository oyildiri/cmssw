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
        "--inputfile",
        type=str
)

parser.add_argument(
	"--tagging_type",
	type=str
)

parser.add_argument(
	"--xlabel",
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

def getbinvalue(H,run,bin):
        f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%run[6])
        if run[1] == "4D" or run[1] == "4DinBlocks":
                h_run = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices4D/%s"%H)
        else:
                h_run = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/%s"%H)
        h_run.SetDirectory(0)
        binvalue = h_run.GetBinCenter(bin)
        return binvalue

with open(f"{args.inputfile}.json", "r") as f:
	RUN_HISTP_RESULTS = json.load(f)

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
                if args.tagging_type == "only_by_int":
                        tag = [R[0][0]]
                else:
                        tag = [R[0][3],R[0][0],R[0][1]] ##
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
        print("START PLOTTING")
        np = 0
        ni = 0
        nb2 = 0
        for j, P in enumerate(YS[1]):
                ptcolorP = pltcolors[np % len(pltcolors)]
                ptcolorI = pltcolors[ni % len(pltcolors)]
                ptcolorB2 = pltcolors[nb2 % len(pltcolors)]
                ptcolor = pltcolors[j % len(pltcolors)]
                if args.tagging_type == "only_by_int":
                        xvalues = []
                        yvalues = []
                        for P1 in P[1]:
                                if P1[0][3] == "P":
                                        xvalues.append(f"{P1[0][1]}/{P1[0][4]:.3f}")
                                else:
                                        xvalues.append(f"{P1[0][1]}/{P1[0][2]}")
                                yvalues.append(P1[1])
                        plt.plot(xvalues, yvalues, color=ptcolor, label = f"{P[0][0]}")
                else:
                        if P[0][0] == "P":
                                xvalues = []
                                yvalues = []
                                for P1 in P[1]:
                                        xvalues.append(P1[0][4])
                                        yvalues.append(P1[1])
                                plt.plot(xvalues,yvalues,color=ptcolorP,label = f"{P[0][1]}")
                                np = np + 1
                        elif P[0][0] == "B2":
                                xvalues = []
                                yvalues = []
                                print("!!!!! ATTENTION HERE: !!!!!")
                                for P1 in P[1]:
                                        print(YS[0])
                                        print(P1)
                                        xvalues.append(f"{str(P1[0][4][0])}/{str(P1[0][4][1])} | {str(P1[0][2])}")
                                        yvalues.append(P1[1])
                                plt.plot(xvalues,yvalues,color=ptcolorB2,label = f"{P[0][1]}")
                                nb2 = nb2 + 1
                        elif P[0][0] == "I":
                                for P1 in P[1]:
                                        yvalue = P1[1]
                                        plt.axhline(y=yvalue,color=ptcolorI, label = f"{P[0][1]}")
                                ni = ni + 1
        # Titles, axis labels, plotting
        plt.xlabel(f"{args.xlabel}")
        if YS[0] == "e_glob":
                plt.ylabel(r"Efficiency $\overline{\epsilon}$")
                plt.title(f"Efficiency vs {args.xlabel}")
                plotname = "eff_mintrkweight.png"
        elif YS[0] == "f_glob":
                plt.title(f"Fake rate vs {args.xlabel}")
                plt.ylabel(r"Fake rate $\overline{f}$")
                plotname = "fakerate_mintrkweight.png"
        elif YS[0] == "f_glob_lowntrk":
                plt.title(f"Fake rate for low NumTrack (NumTrak < ~{binvalue}) vs {args.xlabel}")
                plt.ylabel(r"Fake rate $\overline{f}$")
                plotname = "fakerate_lowntrk_mintrkweight.png"
        elif YS[0] == "f_glob_highntrk":
                plt.title(f"Fake rate for high NumTrack (NumTrak > ~{binvalue}) vs {args.xlabel}")
                plt.ylabel(r"Fake rate $\overline{f}$")
                plotname = "fakerate_highntrk_mintrkweight.png"
        elif YS[0] == "NoRecFrac":
                plt.ylabel("Fraction of events with PV not reconstructed")
                plt.title(f"Fraction of events with PV not reconstructed vs {args.xlabel}")
                plotname = "NoRecFrac_mintrkweight.png"
        elif YS[0] == "RecAndIdFrac":
                plt.ylabel("Fraction of events with PV reconstructed and identified")
                plt.title(f"Fraction of events with PV reconstructed and identified vs {args.xlabel}")
                plotname = "RecAndIdFrac_mintrkweight.png"
        elif YS[0] == "RecNoIdFrac":
                plt.ylabel("Fraction of events with PV reconstructed but not identified")
                plt.title(f"Fraction of events with PV reconstructed but not identified vs {args.xlabel}")
                plotname = "RecNoIdFrac_mintrkweight.png"
        elif YS[0] == "PV_Z_Res":
                plt.ylabel(r"PV resolution z ($cm$)")
                plt.title(f"PV resolution z vs {args.xlabel}")
                plotname = "PV_Z_Res_mintrkweight.png"
        elif YS[0] == "PV_X_Res":
                plt.ylabel(r"PV resolution x ($cm$)")
                plt.title(f"PV resolution x vs {args.xlabel}")
                plotname = "PV_X_Res_mintrkweight.png"
        elif YS[0] == "PV_Y_Res":
                plt.ylabel(r"PV resolution y ($cm$)")
                plt.title(f"PV resolution y vs {args.xlabel}")
                plotname = "PV_Y_Res_mintrkweight.png"
        elif YS[0] == "PV_Z_Mean":
                plt.ylabel(r"PV resolution z mean ($cm$)")
                plt.title(f"PV resolution z mean vs {args.xlabel}")
                plotname = "PV_Z_Res_mean_mintrkweight.png"
        elif YS[0] == "PV_X_Mean":
                plt.ylabel(r"PV resolution x mean ($cm$)")
                plt.title(f"PV resolution x mean vs {args.xlabel}")
                plotname = "PV_X_Res_mean_mintrkweight.png"
        elif YS[0] == "PV_Y_Mean":
                plt.ylabel(r"PV resolution y mean ($cm$)")
                plt.title(f"PV resolution y mean vs {args.xlabel}")
                plotname = "PV_Y_Res_mean_mintrkweight.png"
        elif YS[0] == "All_Z_Res":
                plt.ylabel(r"All resolution z ($cm$)")
                plt.title(f"All resolution z vs {args.xlabel}")
                plotname = "All_Z_Res_mintrkweight.png"
        elif YS[0] == "All_X_Res":
                plt.ylabel(r"All resolution x ($cm$)")
                plt.title(f"All resolution x vs {args.xlabel}")
                plotname = "All_X_Res_mintrkweight.png"
        elif YS[0] == "All_Y_Res":
                plt.ylabel(r"All resolution y ($cm$)")
                plt.title(f"All resolution y vs {args.xlabel}")
                plotname = "All_Y_Res_mintrkweight.png"
        elif YS[0] == "All_Z_Mean":
                plt.ylabel(r"All resolution z mean ($cm$)")
                plt.title(f"All resolution z mean vs {args.xlabel}")
                plotname = "All_Z_Res_mean_mintrkweight.png"
        elif YS[0] == "All_X_Mean":
                plt.ylabel(r"All resolution x mean ($cm$)")
                plt.title(f"All resolution x mean vs {args.xlabel}")
                plotname = "All_X_Res_mean_mintrkweight.png"
        elif YS[0] == "All_Y_Mean":
                plt.ylabel(r"All resolution y mean ($cm$)")
                plt.title(f"All resolution y mean vs {args.xlabel}")
                plotname = "All_Y_Res_mean_mintrkweight.png"
        elif YS[0] == "Merged_Z_Res":
                plt.ylabel(r"Merged resolution z ($cm$)")
                plt.title(f"Merged resolution z vs {args.xlabel}")
                plotname = "Merged_Z_Res_mintrkweight.png"
        elif YS[0] == "Merged_X_Res":
                plt.ylabel(r"Merged resolution x ($cm$)")
                plt.title(f"Merged resolution x vs {args.xlabel}")
                plotname = "Merged_X_Res_mintrkweight.png"
        elif YS[0] == "Merged_Y_Res":
                plt.ylabel(r"Merged resolution y ($cm$)")
                plt.title(f"Merged resolution y vs {args.xlabel}")
                plotname = "Merged_Y_Res_mintrkweight.png"
        elif YS[0] == "Merged_Z_Mean":
                plt.ylabel(r"Merged resolution z mean ($cm$)")
                plt.title(f"Merged resolution z mean vs {args.xlabel}")
                plotname = "Merged_Z_Res_mean_mintrkweight.png"
        elif YS[0] == "Merged_X_Mean":
                plt.ylabel(r"Merged resolution x mean ($cm$)")
                plt.title(f"Merged resolution x mean vs {args.xlabel}")
                plotname = "Merged_X_Res_mean_mintrkweight.png"
        elif YS[0] == "Merged_Y_Mean":
                plt.ylabel(r"Merged resolution y mean ($cm$)")
                plt.title(f"Merged resolution y mean vs {args.xlabel}")
                plotname = "Merged_Y_Res_mean_mintrkweight.png"
        plt.grid()
        plt.legend(loc="upper left",fontsize=8)
        plt.tight_layout()
        os.makedirs("OptPlots", exist_ok=True)
        plt.savefig("OptPlots/%s"%plotname)
        print("PLOT SAVED")
        plt.close()

