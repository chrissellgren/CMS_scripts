import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple_1_interp_newleaves.root")
file2 = ROOT.TFile("Ntuple_1_interp_newleaves.root")
file = ROOT.TFile("Ntuple_2_369873.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("trajTree")
branch = tree.GetBranch("clust")
#branch = tree.GetBranch("event")
leaf = branch.GetLeaf("glz")

layerbranch = tree.GetBranch("mod_on")
layerleaf = layerbranch.GetLeaf("layer")

tree2 = file2.Get("clustTree")
branch2 = tree2.GetBranch("clust")
leaf2 = branch2.GetLeaf("charge")

h = ROOT.TH1F("histogram", "Global z of Layer 1 clusters for first 30 trajectories", 200, -30, 30) 
h2 = ROOT.TH1F("histogram", "Comparing charge depo before/after irradiation correction", -10, 0, 200e3) 

# Loop over the entries in the tree and fill the histogram
for entry in range(30):#tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    layer = layerleaf.GetValue()
    tree2.GetEntry(entry)
    value2 = leaf2.GetValue()
    print(layer)
    if (layer ==1):
        h.Fill(value)
        #print(value)
    h2.Fill(value2)
    #print(value, value2)

# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
h.Draw()
h.GetXaxis().SetTitle("Global Z (mm)")
h.GetYaxis().SetTitle("Number of clusters / 300um")
h.SetLineWidth(2)

#h2.Draw("SAME")
#h2.SetLineWidth(2)
#h2.SetLineColor(ROOT.kRed)

#legend = ROOT.TLegend(0.70, 0.6, 0.98, 0.75)
#legend.AddEntry(h2, "Original charge depo", "l")
#legend.AddEntry(h, "Original*qscale/r_qmeas_qtrue", "l")  # "l" for line
#legend.Draw()

#canvas.SetTitle("N_clusters/event")
canvas.SaveAs("plots/20_tracksep.png")
file.Close()

