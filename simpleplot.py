import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple_fixedcharge_withcorr.root")
file2 = ROOT.TFile("Ntuple_qcorr.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
leaf = branch.GetLeaf("charge")

tree2 = file2.Get("clustTree")
branch2 = tree2.GetBranch("clust")
leaf2 = branch2.GetLeaf("charge")

h = ROOT.TH1F("histogram", "qscale", 100, -2, 2) 

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    tree2.GetEntry(entry)
    value2 = leaf2.GetValue()
    h.Fill(value)
    print(value, value2)

# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
h.Draw()
h.SetLineWidth(2)
canvas.SaveAs("plots/charged_fixed.png")
file.Close()

