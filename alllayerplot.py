import ROOT
import sys

ROOT.gROOT.SetBatch(True) #stop the canvas being drawn

# Open the ROOT file
file = ROOT.TFile("Ntuple_2_369873.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
leaf = branch.GetLeaf("charge_corr")
leaf2 = branch.GetLeaf("charge")
layerbranch = tree.GetBranch("mod_on")
layerleaf = layerbranch.GetLeaf("layer")


h2 = ROOT.TH1F("histogram", "Charge deposited on all layers, run 369/873, qscale adjusted", 100, 0, 200e3) 
h = ROOT.TH1F("histogram", "Charge deposited on all layers, qscale adjusted", 100, 0, 200e3) 

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    value2 = leaf2.GetValue()
    h.Fill(value)
    h2.Fill(value2)

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
h.Fit(gauss_func, "R")
h.Fit(landau_func, "R+")

# get params to feed to to the sensitive convolution
gaussfit = h.GetFunction("gauss_func")
landaufit = h.GetFunction("landau_func")
# draw the first two fits happens implicitly with the fit
gaussfit.SetLineColor(ROOT.kOrange)
landaufit.SetLineColor(ROOT.kViolet)
landaufit.SetLineWidth(3)
gaussfit.SetLineWidth(3)
gaussfit.Draw()
landaufit.Draw()

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
f.SetParameters(0.1,l_mpv, l_sig, g_mean, g_sig)

print("Drawing canvas...")
# Create a canvas and draw the histogram
canvas = ROOT.TCanvas("canvas", "canvas", 1500, 1000)
h2.Draw()
h2.SetLineColor(ROOT.kBlack)
h.Draw("same")
h.SetLineWidth(3)
h.Fit("f","R+")

vavfit = h.GetFunction("f")
vavfit.SetLineColor(ROOT.kGreen)
vavfit.SetLineWidth(4)

MPV = vavfit.GetMaximumX()
line = ROOT.TLine(MPV,0,MPV,vavfit(MPV))
line.SetLineColor(ROOT.kRed)
line.SetLineWidth(4)
line.Draw()

legend = ROOT.TLegend(0.70, 0.45, 0.98, 0.75)
legend.AddEntry(h2, "Original charge dep", "l")  # "l" for line
legend.AddEntry(h, "Corrected charge", "l")  # "l" for line
legend.AddEntry(landaufit, "Landau Fit", "l")
legend.AddEntry(gaussfit, "Gauss Fit", "l")
legend.AddEntry(vavfit, "Convolution Fit", "l")
legend.AddEntry(line, "MPV of Convolution", "l")
legend.Draw()

# Add MPV text using TText
mpv_text = ROOT.TText(100e3, vavfit(MPV) , "MPV: {:.2f}".format(MPV))
mpv_text.SetTextSize(0.06)
mpv_text.SetTextAlign(22)  # Center align text
mpv_text.Draw()

canvas.SaveAs("plots/13_newrun_corrected_withfit.png")
    

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
#legend = ROOT.TLegend(0.78, 0.5, 0.98, 0.75)
#legend.AddEntry(h, "Charge Depo", "l")  # "l" for line
#legend.AddEntry(landaufit, "Landau Fit", "l")
#legend.AddEntry(gaussfit, "Gauss Fit", "l")
#legend.AddEntry(vavfit, "Convolution (Vavilov) Fit", "l")
#legend.AddEntry(line, "p4 of Convolution", "l")
#legend.Draw()

# Add MPV text using TText
#mpv_text = ROOT.TText(100e3, 200, "MPV: {:.2f}".format(MPV))
#mpv_text.SetTextSize(0.06)
#mpv_text.SetTextAlign(22)  # Center align text
#mpv_text.Draw()
#canvas.SaveAs("plots/chargedepo_alllayers.png")
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