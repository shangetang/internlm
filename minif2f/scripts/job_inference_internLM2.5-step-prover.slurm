#!/bin/bash
#SBATCH --job-name=internlm_inference    # create a short name for your job
#SBATCH --output=/scratch/gpfs/st3812/logs/slurm-%A_%a.out
#SBATCH --error=/scratch/gpfs/st3812/logs/slurm-%A_%a.err
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=10
#SBATCH --mem=128g
#SBATCH --gres=gpu:2             # number of gpus per node
#SBATCH --time=23:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=all          # send email on job start, end and fault
#SBATCH --mail-user=st3812@princeton.edu
#SBATCH --partition=pli
#SBATCH --account=mathproof
# ------------- activate environment -----------------
# source /scratch/gpfs/yl7690/.bashrc
source /scratch/gpfs/st3812/.bashrc
conda activate internlm

cd /scratch/gpfs/st3812/InternLM-Math/minif2f


MAX_ITERS=4000
NUM_SAMPLES=16

# TEMPERATURES="0.0" # For pass@1 test, beam-search(t=0.0) is often the most performant choice. If pass@32 is wanted, change temperature to 0.7 or 0.9.

TEMPERATURES="1.0" # For pass@1 test, beam-search(t=0.0) is often the most performant choice. If pass@32 is wanted, change temperature to 0.7 or 0.9.


TIMEOUT=300
NUM_SHARDS=1
DATASET="minif2f-test"
DATA="data/minif2f-lean4.7.0.jsonl"

# MODEL="internlm/internlm2_5-step-prover"

MODEL="/scratch/gpfs/st3812/models/internlm2_5-step-prover"
NAME="internLM2_5-step-prover"

OUTPUT_DIR="output/${NAME}_minif2f_test"


#Shange leandojo fetch
# DATA_OUTPUT_PATH="data/minif2f_test_with_prompt.json"
DATA_OUTPUT_PATH="data/minif2f_compilation_results.json"
# mkdir -p logs
# for SHARD in 0
# do
#   python leandojo_fetch_state.py --dataset-name ${DATASET} \
#   --temperatures ${TEMPERATURES} --timeout ${TIMEOUT} --num-shards ${NUM_SHARDS} \
#   --shard ${SHARD} --model-name ${MODEL} --max-iters ${MAX_ITERS} --dataset-path ${DATA} \
#   --num-samples ${NUM_SAMPLES} --early-stop --output-dir ${OUTPUT_DIR} --output_path ${DATA_OUTPUT_PATH} \
#   &> logs/${NAME}_leandojo_fetch_shard${SHARD}.out &
# done



#Shange
# OUTPUT_PATH="output/test_results.json"
# OUTPUT_PATH="output/test_results_0_10.json"
OUTPUT_PATH="output/test_results_new_full.json"

mkdir -p logs
for SHARD in 0
do
  CUDA_VISIBLE_DEVICES=${SHARD} python wholeproof_internLM2.5-StepProver.py --dataset-name ${DATASET} \
  --temperatures ${TEMPERATURES} --timeout ${TIMEOUT} --num-shards ${NUM_SHARDS} \
  --shard ${SHARD} --model-name ${MODEL} --max-iters ${MAX_ITERS} --dataset-path ${DATA} \
  --num-samples ${NUM_SAMPLES} --early-stop --output-dir ${OUTPUT_DIR} --output_path ${OUTPUT_PATH} --input_path ${DATA_OUTPUT_PATH} \
  # &> logs/${NAME}_shard${SHARD}.out &
done