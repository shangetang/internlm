# create file for using eval in our scripts

import json

# input_path = "/scratch/gpfs/st3812/InternLM-Math/minif2f/output/test_results_new_full.json"
input_path = "/scratch/gpfs/st3812/InternLM-Math/minif2f/output/test_results_new.json"



with open(input_path, "r") as file:
    data_list = json.load(file)

to_inference_code_list = []

for data in data_list:
    name = data["name"]
    proof_list = data["proof"]
    header = data["header"]
    formal_statement = data["formal_statement"]

    for proof in proof_list:
        code = header + formal_statement + "  " +proof
        to_inference_code_list.append({"name": name, "code": code})  

# output_path = "/scratch/gpfs/st3812/aiformath/Deepseek/eval_results/minif2f/internlm2_5_step_prover/to_inference_codes.json" 
output_path = "/scratch/gpfs/st3812/aiformath/Deepseek/eval_results/minif2f/internlm2_5_step_prover2/to_inference_codes.json" 



with open(output_path, "w") as file:
    json.dump(to_inference_code_list, file, indent = 4)