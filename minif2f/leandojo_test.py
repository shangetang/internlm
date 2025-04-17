import os
from lean_dojo import *


# repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "d08b8ba")
os.environ['DISABLE_REMOTE_CACHE'] = 'true'

# repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "1ef4e4cac9dd370b7be6d648ce135a06aa6fce5f")
# repo = LeanGitRepo("/scratch/gpfs/st3812/datasets/lean-dojo-mew", "main")
repo = LeanGitRepo.from_path("/scratch/gpfs/st3812/datasets/lean-dojo-mew")
file_path = "MiniF2F/Test.lean"
thm_name = "mathd_numbertheory_150"


theorem = Theorem(repo, file_path, thm_name)

print("hhh",flush= True)

# this is the correct proof
# step1 = ''' by
#   have h₁ : 6 ≤ n := by
#     -- We use contraposition to prove the statement.
#     contrapose! h₀
#     -- We check the values of N starting from 1.
#     interval_cases n <;> norm_num [Nat.Prime]
#   -- We have shown that 6 is the smallest N such that 7 + 30N is not a prime number.
#   exact h₁'''

step1 = '''have h₁ : 6 ≤ n := by contrapose! h₀; interval_cases n <;> norm_num [Nat.Prime]'''

step1_1 = '''  have h₁ : 6 ≤ n := by
    -- We use contraposition to prove the statement.
    contrapose! h₀
    -- We check the values of N starting from 1.
    interval_cases n <;> norm_num [Nat.Prime]'''
# step1_1 = ''' by
#   have h₁ 
#   : 6 ≤ n := by
#     -- We use contraposition to prove the statement.
#     contrapose! h₀
#     -- We check the values of N starting from 1.
#     interval_cases n <;> norm_num [Nat.Prime]
#   -- We have shown that 6 is the smallest N such that 7 + 30N is not a prime number.
#   exact h₁'''

step2 = "  sorry"

# step2 = "  hello world"
step3 = "omega"

# step4 = "have hhh : 1=1 := rfl"
step4 = '''have hhh : 1=1 := rfl'''

# test check_proof
with Dojo(theorem, timeout=300) as (dojo, init_state):
  # result = dojo.run_tac(init_state, step3)
  result = dojo.run_tac(init_state, step1_1)

print(result)
# result1 = check_proof(theorem, step1)

# print("result1:",result1)

# result2 = check_proof(theorem, step2)

# print("result2:",result2)


