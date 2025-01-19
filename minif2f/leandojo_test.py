import os
from lean_dojo import *

os.environ['CACHE_DIR'] = '/scratch/gpfs/st6881/.cache/lean_dojo_jy'

os.environ['DISABLE_REMOTE_CACHE'] = 'false'



repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "d08b8ba")

file_path = "MiniF2F/Test.lean"
thm_name = "mathd_algebra_478"

theorem = Theorem(repo, file_path, thm_name)
print("thm success")


# with Dojo(theorem, timeout=60, additional_imports=["Mathlib.Tactic"]) as (dojo, init_state):
with Dojo(theorem, timeout=60, additional_imports=["Mathlib.Tactic"]) as (dojo, init_state):
    print("dojo success")

