import os
from lean_dojo import *
import json
from pathlib import Path

# need conda activate internlm


def trace_thm_in_file(traced_repo, file_name = "MiniF2F/correct_answers_Goedel_Test.lean"):
    target_file = Path(file_name)

    theorems_in_file = [
        thm for thm in traced_repo.get_traced_theorems()
        if thm.theorem.file_path == target_file
    ]

    output_list = []

    print(f"Found {len(theorems_in_file)} theorems in {target_file}:")
    for thm in theorems_in_file:
        print("-", thm.theorem.full_name, flush = True)
        thm_data = {
        "theorem_name": thm.theorem.full_name,
        "tactics": []
        }
        for t in thm.get_traced_tactics():
            thm_data["tactics"].append({
                                    "tactic": t.tactic,
                                    "annotated_tactic": t.get_annotated_tactic(),
                                    "state_before": t.state_before,
                                    "state_after": t.state_after,
                                })  
        output_list.append(thm_data)

    return output_list



# os.environ['DISABLE_REMOTE_CACHE'] = 'true'

# repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/mathlib4")



# traced_repo = trace(repo)
# file_path = "MiniF2F/correct_answers_Goedel_Test.lean"

# output_list = trace_thm_in_file(traced_repo, file_path)

# output_path = "/scratch/gpfs/st3812/aiformath/Deepseek/datasets/train_datasets/step_prover/Goedel_tactics_output.json"

# with open(output_path, "w") as f:
#     json.dump(output_list, f, indent=4)

# print(f"Save traced tactics to {output_path}", flush = True)



# Setup
os.environ['DISABLE_REMOTE_CACHE'] = 'true'
repo_root = "/scratch/gpfs/CHIJ/Shange/datasets/mathlib4_training"
repo = LeanGitRepo.from_path(repo_root)
traced_repo = trace(repo)

# Directory and pattern to search for
training_dir = Path(repo_root) / "Training"
lean_files = list(training_dir.glob("havecot_lwb_sonnet_*.lean")) + \
             list(training_dir.glob("dsstyle_lwb_sonnet_*.lean"))

# Output dir
output_base_dir = Path("/scratch/gpfs/CHIJ/Shange/Deepseek/datasets/training_datasets/step_prover/lwb_sonnet")

# Process each file
for lean_file in lean_files:
    relative_path = lean_file.relative_to(repo_root)
    output_list = trace_thm_in_file(traced_repo, str(relative_path))

    output_path = output_base_dir / f"{lean_file.stem}_tactics_output.json"
    with open(output_path, "w") as f:
        json.dump(output_list, f, indent=4)

    print(f"Saved traced tactics to {output_path}", flush=True)



