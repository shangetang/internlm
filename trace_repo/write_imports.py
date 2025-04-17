import os

# Path to your repo (CHANGE this)
repo_root = "/scratch/gpfs/CHIJ/Shange/datasets/mathlib4_training/"
training_folder = os.path.join(repo_root, "Training")
training_lean = os.path.join(repo_root, "Training.lean")

# Get all .lean files in the Training/ folder
lean_files = [
    f for f in os.listdir(training_folder)
    if f.endswith(".lean")
]

# Sort for consistency
lean_files.sort()

# Generate import lines
import_lines = [
    f"import Training.{os.path.splitext(f)[0]}"
    for f in lean_files
]

# Overwrite Training.lean
with open(training_lean, "w") as f:
    f.write("\n".join(import_lines) + "\n")

print(f"Overwrote {training_lean} with {len(import_lines)} import statements.")