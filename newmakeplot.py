import ROOT
import sys

ROOT.gROOT.SetBatch(True)  # Stop the canvas from being drawn

file = ROOT.TFile("Ntuple.root")

# Check if the file is successfully opened
if file.IsOpen():
    print("File successfully opened!")
else:
    print("Failed to open the file.")
    exit()

tree = file.Get("clustTree")
branch = tree.GetBranch("clust")
leaf = branch.GetLeaf("charge")
h = ROOT.TH1F("histogram", "Charge deposited on clusters", 100, 0, 300e3)

# Loop over the entries in the tree and fill the histogram
for entry in range(tree.GetEntries()):
    tree.GetEntry(entry)
    value = leaf.GetValue()
    h.Fill(value)

print("Making canvas...")

# Create canvas, draw histogram
canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
h.Draw()
canvas.Update()

# Make vavilov custom function
def my_vavilov(x, par):
    beta = par[0]
    kappa = par[1]
    landau = ROOT.TMath.Landau((x[0] - beta) / kappa) / kappa
    return landau * ROOT.TMath.Vavilov(x[0], kappa, beta)

print("Making Vavilov function...")

# Create a function for the Vavilov distribution
vavilov_func = ROOT.TF1("vavilov_func", my_vavilov, 0, 300e3, 2)

mean_charge = h.GetMean()
std_charge = h.GetStdDev()

#vavilov_func.SetParameters(mean_charge, std_charge)
vavilov_func.SetParameters(20000, 1)  # Set initial parameters

print("Fitting distribution...")

# Fit the distribution using the Vavilov function
h.Fit("vavilov_func", "N")
fit_function = vavilov_func

# Print fit results
beta = fit_function.GetParameter(0)
kappa = fit_function.GetParameter(1)
print("MPV:", beta)
print("Kappa:", kappa)

# Create a separate TF1 function for plotting the Vavilov fit
def fit_plot_function(x, par):
    return par[0] * my_vavilov(x, [par[1], par[2]])

# Set the parameters for the plot function with better initial values
fit_plot_func = ROOT.TF1("fit_plot_func", fit_plot_function, 0, 300e3, 3)
fit_plot_func.SetParameters(h.GetMaximum(), beta, kappa)

# Scale the plot function by the integral of the histogram
scaling_factor = h.Integral() / fit_plot_func.Integral(0, 300e3)

# Multiply the scaling factor to the existing parameters of the plot function
fit_plot_func.SetParameter(0, fit_plot_func.GetParameter(0) * scaling_factor)

# Draw
fit_plot_func.SetLineColor(ROOT.kRed)
fit_plot_func.SetLineWidth(2)
fit_plot_func.Draw("same")  # Use "same" to overlay on the existing canvas

# Add a legend to the plot
legend = ROOT.TLegend(0.78, 0.6, 0.98, 0.75)
legend.AddEntry(h, "Charge Depo", "l")  # "l" for line
legend.AddEntry(fit_function, "Vavilov Fit", "l")
legend.Draw()

canvas.SaveAs("chargedepo_vavilov.png")
file.Close()
