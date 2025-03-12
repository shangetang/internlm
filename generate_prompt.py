# Tiger
import json
from tqdm import tqdm
import numpy as np

input_file = "/home/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented_compiled.json"
output_file = "/home/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented_prompts.jsonl"

with open(input_file, 'r') as file:
    data = json.load(file)

# Count block numbers. Theorem names are not unique. Require that blocks for the same statement are consecutive.
block_num = []
for item in tqdm(data, total=len(data), desc='Counting block number'):
    last_number = int(item['name'].split('_')[-1])
    if last_number == 0:
        block_num.append(last_number)
    elif last_number > block_num[-1]:
        block_num[-1] = last_number

values = np.array(block_num) + 1
unique, counts = np.unique(values, return_counts=True)
value_counts = dict(zip(unique, counts))
print("Value counts:", value_counts)

err_num = {}
for item in tqdm(data, total=len(data), desc='Counting error number'):
    if "compilation_result" in item and "errors" in item["compilation_result"]:
        number = len(item["compilation_result"]["errors"])
        err_num[number] = err_num.get(number, 0) + 1
    else:
        err_num[-1] = err_num.get(-1, 0) + 1
        # print('errors not in key', item["compilation_result"])
print("Error number:", err_num)

# generate prompts
prompts = []
for item in tqdm(data, total=len(data), desc='Generating prompt'):
    if len(item['next_block']) == 0:
        continue
    code = item['code'].lstrip('\n')
    compile_result = item['compilation_result']
    next_block = item['next_block'] if item['next_block'] != item['remaining_proof'] else item['next_block'] + '\n-- <END>'
    full_proof = \
f"""Objective:
Generate the next step of a formal Lean 4 proof based on the provided problem statement, existing code, and compilation results. Follow the instructions precisely to ensure correctness and clarity.

Instructions:
- Shorten the Conclusion: Move objects from the conclusion into assumptions where possible to simplify the statement.
- Avoid Lean 3 Style: Use Lean 4 syntax exclusively; no deprecated Lean 3 constructs.
- No Undefined Objects: Do not introduce objects that require additional definitions.
- Step-by-Step Proof: The next step of the proof should be easy to verify in few lines. Begin the next step with the `have` tactic.
- No Sorry Statements: Do not use any `sorry` statements.

Output Format:
- Place the next step only between `-- <NEXT>` and `-- <NEXT/>`.
- Include inline comments explaining each logical move.
- Place `-- <END>` after the next step if the proof is complete.

Statement and Existing Code:
```lean
{code}
```

Compilation Result:
```compilation
{compile_result}
```

Next Step:
```lean
-- <NEXT>
{next_block}
-- <NEXT/>
```
"""
    prompt = {
        'name': item['name'],
        'full_proof': full_proof,
    }
    prompts.append(prompt)
    
with open(output_file, 'w') as file:
    for prompt in tqdm(prompts, total=len(prompts), desc='Saving prompts'):
        # print(prompt['full_proof'])
        file.write(json.dumps(prompt) + '\n')
