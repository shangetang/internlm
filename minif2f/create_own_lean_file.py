import json

def write_lean_file(jsonl_path, lean_output_path, split = "test"):
    """
    Reads theorems from a .jsonl file and writes them as Lean theorems in a .lean file.
    
    Args:
    - jsonl_path: Path to the input .jsonl file.
    - lean_output_path: Path to the output .lean file.
    """
    with open(jsonl_path, 'r') as infile, open(lean_output_path, 'w') as outfile:
        
        header = '''import Mathlib

open BigOperators

open Real

open Nat

open Topology


'''
        
        # Write file header (optional imports)
        outfile.write(header)  # Add necessary imports
        
        theorem_counter = 1
        
        for line in infile:
            # Parse JSON object
            theorem_data = json.loads(line)
            
            # Extract details
            theorem_name = theorem_data.get("full_name", f"theorem_{theorem_counter}")
            theorem_statement = theorem_data.get("statement", "sorry") + " := by sorry"

            theorem_split = theorem_data.get("split","test")
            # theorem_proof = theorem_data.get("proof", "by sorry")
            
            # Format the theorem
            lean_theorem = theorem_statement + "\n\n"
            
            # Write to .lean file
            if theorem_split == split:
                outfile.write(lean_theorem)
            
            theorem_counter += 1

    print(f"Lean file successfully written to: {lean_output_path}")



write_lean_file("data/minif2f-lean4.7.0.jsonl", "data/Test.lean")

write_lean_file("data/minif2f-lean4.7.0.jsonl", "data/Valid.lean", split = "valid")