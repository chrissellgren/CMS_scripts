import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple_1_interp_newleaves.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
qscale_leaf = branch.GetLeaf("qscale")
r_qmeas_qtrue_leaf = branch.GetLeaf("r_qmeas_qtrue")
corr_factor_leaf = branch.GetLeaf("corr_factor")

charge_leaf = branch.GetLeaf("charge")
charge_qscale_leaf = branch.GetLeaf("charge_qscale")
charge_r_qmeas_qtrue_leaf = branch.GetLeaf("charge_r_qmeas_qtrue")
charge_corr_leaf = branch.GetLeaf("charge_corr")


h1 = ROOT.TH1F("histogram", "qscale", 100, 1, 1.5) 
h2 = ROOT.TH1F("histogram", "r_qmeas_qtrue", 100, 0.7, 1) 
h3 = ROOT.TH1F("histogram","corr_factor", 100, 1, 2)

leaf = corr_factor_leaf
h = h3

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    #value2 = leaf2.GetValue()
    h.Fill(1.6574821472167969)
    print(value)
    #h2.Fill(value2)
    #print(value, value2)

# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)

h.SetLineWidth(2)
h.Draw("SAME")
#h2.SetLineWidth(2)
#h2.SetLineColor(ROOT.kRed)

#legend = ROOT.TLegend(0.70, 0.6, 0.98, 0.75)
##legend.AddEntry(h2, "Original charge depo", "l")
#legend.AddEntry(h, "qscale", "l")  # "l" for line
#legend.Draw()

#canvas.SetTitle("r_qmeas_qtrue")
canvas.SaveAs("plots/10_wrong_corrfactor.png")
file.Close()

