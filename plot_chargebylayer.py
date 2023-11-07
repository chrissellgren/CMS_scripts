import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
branch2 = tree.GetBranch("mod_on")
leaf = branch.GetLeaf("charge")
leaf2 = branch2.GetLeaf("layer")
h1 = ROOT.TH1F("histogram", "Charge depo on layer 1", 100, 0, 200e3)
h2 = ROOT.TH1F("histogram2", "Charge depo on layer 2", 100, 0, 200e3) 
h3 = ROOT.TH1F("histogram3", "Charge depo on layer 3", 100, 0, 200e3) 
h4 = ROOT.TH1F("histogram4", "Charge depo on layer 4", 100, 0, 200e3)  

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    layer = int(leaf2.GetValue())
    #print(layer)
    #print(value)
    if (layer==1):
        h1.Fill(value)
    elif (layer==2):
        h2.Fill(value)
    elif (layer==3):
        h3.Fill(value)
    elif (layer==4):
        h4.Fill(value)
    else:
        pass
        #print("layer is out of control")

# Define a Landau fit function
landau_func = ROOT.TF1("landau_func", "landau", 0, 300e3)
landau_func.SetParameters(1.0, 20000.0, 1000.0)  # Set initial parameters

h1.Fit("landau_func", "R")  # "R" indicates to use the range specified in the function
fit_function1 = h1.GetFunction("landau_func")
MPV1 = fit_function1.GetParameter(1)
width1 = fit_function1.GetParameter(2)
print("Most Probable Value (MPV):", MPV1)
print("Width:", width1)

h2.Fit("landau_func", "R")
fit_function2 = h2.GetFunction("landau_func")
MPV2 = fit_function2.GetParameter(1)
width2 = fit_function2.GetParameter(2)
print("Most Probable Value (MPV):", MPV2)
print("Width:", width2)

h3.Fit("landau_func", "R")
fit_function3 = h3.GetFunction("landau_func")
MPV3 = fit_function3.GetParameter(1)
width3 = fit_function3.GetParameter(2)
print("Most Probable Value (MPV):", MPV3)
print("Width:", width3)

h4.Fit("landau_func", "R")
fit_function4 = h4.GetFunction("landau_func")
MPV4 = fit_function4.GetParameter(1)
width4 = fit_function4.GetParameter(2)
print("Most Probable Value (MPV):", MPV4)
print("Width:", width4)

# Create a canvas and draw the histogram
c1 = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
h1.Draw()
c1.Update()
# Add MPV text using TText
mpv_text = ROOT.TText(100e3, 30, "MPV: {:.2f}".format(MPV1))
mpv_text.SetTextSize(0.06)
mpv_text.SetTextAlign(22)  # Center align text
mpv_text.Draw()
c1.SaveAs("plots/cdepo_layer1.png")

c2 = ROOT.TCanvas("canvas2", "canvas", 1500, 1000)
h2.Draw()
c2.Update()
# Add MPV text using TText
mpv_text = ROOT.TText(100e3, 30, "MPV: {:.2f}".format(MPV2))
mpv_text.SetTextSize(0.06)
mpv_text.SetTextAlign(22)  # Center align text
mpv_text.Draw()
c2.SaveAs("plots/cdepo_layer2.png")

c3 = ROOT.TCanvas("canvas3", "canvas", 1500, 1000)
h3.Draw()
c3.Update()
# Add MPV text using TText
mpv_text = ROOT.TText(100e3, 30, "MPV: {:.2f}".format(MPV3))
mpv_text.SetTextSize(0.06)
mpv_text.SetTextAlign(22)  # Center align text
mpv_text.Draw()
c3.SaveAs("plots/cdepo_layer3.png")

c4 = ROOT.TCanvas("canvas4", "canvas", 1500, 1000)
h4.Draw()
c4.Update()
# Add MPV text using TText
mpv_text = ROOT.TText(100e3, 30, "MPV: {:.2f}".format(MPV4))
mpv_text.SetTextSize(0.06)
mpv_text.SetTextAlign(22)  # Center align text
mpv_text.Draw()
c4.SaveAs("plots/cdepo_layer4.png")
file.Close()