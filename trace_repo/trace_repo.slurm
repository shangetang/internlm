#!/bin/bash
#SBATCH --job-name=trace_repo    # create a short name for your job
#SBATCH --output=/scratch/gpfs/CHIJ/Shange/logs/slurm-%A_%a.out
#SBATCH --error=/scratch/gpfs/CHIJ/Shange/logs/slurm-%A_%a.err
#SBATCH --exclude=tiger-g04c1n3,tiger-g04c1n8,tiger-g04c2n8,tiger-g04c4n5,tiger-g04c5n2,tiger-g04c1n3,tiger-g04c1n4,tiger-g04c1n5,tiger-g04c1n6,tiger-g04c1n8,tiger-g04c6n4,tiger-g04c5n5,tiger-g04c5n6
#SBATCH --nodes=1              # node count
#SBATCH --ntasks=1            # total number of tasks across all nodes
#SBATCH --ntasks-per-node=1      # one task per node
#SBATCH --cpus-per-task=32 # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G # memory per cpu-core (4G is default)
#SBATCH --time=23:59:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=FAIL          # send email on job start, end and fault
#SBATCH --mail-user=st3812@princeton.edu
#SBATCH --account=chij

source /scratch/gpfs/CHIJ/Shange/.bashrc


conda activate internlm

PROJ_DIR=/scratch/gpfs/CHIJ/Shange/projects/trace_repo


cd $PROJ_DIR



python trace_our_theorem_mathlib4_small.py

