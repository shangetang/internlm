import os
from lean_dojo import *
import json


# repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "d08b8ba")
os.environ['DISABLE_REMOTE_CACHE'] = 'true'

repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/mathlib4")

traced_repo = trace(repo)
file_path = "MiniF2F/correct_answers_CoT_Test.lean"




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







# # file_path = "MiniF2F/correct_answers_CoT_Test.lean"
# thm_name = "mathd_numbertheory_150"
# # file_path = "MiniF2F/Test.lean"

# # print("graph.nodes:",list(traced_repo.traced_files_graph.nodes))


# theorem = Theorem(traced_repo.repo, file_path, thm_name)

# print("theorem.repo:",theorem.repo)
# print("traced_repo.repo",traced_repo.repo)

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


# # # test check_proof
# # with Dojo(theorem, timeout=300) as (dojo, init_state):
# #   # result = dojo.run_tac(init_state, step3)
# #   result = dojo.run_tac(init_state, step1_1)

# # print(result)
# # # result1 = check_proof(theorem, step1)

# # # print("result1:",result1)

# # # result2 = check_proof(theorem, step2)

# # # print("result2:",result2)


