#!/bin/bash
#SBATCH --job-name=lean_fix_batch
#SBATCH --output=/scratch/gpfs/st3812/logs/slurm-%A_%a.out
#SBATCH --error=/scratch/gpfs/st3812/logs/slurm-%A_%a.err
#SBATCH --array=900-999
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6G # memory per cpu-core (4G is default)
#SBATCH --time=23:59:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=fail          
#SBATCH --mail-user=st3812@princeton.edu
#SBATCH --account=chij


source ~/.bashrc
conda activate internlm

# Path to your project root
ROOT_DIR="/scratch/gpfs/st3812/datasets/mathlib4_training"
cd "$ROOT_DIR" || exit 1

# Get the Lean module name from the array index
MODULE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" /scratch/gpfs/st3812/projects/step-prover/trace_repo/module_list.txt)

MAX_ATTEMPTS=10
ATTEMPT=1

echo ">>> Starting fix+verify loop for $MODULE"


while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo ">>> Attempt $ATTEMPT: Running fix_wrong_proofs.py for $MODULE"
    
    python /scratch/gpfs/st3812/projects/step-prover/trace_repo/fix_wrong_proofs.py "$MODULE"
    STATUS=$?

    if [ $STATUS -eq 0 ]; then
        echo "$MODULE successfully built on attempt $ATTEMPT"
        exit 0
    else
        echo "$MODULE failed on attempt $ATTEMPT, retrying..."
        ((ATTEMPT++))
    fi
done


# while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
#     echo ">>> Attempt $ATTEMPT for $MODULE"

#     python /scratch/gpfs/st3812/projects/step-prover/trace_repo/fix_wrong_proofs.py "$MODULE"

#     if lake build "$MODULE"; then
#         echo "$MODULE successfully built on attempt $ATTEMPT"
#         exit 0
#     fi

#     echo "Build failed for $MODULE on attempt $ATTEMPT"
#     ((ATTEMPT++))
# done

echo "$MODULE failed to build after $MAX_ATTEMPTS attempts"
exit 1