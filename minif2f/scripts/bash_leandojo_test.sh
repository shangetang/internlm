
export DISABLE_REMOTE_CACHE='false'

export CACHE_DIR=/scratch/gpfs/st3812/.cache/lean_dojo_jy

export VERBOSE=1

mkdir -p logs
# for SHARD in 0 1 2 3 4 5 6 7

python leandojo_test.py \
&> logs/test_leandojo.out &
