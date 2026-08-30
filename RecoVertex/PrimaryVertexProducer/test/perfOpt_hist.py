from myFunctions import *
from jobScriptsConfig import user, mainpath, workarea
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
	"--foldername",
	type=str,
)
parser.add_argument(
	"--firstline",
	type=int,
)
parser.add_argument(
	"--lastline",
	type=int,
)
args = parser.parse_args()

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
    "RecoAllAssoc2Gen_Y",
    "tagVtxTrksVsZ",
    "otherVtxTrksVsZ"
]

run_list = []
list = []
with open(args.run_path_list) as file:
	for line in file:
		list.append(line)
for i, line in enumerate(list):
	if i+1 < args.firstline or i+1 > args.lastline:
		continue
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


RUN_HIST_H = []
for r in run_list:
	print(r)
for H in HIST_H:
	h_results = []
	for r in run_list:
		f = ROOT.TFile.Open("/eos/user/o/oyildiri/OldNewCF/%s/DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"%str(r[6]))
		if H == "tagVtxTrksVsZ" or H == "otherVtxTrksVsZ":
			if r[1] == "4D" or r[1] == "4DinBlocks":
				h = f.Get("DQMData/Run 1/OfflinePV/Run summary/offlinePrimaryVertices4D/%s"%H)
			else:
				h = f.Get("DQMData/Run 1/OfflinePV/Run summary/offlinePrimaryVertices/%s"%H)
		else:
			if r[1] == "4D" or r[1] == "4DinBlocks":
				h = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices4D/%s"%H)
			else:
				h = f.Get("DQMData/Run 1/Vertexing/Run summary/PrimaryVertexV/offlinePrimaryVertices/%s"%H)
		print(H)
		h.SetDirectory(0)
		if r[3] == "P":
			label = f"{r[0]}/{r[1]}/{r[4]:.3f}"
		elif r[3] == "I":
			label = f"{r[0]}/{r[1]}"
		elif r[3] == "B2":
			label = f"{r[0]}/{r[1]}/{r[4]}/{r[2]}"
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
	ROOT.kCyan+3,
	ROOT.kPink+7,
	ROOT.kTeal+3,
	ROOT.kSpring+5,
	ROOT.kYellow+2,
	ROOT.kOrange+1,
	ROOT.kRed+2,
	ROOT.kBlue+2,
	ROOT.kGreen+3,
	ROOT.kMagenta+2,
	ROOT.kGray+3,
	ROOT.kGray+2
]

def RootTH1FPlot(hist_folder,hist_name, hist_list,x1,y1,x2,y2,xtitle,ytitle):
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
	c1.SaveAs(f"OptPlots_HIST/{hist_folder}/{hist_name}.png")

foldername = args.foldername
path = f"{workarea}/OptPlots_HIST/{foldername}"
Path(path).mkdir(parents=True, exist_ok=True)
for RH in RUN_HIST_H:
	if RH[0] == "RecoAllAssoc2Gen_NumTracks":
		RootTH1FPlot(foldername,RH[0], RH, 0.5, 0.5, 0.92, 0.92, "Number of tracks in vertex fit", "N")
	elif RH[0] == "RecoAllAssoc2Gen_X":
		RootTH1FPlot(foldername,RH[0], RH, 0.6, 0.4, 0.92, 0.92, "Reco vertex pos x (cm)", "N")
	elif RH[0] == "RecoAllAssoc2Gen_Y":
		RootTH1FPlot(foldername,RH[0], RH, 0.6, 0.4, 0.92, 0.92, "Reco vertex pos y (cm)", "N")
	elif RH[0] == "effic_vs_NumTracks":
		RootTH1FPlot(foldername,RH[0], RH, 0.46, 0.29, 0.83, 0.69,"Number of tracks in vertex fit","Efficiency")
	elif RH[0] == "fakerate_vs_NumTracks":
		RootTH1FPlot(foldername,RH[0], RH, 0.5, 0.5, 0.92, 0.92, "Number of tracks in vertex fit", "Fake rate")
	elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolZ":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (cm)", "N")
	elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolX":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (cm)", "N")
	elif RH[0] == "RecoPVAssoc2GenPVMatched_ResolY":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatched_ResolZ":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatched_ResolX":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatched_ResolY":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolZ":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Z (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolX":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in X (cm)", "N")
	elif RH[0] == "RecoAllAssoc2GenMatchedMerged_ResolY":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Resolution in Y (cm)", "N")
	elif RH[0] == "tagVtxTrksVsZ":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Z (cm)", "Tracks / selected PV")
	elif RH[0] == "otherVtxTrksVsZ":
		RootTH1FPlot(foldername,RH[0], RH, 0.7, 0.5, 0.92, 0.92, "Z (cm)", "Tracks / pileup vertex")
