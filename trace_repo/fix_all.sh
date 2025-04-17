#!/bin/bash

source ~/.bashrc

conda activate internlm

# Path to your project root
ROOT_DIR="/scratch/gpfs/st3812/datasets/mathlib4_training"
cd "$ROOT_DIR" || exit 1

# Activate your Lean environment if needed (e.g., source ~/.bashrc or conda)

# Loop through each .lean file under Training/
for file in Training/*.lean; do
    # Convert file path to module name: Training/Foo.lean → Training.Foo
    module_name="${file%.lean}"
    module_name="${module_name//\//.}"


    echo ">>> First pass: fix broken proofs in $module_name"
    python /scratch/gpfs/st3812/projects/step-prover/trace_repo/fix_wrong_proofs.py "$module_name"
    
    # echo ">>> Second pass: verify $module_name builds after fix"
    # python fix_wrong_proofs.py "$module_name"

    echo ">>> Second pass: verify $module_name builds after fix"
    if ! python /scratch/gpfs/st3812/projects/step-prover/trace_repo/fix_wrong_proofs.py "$module_name"; then
        echo "Still failing after fix: $module_name"
    fi
    
    echo ""
done

