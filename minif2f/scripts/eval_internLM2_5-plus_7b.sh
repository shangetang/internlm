# MAX_ITERS means number of expansions
MAX_ITERS=1

# NUM_SAMPLES means how many leaf nodes at each expansion
# NUM_SAMPLES=32
NUM_SAMPLES=1


TEMPERATURES="0.0"

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

OUTPUT_DIR="output/${NAME}_minif2f_test_local"
mkdir -p logs
# for SHARD in 0 1 2 3 4 5 6 7
for SHARD in 0
do
  CUDA_VISIBLE_DEVICES=${SHARD} python proofsearch_internLM2.5-StepProver.py --dataset-name ${DATASET} \
  --temperatures ${TEMPERATURES} --timeout ${TIMEOUT} --num-shards ${NUM_SHARDS} \
  --shard ${SHARD} --model-name ${MODEL} --max-iters ${MAX_ITERS} --dataset-path ${DATA} \
  --num-samples ${NUM_SAMPLES} --early-stop --output-dir ${OUTPUT_DIR} \
  &> logs/${NAME}_local_shard${SHARD}.out &
done