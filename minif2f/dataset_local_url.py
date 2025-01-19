import json


input_path = "/scratch/gpfs/st3812/InternLM-Math/minif2f/data/minif2f.jsonl"

data_list = []

# local_url = "/scratch/gpfs/st3812/datasets/lean-dojo-mew"

# local_url = "/scratch/gpfs/st3812/datasets/miniF2F"

local_url = "https://github.com/shangetang/miniF2F"

# local_commit = "main"

local_commit = "fa58dc2d89d2292adbbe4c75c2b1d54f82ed1cdb"

with open (input_path,"r") as file:
    for line in file:
        data = json.loads(line)
        data["url"] = local_url
        data["commit"] = local_commit
        data_list.append(data)

print(data)

# output_path = "/scratch/gpfs/st3812/InternLM-Math/minif2f/data/minif2f-local.jsonl"

output_path = "/scratch/gpfs/st3812/InternLM-Math/minif2f/data/minif2f-shange.jsonl"

with open(output_path, 'w') as outfile:
    for data in data_list:
        json.dump(data, outfile)
        outfile.write('\n')


