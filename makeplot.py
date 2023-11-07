import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple.root")
layer = "all" # -1 default for all layers

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
leaf = branch.GetLeaf("charge")
layerbranch = tree.GetBranch("mod_on")
layerleaf = layerbranch.GetLeaf("layer")

h = ROOT.TH1F("histogram", "Charge deposited on all layers", 100, 0, 200e3) 
h1 = ROOT.TH1F("histogram", "Charge depo on layer 1", 100, 0, 200e3)
h2 = ROOT.TH1F("histogram2", "Charge depo on layer 2", 100, 0, 200e3) 
h3 = ROOT.TH1F("histogram3", "Charge depo on layer 3", 100, 0, 200e3) 
h4 = ROOT.TH1F("histogram4", "Charge depo on layer 4", 100, 0, 200e3)

hlist = [h, h1, h2, h3, h4]

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    h.Fill(value)
    layer = layerleaf.GetValue()
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

print("Making fxns...")

# Define fit functions
landau_func = ROOT.TF1("landau_func", "landau", 0, 300e3)
gauss_func = ROOT.TF1("gauss_func", "gaus", 12e3, 31e3)

# set params for each
landau_func.SetParameter(0, 20e3)  # MPV of the Landau
landau_func.SetParameter(1, 1e3)  # Sigma of the Landau
gauss_func.SetParameter(0, 20e3)  # Mean of the Gaussian
gauss_func.SetParameter(1, 1e3)  # Sigma of the Gaussian

print("Doing easy fits...")

# Fit the histogram with each of the functions.
h.Draw()
h.Fit(gauss_func, "R")
h.Fit(landau_func, "R+")

print("helllooooo")

# get params to feed to to the sensitive convolution
gaussfit = h.GetFunction("gauss_func")
landaufit = h.GetFunction("landau_func")
# draw the first two fits happens implicitly with the fit
gaussfit.SetLineColor(ROOT.kRed)
landaufit.SetLineColor(ROOT.kViolet)
landaufit.SetLineWidth(3)
gaussfit.SetLineWidth(3)

# pull params
g_mean = gaussfit.GetParameter(0)
g_sig  = gaussfit.GetParameter(1)
l_mpv = landaufit.GetParameter(0)
l_sig  = landaufit.GetParameter(1)

print("Making convolutions...")

f_conv = ROOT.TF1Convolution("landau", "gaus", -1000, 300e3+1000, True)
f_conv.SetRange(-1000, 300e3+1000)
f_conv.SetNofPointsFFT(1000)
f_conv.Draw("same")

f = ROOT.TF1("f", f_conv, 0.0, 300e3, f_conv.GetNpar())
f.SetParameters(10e3,l_mpv, l_sig, g_mean, g_sig)

for i,h in enumerate(hlist):
    print("Drawing canvas...")
    # Create a canvas and draw the histogram
    canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
    for hist in hlist:
        hist.SetLineWidth(3)
        hist.Draw()
    canvas.Update()

    h.Fit("f","R+")
    vavfit = h.GetFunction("f")
    vavfit.SetLineColor(ROOT.kGreen)
    vavfit.SetLineWidth(4)
    MPV = vavfit.GetParameter(4) * 10
    line = ROOT.TLine(MPV,0,MPV,230)
    line.SetLineColor(ROOT.kOrange)
    line.SetLineWidth(3)
    line.Draw()

    legend = ROOT.TLegend(0.78, 0.5, 0.98, 0.75)
    legend.AddEntry(h, "Charge Depo", "l")  # "l" for line
    #legend.AddEntry(landaufit, "Landau Fit", "l")
    #legend.AddEntry(gaussfit, "Gauss Fit", "l")
    legend.AddEntry(vavfit, "Convolution (Vavilov) Fit", "l")
    legend.AddEntry(line, "p4 of Convolution", "l")
    legend.Draw()
    canvas.SaveAs("plots/chargedepo_withconvolution_layer%d.png" % i)
    

# draw a TLine where the MPV should be for the vav fit



# make a convolution fxn
#vavilov_func = ROOT.TF1Convolution(gauss_new, landaufit, 0, 300e3, True)
#f0 = ROOT.TF1("fdata", vavilov_func, 0, 300e3, vavilov_func.GetNpar())
#f0.SetLineColor(ROOT.kBlack)
#f0.Draw("same")

# set vav params equal to output from the gauss, landau fits
#vavilov_func.SetParameter(0, g_mean) 
#vavilov_func.SetParameter(1, g_sig ) 
#vavilov_func.SetParameter(2, l_mean) 
#vavilov_func.SetParameter(3, l_sig ) 

#h.Fit(vavilov_func, "R+")
#vavfit = h.GetFunction("vavilov_func")


#landaufit.Draw("same")
#gaussfit.Draw("same")
#vavfit.Draw("same")

# Add a legend
legend = ROOT.TLegend(0.78, 0.5, 0.98, 0.75)
legend.AddEntry(h, "Charge Depo", "l")  # "l" for line
legend.AddEntry(landaufit, "Landau Fit", "l")
legend.AddEntry(gaussfit, "Gauss Fit", "l")
legend.AddEntry(vavfit, "Convolution (Vavilov) Fit", "l")
legend.AddEntry(line, "p4 of Convolution", "l")
legend.Draw()

# Add MPV text using TText
#mpv_text = ROOT.TText(100e3, 200, "MPV: {:.2f}".format(MPV))
#mpv_text.SetTextSize(0.06)
#mpv_text.SetTextAlign(22)  # Center align text
#mpv_text.Draw()
canvas.SaveAs("plots/chargedepo_alllayers.png")
file.Close()

###
## Define two separate TF1 functions for the Gaussian and Landau distributions.
#gauss_function = ROOT.TF1("gauss_function", "TMath::Gaus(x, [mean_gauss], [sigma_gauss])", [x_min], [x_max])
#landau_function = ROOT.TF1("landau_function", "TMath::Landau(x, [mpv_landau], [sigma_landau])", [x_min], [x_max])
#
## Create a new TF1 by convolving the two functions.
#convolution_function = gauss_function.Convolution(landau_function, x_min, x_max)
#
## Set the parameters for the Gaussian and Landau functions later.
#convolution_function.SetParameter(0, initial_parameter_value_1)  # Mean of the Gaussian
#convolution_function.SetParameter(1, initial_parameter_value_2)  # Sigma of the Gaussian
#convolution_function.SetParameter(2, initial_parameter_value_3)  # Most Probable Value (MPV) of the Landau
#convolution_function.SetParameter(3, initial_parameter_value_4)  # Sigma of the Landau