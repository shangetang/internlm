import os
from lean_dojo import *
import json


# repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "d08b8ba")
os.environ['DISABLE_REMOTE_CACHE'] = 'true'

os.environ["VERBOSE"] = "1"

# repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "1ef4e4cac9dd370b7be6d648ce135a06aa6fce5f")
# repo = LeanGitRepo("/scratch/gpfs/st3812/datasets/lean-dojo-mew", "main")
repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/miniF2F")
# repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/miniF2F_old_version")
# repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/mathlib4")

traced_repo = trace(repo)


# file_path = "MiniF2F/correct_answers_CoT_Test.lean"

# # file_path = "MiniF2F/correct_answers_CoT_Test.lean"
# thm_name = "mathd_numbertheory_150"
# # file_path = "MiniF2F/Test.lean"

# traced_theorems = [
#     thm for thm in traced_repo.get_traced_theorems() if not thm.repo.is_lean4
# ]

# print(traced_theorems)


from pathlib import Path

target_file = Path("MiniF2F/correct_answers_CoT_Test.lean")

theorems_in_file = [
    thm for thm in traced_repo.get_traced_theorems()
    if thm.theorem.file_path == target_file
]

print(f"Found {len(theorems_in_file)} theorems in {target_file}:")
for thm in theorems_in_file:
    print("-", thm.theorem.full_name)
    for t in thm.get_traced_tactics():
        tactic_json = {
                                "tactic": t.tactic,
                                "annotated_tactic": t.get_annotated_tactic(),
                                "state_before": t.state_before,
                                "state_after": t.state_after,
                            }  
        print(tactic_json)

# print("Checking:", file_path in traced_repo.traced_files_graph.nodes)
# print("Graph keys:", list(traced_repo.traced_files_graph.nodes))
# print("Looking for:", file_path)
# if file_path not in traced_repo.traced_files_graph.nodes:
#     raise ValueError(f"File {file_path} is not in traced files.")
# # print("graph.nodes:",list(traced_repo.traced_files_graph.nodes))


# theorem = Theorem(traced_repo.repo, file_path, thm_name)

# print("theorem.repo:",theorem.repo)
# print("traced_repo.repo",traced_repo.repo)

# print("traced_repo.traced_files_graph.nodes[MiniF2F/correct_answers_CoT_Test.lean]",traced_repo.traced_files_graph.nodes["MiniF2F/correct_answers_CoT_Test.lean"])

# # print("theorem.file:", theorem.file)
# # print("type(theorem.file):", type(theorem.file))
# # print("repr(theorem.file):", repr(theorem.file))

# for path, data in traced_repo.traced_files_graph.nodes(data=True):
#     print("Path:", path)
#     print("Keys:", data.keys())
#     print("Traced file type:", type(data["traced_file"]))
#     # break

# thm = traced_repo.get_traced_theorem(theorem)



# print("hhh",flush= True)

# for t in thm.get_traced_tactics():
#   tactic_json = {
#                         "tactic": t.tactic,
#                         "annotated_tactic": t.get_annotated_tactic(),
#                         "state_before": t.state_before,
#                         "state_after": t.state_after,
#                     }  
#   print(tactic_json)







# # test check_proof
# with Dojo(theorem, timeout=300) as (dojo, init_state):
#   # result = dojo.run_tac(init_state, step3)
#   result = dojo.run_tac(init_state, step1_1)

# print(result)
# # result1 = check_proof(theorem, step1)

# # print("result1:",result1)

# # result2 = check_proof(theorem, step2)

# # print("result2:",result2)


