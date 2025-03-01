import os
from lean_dojo import *


repo = LeanGitRepo("https://github.com/wzj423/lean-dojo-mew", "d08b8ba")

file_path = "MiniF2F/Test.lean"
thm_name = "mathd_numbertheory_150"

theorem = Theorem(repo, file_path, thm_name)


# this is the correct proof
step1 = ''' by
  have h₁ : 6 ≤ n := by
    -- We use contraposition to prove the statement.
    contrapose! h₀
    -- We check the values of N starting from 1.
    interval_cases n <;> norm_num [Nat.Prime]
  -- We have shown that 6 is the smallest N such that 7 + 30N is not a prime number.
  exact h₁'''

# step2 = "  sorry"

step2 = "  hello world"


# test check_proof


result1 = check_proof(theorem, step1)

print("result1:",result1)

# result2 = check_proof(theorem, step2)

# print("result2:",result2)


