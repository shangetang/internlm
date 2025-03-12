# Della
from transformers import AutoTokenizer
from tqdm import tqdm
import json
import numpy as np
import pandas as pd

input_file = "/scratch/gpfs/jw6881/projects/lean/StepProver/lwb_v1tov5_cot2_segmented_prompts.jsonl"
model_name = "/scratch/gpfs/st3812/models/Goedel-Prover-SFT"

# Load tokenizer with fast version (critical for speed)
tokenizer = AutoTokenizer.from_pretrained(
    model_name, 
    use_fast=True,          # Enable fast tokenizer
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

# Optimized batch processing parameters
BATCH_SIZE = 4000  # Adjust based on available RAM (8000-10000 for large RAM)

# Read and process in batches
seq_length_list = []
with open(input_file, 'r') as f:
    batch = []
    for line in tqdm(f, desc="Processing lines"):
        try:
            data = json.loads(line.strip())
            if text := data.get("full_proof"):
                batch.append(text)
                
                # Process when batch is full
                if len(batch) >= BATCH_SIZE:
                    encoded = tokenizer.batch_encode_plus(
                        batch,
                        truncation=False,
                        padding=False,
                        return_attention_mask=False,
                        return_token_type_ids=False
                    )
                    seq_length_list.extend(map(len, encoded['input_ids']))
                    batch = []
        except Exception as e:
            print(f"Error processing line: {e}")

    # Process final batch
    if batch:
        encoded = tokenizer.batch_encode_plus(
            batch,
            truncation=False,
            padding=False,
            return_attention_mask=False,
            return_token_type_ids=False
        )
        seq_length_list.extend(map(len, encoded['input_ids']))

# Generate output (keep original format)
unique_lengths, counts = np.unique(seq_length_list, return_counts=True)
pd.DataFrame({
    "Sequence Length": unique_lengths,
    "Count": counts
}).to_csv("/scratch/gpfs/jw6881/projects/lean/StepProver/sequence_length_counts.csv", index=False)
