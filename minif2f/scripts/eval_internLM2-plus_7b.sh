MAX_ITERS=100
# NUM_SAMPLES=32
NUM_SAMPLES=1
TEMPERATURES="0.0"
TIMEOUT=600
# NUM_SHARDS=8
NUM_SHARDS=1
DATASET="minif2f-test"
DATA="data/minif2f.jsonl"

MODEL="internlm/internlm2-math-plus-7b"
NAME="internLM2-plus-7b"

OUTPUT_DIR="output/${NAME}_minif2f_test"
mkdir -p logs
# for SHARD in 0 1 2 3 4 5 6 7
for SHARD in 0
do
  CUDA_VISIBLE_DEVICES=${SHARD} python proofsearch_internLM2-plus.py --dataset-name ${DATASET} \
  --temperatures ${TEMPERATURES} --timeout ${TIMEOUT} --num-shards ${NUM_SHARDS} \
  --shard ${SHARD} --model-name ${MODEL} --max-iters ${MAX_ITERS} --dataset-path ${DATA} \
  --num-samples ${NUM_SAMPLES} --early-stop --output-dir ${OUTPUT_DIR} \
  &> logs/${NAME}_shard${SHARD}.out &
done