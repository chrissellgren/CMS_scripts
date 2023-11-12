import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple_qcorr_noreco.root")
file2 = ROOT.TFile("Ntuple_qcorr_noreco.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
leaf = branch.GetLeaf("charge_corr")

tree2 = file2.Get("clustTree")
branch2 = tree2.GetBranch("clust")
leaf2 = branch2.GetLeaf("charge")

h = ROOT.TH1F("histogram", "qcorr", 100, 0, 200e3) 
h2 = ROOT.TH1F("histogram", "Comparison original/corrected charge, no reco, only interpolation", 100, 0, 200e3) 

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    tree2.GetEntry(entry)
    value2 = leaf2.GetValue()
    h.Fill(value)
    h2.Fill(value2)
    #print(value, value2)

# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
h2.Draw()
h.SetLineWidth(2)

h.Draw("SAME")
h2.SetLineWidth(2)
h2.SetLineColor(ROOT.kRed)

legend = ROOT.TLegend(0.78, 0.6, 0.98, 0.75)
legend.AddEntry(h, "Corrected charge depo", "l")  # "l" for line
legend.AddEntry(h2, "Original charge depo", "l")
legend.Draw()

canvas.SetTitle("Comparison original/corrected charge, no reco, only interpolation")
canvas.SaveAs("plots/3_comp_noreco.png")
file.Close()

