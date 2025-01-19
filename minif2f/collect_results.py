import os
import json
import pandas as pd

def merge_json_files(root_directory, output_file):
    merged_data = []

    # Traverse all subdirectories and files under the root directory
    for subdir, _, files in os.walk(root_directory):
        # Skip the root directory itself
        if subdir == root_directory:
            continue
        for file in files:
            if file.endswith('.json'):
                json_path = os.path.join(subdir, file)
                # Read and parse each JSON file
                try:
                    with open(json_path, 'r') as f:
                        data = json.load(f)
                        # Assuming JSON content is a list or a dictionary, adapt as needed
                        if isinstance(data, list):
                            merged_data.extend(data)
                        elif isinstance(data, dict):
                            merged_data.extend(data["results"])
                        else:
                            print(f"Skipping non-list/dict JSON content in {json_path}")
                except Exception as e:
                    print(f"Error reading {json_path}: {e}")


    modified_data=[{"name":idata["example"]["full_name"],"success":int(idata["success"])} for idata in merged_data]


    # Write the merged data into the output JSON file
    try:
        with open(output_file, 'w') as out_f:
            json.dump(modified_data, out_f, indent=4)
        print(f"Merged JSON data saved to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

# Example usage
root_directory = '/scratch/gpfs/st3812/InternLM-Math/minif2f/output/internLM2_5-step-prover_minif2f_test_local_offline_gpu_1*32*600'
output_file = f'{root_directory}/full_results.json'
merge_json_files(root_directory, output_file)







output_path = f'{root_directory}/summarize.json'


input_file= output_file
df = pd.read_json(input_file)



df_grp = df.groupby("name")["success"].sum() 

result = {
#   "total": len(df_grp),
  "total": 244,
  "success": sum(df_grp > 0),
#   "accuracy": F"{sum(df_grp > 0) / len(df_grp)  * 100:.2f}",
  "accuracy": F"{sum(df_grp > 0) / 244  * 100:.2f}",
}

with open(output_path, "w") as f:
    json.dump(result, f)

#
df_grp.reset_index()[["name", "success"]].to_csv(output_path.replace(".json", ".csv"), index=False, header=True, sep='\t', quoting=1, na_rep='Missing')
