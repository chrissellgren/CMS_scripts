import ROOT
import sys
print(sys.argv[0],sys.argv[1])

# Open the ROOT file in read mode
file = ROOT.TFile.Open(sys.argv[1], "READ")

# Check if the file is successfully opened
if not file or file.IsZombie():
    print("Failed to open the file or the file is a zombie.")
    exit()

# Get the list of keys in the file
key_list = file.GetListOfKeys()

# Print the names of trees, branches, and leaves
print("Trees in the file:")
for key in key_list:
    obj = key.ReadObj()
    if isinstance(obj, ROOT.TTree):
        tree = file.Get(key.GetName())
        print(f"- Tree: {key.GetName()}")
        branch_list = tree.GetListOfBranches()
        for branch_key in branch_list:
            branch = branch_list.FindObject(branch_key)
            print(f"  - Branch: {branch.GetName()}")
            leaf_list = branch.GetListOfLeaves()
            for leaf_key in leaf_list:
                leaf = leaf_list.FindObject(leaf_key)
                print(f"    - Leaf: {leaf.GetName()}")

# Print the number of events in each tree
for key in key_list:
    obj = key.ReadObj()
    if isinstance(obj, ROOT.TTree):
        tree = file.Get(key.GetName())
        print(f"Number of events in tree '{key.GetName()}': {tree.GetEntries()}")

# Close the file
file.Close()
