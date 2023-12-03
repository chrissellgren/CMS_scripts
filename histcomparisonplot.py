import ROOT as R
import math
import os
import numpy as np
import matplotlib.pyplot as plt

R.gStyle.SetOptStat(0)
R.gStyle.SetGridColor(14)
R.gStyle.SetPadRightMargin(0.03)
R.gStyle.SetPadLeftMargin(0.12)

# pull file
file_in = R.TFile("rootfiles/Histos_1.root")

h_no1x1 = file_in.HSCParticleAnalyzer.BaseName.BefPreS_ProbQNoL1_Nsingleclusters
h_with1x1 = file_in.HSCParticleAnalyzer.BaseName.BefPreS_ProbQNoL1

numbins = h_no1x1.GetNbinsX()
x_bins = []
bin_diff = []
bins_quo = []
for i in range(1,numbins+1):
    x_bins.append(h_no1x1.GetXaxis().GetBinCenter(i))
    no1x1_thisbin = h_no1x1.GetBinContent(i)
    with1x1_thisbin = h_with1x1.GetBinContent(i)
    bin_diff.append(no1x1_thisbin - with1x1_thisbin)
    if with1x1_thisbin != 0:
        bins_quo.append(no1x1_thisbin/with1x1_thisbin)
    else:
        bins_quo.append(0)

print("got bins...")
plt.figure(figsize=(6,4),dpi=500)
print("plotting figure")
plt.plot(x_bins,bins_quo,linestyle='',marker='.',label="Ratio of no 1x1 to with 1x1 hists")
print("saving fig...")
plt.legend()
plt.xlabel("F_i_pixels")
plt.ylabel("Tracks/bin (no1x1 - with1x1)")
plt.savefig("plots/hscp/2_ratio.png")