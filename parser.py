# Della
import json
import os
from math import ceil
from tqdm import tqdm

def read_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file):
            # Parse each line as a JSON object
            json_obj = json.loads(line.strip())
            data.append(json_obj)
            # print (json_obj)
    return data

file_path = 'lwb_v1tov5_cot2.jsonl'
jsonl_data = read_jsonl(file_path) # lean4_code, problem_id, source, full_proof


# # save jsonl_data_new to a new file
# with open('lwb_v1tov5_cot2_small.jsonl', 'w', encoding='utf-8') as file:
#     for data in jsonl_data[:10]:
#         print(data)
#         json.dump(data, file, ensure_ascii=False)
#         file.write('\n')


# for item in jsonl_data[:10]:
#     print (item) 


def segment_lean_proof(proof_text):
    # Split the proof text into lines
    lines = proof_text.split('\n')
    
    # Find the end of the theorem block (first ":=" by)
    theorem_end = None
    for i, line in enumerate(lines):
        if ":= by" in line:
            theorem_end = i
            break
    if theorem_end is None:
        raise Exception(f"Theorem not found in: {proof_text}")
    
    # Split into theorem block and proof lines
    theorem_block = lines[:theorem_end+1]
    proof_lines = lines[theorem_end+1:]
    
    # Function to get indentation level
    def get_indent(line):
        return len(line) - len(line.lstrip())
    
    # Process proof lines into blocks based on indentation
    blocks = []
    
    current_block = []
    low_indent = None
    indent_increased = False
    
    for line in proof_lines:
        if line.strip() == "":
            current_block.append(line)
            continue
        indent = get_indent(line)
        # print(indent, current_indent, line)
        if low_indent is None:
            low_indent = indent
            current_block.append(line)
        else:
            if indent == low_indent and not indent_increased:
                current_block.append(line)
            elif indent > low_indent:
                indent_increased = True
                current_block.append(line)
            else: # indent < low_indent or (indent == low_indent and indent_increased)
                # End of current block, start new one
                low_indent = indent
                indent_increased = False
                blocks.append('\n'.join(current_block))
                current_block = [line]
    # Add the last block
    if current_block:
        blocks.append('\n'.join(current_block))
        # if current_block[-1].strip() == "":
        #     blocks[-1] += '\n'
        # else:
        #     blocks.append('\n'.join(current_block))
    
    # Combine theorem block with proof blocks
    segmented_blocks = ['\n'.join(theorem_block)] + blocks
    
    return segmented_blocks

# for data in jsonl_data[:10]:
#     segments = segment_lean_proof(data['lean4_code'])
#     print ('---------------------------')
#     print(data['problem_id'])
#     print ('---------------------------')
#     for segment in segments:
#         print(segment)
#         print ('---------------------------')
# exit(0)


jsonl_data_new = []

for data in tqdm(jsonl_data, total=len(jsonl_data)):
    try:
        segments = segment_lean_proof(data['lean4_code'])
    except Exception as e:
        print(f"Error in {data['problem_id']}: {e}")
        continue
    # segments_blocks = []
    # accum_segments = None
    if len(segments) == 0:
        print (f"No segments found in {data['problem_id']}")
    # for seg in segments:
    #     if accum_segments is None:
    #         accum_segments = seg
    #     else:
    #         accum_segments = '\n'.join([accum_segments, seg])
    #     segments_blocks.append(accum_segments)
    for i in range(len(segments)):
        data_new = {
            'name': f"{data['problem_id']}_{i}",
            'source': data['source'],
            'full_proof': data['full_proof'],
            'code': '\n'.join(segments[:i+1]),  # seg
            'next_block': segments[i+1] if i < len(segments) - 1 else "",
            'remaining_proof': '\n'.join(segments[i+1:]) if i < len(segments) - 1 else "",
        }
        # print (data_new['lean4_code'])
        jsonl_data_new.append(data_new)
print (f"Total number of segments: {len(jsonl_data_new)}")

save = True

# save jsonl_data_new to a new file
if save:
    split = 20
    step = ceil(len(jsonl_data_new) / split)
    # save jsonl_data_new to a new json file
    for i in tqdm(range(split), total=split):
        os.makedirs(f'lwb_v1tov5_cot2_segmented/{i}', exist_ok=True)
        json.dump(jsonl_data_new[i*step : (i+1)*step], open(f'lwb_v1tov5_cot2_segmented/{i}/to_inference_codes.json', 'w', encoding='utf-8'), ensure_ascii=False)

    # with open('lwb_v1tov5_cot2_segmented.jsonl', 'w', encoding='utf-8') as file:
    #     for data in tqdm(jsonl_data_new, total=len(jsonl_data_new)):
    #         json.dump(data, file, ensure_ascii=False)
    #         file.write('\n')

