import re
from pathlib import Path
import subprocess
import sys

# # Set your root directory here (absolute or relative path)
# root_dir = Path("/scratch/gpfs/st3812/datasets/mathlib4_training")

# # Regex to extract errors from `lake build` output
# error_pattern = re.compile(r"error: (.*\.lean):(\d+):(\d+):")

# # Find the bounds of the Lean declaration (e.g. theorem, def) causing the error
# def find_theorem_bounds(lines, error_line_idx):
#     start = None
#     for i in range(error_line_idx, -1, -1):
#         if lines[i].strip().startswith(('theorem', 'lemma', 'def', 'example')):
#             start = i
#             break
#     if start is None:
#         return None, None

#     # Look forward to find the next declaration
#     end = len(lines) - 1
#     for j in range(start + 1, len(lines)):
#         if lines[j].strip().startswith(('theorem', 'lemma', 'def', 'example')):
#             end = j - 1
#             break

#     return start, end

# # Comment out the identified lines
# def comment_out_lines(lines, start, end):
#     return ['-- ' + line if not line.strip().startswith('--') else line for line in lines[start:end+1]]

# # Process the error log and modify Lean files
# def process_errors(error_output: str):
#     file_to_lines = {}
#     for match in error_pattern.finditer(error_output):
#         file_path_raw, line_str, _ = match.groups()
#         line_num = int(line_str) - 1

#         # # Clean and resolve path
#         # relative_path = Path(file_path_raw).resolve().relative_to(root_dir)
#         # path = (root_dir / relative_path).resolve()
#         path = (root_dir / file_path_raw)
#         if not path.exists():
#             print(f" File not found: {path}")
#             continue

#         if path not in file_to_lines:
#             with path.open('r', encoding='utf-8') as f:
#                 file_to_lines[path] = f.readlines()

#         lines = file_to_lines[path]
#         start, end = find_theorem_bounds(lines, line_num)
#         if start is not None and end is not None:
#             print(f" Commenting out lines {start+1}-{end+1} in {path.name}")
#             lines[start:end+1] = comment_out_lines(lines, start, end)
#         else:
#             print(f" Could not find theorem bounds in {path.name} around line {line_num+1}")

#     # Write back the modified files, saving originals first
#     for path, lines in file_to_lines.items():
#         original_backup = path.with_name(path.stem + "_original.lean")
#         if not original_backup.exists():
#             with path.open('r', encoding='utf-8') as orig_f:
#                 original_content = orig_f.read()
#             with original_backup.open('w', encoding='utf-8') as backup_f:
#                 backup_f.write(original_content)
#             print(f" Saved original as {original_backup.name}")
#         else:
#             print(f" Original backup {original_backup.name} already exists, skipping backup.")

#         with path.open('w', encoding='utf-8') as f:
#             f.writelines(lines)

# # Main entry point: read from lake build output log
# if __name__ == "__main__":
#     log_path = "/scratch/gpfs/st3812/projects/step-prover/trace_repo/trace_our_theorem_mathlib4.log"
#     if not Path(log_path).exists():
#         print(f" Cannot find build output log: {log_path}")
#     else:
#         with open(log_path, "r", encoding="utf-8") as f:
#             error_output = f.read()
#         process_errors(error_output)



# Set your root directory
root_dir = Path("/scratch/gpfs/st3812/datasets/mathlib4_training")

# Regex to extract errors
error_pattern = re.compile(r"error: (.*\.lean):(\d+):(\d+):")

def find_theorem_bounds(lines, error_line_idx):
    start = None
    for i in range(error_line_idx, -1, -1):
        if lines[i].strip().startswith(('theorem', 'lemma', 'def', 'example')):
            start = i
            break
    if start is None:
        return None, None
    end = len(lines) - 1
    for j in range(start + 1, len(lines)):
        if lines[j].strip().startswith(('theorem', 'lemma', 'def', 'example')):
            end = j - 1
            break
    return start, end

def comment_out_lines(lines, start, end):
    return ['-- ' + line if not line.strip().startswith('--') else line for line in lines[start:end+1]]

def process_errors(error_output: str):
    file_to_lines = {}
    for match in error_pattern.finditer(error_output):
        file_path_raw, line_str, _ = match.groups()
        line_num = int(line_str) - 1
        path = (root_dir / file_path_raw).resolve()
        if not path.exists():
            print(f" File not found: {path}")
            continue
        if path not in file_to_lines:
            with path.open('r', encoding='utf-8') as f:
                file_to_lines[path] = f.readlines()
        lines = file_to_lines[path]
        start, end = find_theorem_bounds(lines, line_num)
        if start is not None and end is not None:
            print(f" Commenting out lines {start+1}-{end+1} in {path.name}")
            lines[start:end+1] = comment_out_lines(lines, start, end)
        else:
            print(f" Could not find theorem bounds in {path.name} around line {line_num+1}")

    for path, lines in file_to_lines.items():
        original_backup = path.with_name(path.stem + "_original.lean")
        if not original_backup.exists():
            with path.open('r', encoding='utf-8') as orig_f:
                original_content = orig_f.read()
            with original_backup.open('w', encoding='utf-8') as backup_f:
                backup_f.write(original_content)
            print(f" Saved original as {original_backup.name}")
        else:
            print(f" Original backup {original_backup.name} already exists.")
        with path.open('w', encoding='utf-8') as f:
            f.writelines(lines)


def main(module_name: str):
    print(f"Building {module_name}...", flush = True)
    result = subprocess.run(["lake", "build", module_name], capture_output=True, text=True)
    stderr = result.stderr
    stdout = result.stdout

    build_log = stderr + "\n" + stdout
    print(build_log, flush = True)
    if "error: " in build_log:
        process_errors(build_log)
        print(f"{module_name} has errors.", flush = True)
        sys.exit(1)
    else:
        print(f"{module_name} built successfully.", flush = True)
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_wrong_proofs.py <Module.Name.To.Build>")
        sys.exit(1)
    main(sys.argv[1])