#!/bin/bash
#SBATCH --job-name=internlm-1-32-20 # create a short name for your job
#SBATCH --output=/scratch/gpfs/st3812/logs/slurm-%A_%a.out
#SBATCH --error=/scratch/gpfs/st3812/logs/slurm-%A_%a.err
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=10        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=10G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1        # number of gpus per node
#SBATCH --constraint=gpu80
#SBATCH --time=4:50:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=FAIL         
#SBATCH --mail-user=st3812@princeton.edu
#SBATCH --array=0-11             # create a job array with 32 tasks (0 to 31)


source /scratch/gpfs/st3812/.bashrc


conda activate internlm

cd /scratch/gpfs/st3812/InternLM-Math/minif2f

# MAX_ITERS means number of expansions
MAX_ITERS=20

# NUM_SAMPLES means how many leaf nodes at each expansion
# NUM_SAMPLES=32
NUM_SAMPLES=1


TEMPERATURES="1.0"

TIMEOUT=600
# NUM_SHARDS=8
NUM_SHARDS=1
DATASET="minif2f-test"
DATA="data/minif2f-lean4.7.0-local.jsonl"
# DATA="data/minif2f-local2.jsonl"
# DATA="data/minif2f-lean4.7.0.jsonl"
# DATA="data/minif2f.jsonl"
# DATA="data/minif2f-shange.jsonl"

MODEL="/scratch/gpfs/st3812/models/internlm2_5-step-prover"
NAME="internLM2_5-step-prover"

# OUTPUT_DIR="output/${NAME}_minif2f_test_new2"


export DISABLE_REMOTE_CACHE='true'

# export CACHE_DIR=/scratch/gpfs/st3812/.cache/lean_dojo_jy

OUTPUT_DIR="output/${NAME}_minif2f_test_local_offline_gpu_1*${NUM_SAMPLES}*${MAX_ITERS}"
# mkdir -p logs
# for SHARD in 0 1 2 3 4 5 6 7
for SHARD in 0
do
  CUDA_VISIBLE_DEVICES=${SHARD} python proofsearch_internLM2.5-StepProver_local.py --dataset-name ${DATASET} \
  --temperatures ${TEMPERATURES} --timeout ${TIMEOUT} --num-shards ${NUM_SHARDS} \
  --shard ${SHARD} --model-name ${MODEL} --max-iters ${MAX_ITERS} --dataset-path ${DATA} \
  --num-samples ${NUM_SAMPLES} --early-stop --output-dir ${OUTPUT_DIR} \
  # &> logs/${NAME}_local_offline_shard${SHARD}.out &
done




