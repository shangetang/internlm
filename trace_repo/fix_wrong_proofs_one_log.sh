# # Also remove failed Training imports:
# python fix_wrong_proofs_one_log.py \
#  --log /scratch/gpfs/CHIJ/Shange/projects/trace_repo/trace_our_theorem_mathlib4_small_wrong.log \
#  --root-dir /scratch/gpfs/CHIJ/Shange/datasets/mathlib4_training_small \
#  > fix_wrong_proofs_one_log.log 2>&1


# Also remove failed Training imports:
python fix_wrong_proofs_one_log.py \
 --log /scratch/gpfs/CHIJ/Shange/projects/trace_repo/trace_our_theorem_mathlib4_small.log \
 --root-dir /scratch/gpfs/CHIJ/Shange/datasets/mathlib4_training_small \
 --remove-imports \
 > fix_wrong_proofs_one_log.log 2>&1