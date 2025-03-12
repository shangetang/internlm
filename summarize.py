# Tiger
import json
import os
from tqdm import tqdm

input_file = "/home/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented.jsonl"
compile_dir = "/home/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented"
output_file = "/home/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented_compiled.json"


files = []
for root, dirs, filenames in os.walk(compile_dir):
    for filename in filenames:
        if filename.startswith('code_compilation'):
        # if filename.startswith('to_inference'):
            files.append(os.path.join(root, filename))
print (files)

data = []
for file in tqdm(files, total=len(files), desc='Reading files'):
    with open(file, 'r') as f:
        data.extend(json.load(f))
print ('compilation results: ', len(data))

proof_list = []
with open(input_file, 'r', encoding='utf-8') as file:
    for line in tqdm(file):
        # Parse each line as a JSON object
        json_obj = json.loads(line.strip())
        proof_list.append(json_obj)
print ('proof: ', len(proof_list))

assert len(data) == len(proof_list)

data_dict = {item["name"]: item for item in data}
merged_list = []
for proof in tqdm(proof_list, total=len(proof_list), desc='Merging'):
    proof_name = proof.get("name")
    if proof_name in data_dict:
        merged_dict = {**proof, **data_dict[proof_name]}
        merged_list.append(merged_dict)
    else:
        raise Exception(f"Proof {proof_name} not found in the compilation results")

print ('saving...')
json.dump(merged_list, open(output_file, 'w', encoding='utf-8'), ensure_ascii=False)


