
import re
from pathlib import Path
import sys
import argparse

# # Set your root directory here (absolute or relative path)
# root_dir = Path("/scratch/gpfs/CHIJ/Shange/datasets/mathlib4_training_small")

import re
from pathlib import Path

def wrap_in_namespace(path: Path):
    """
    Wraps the content of the Lean file in a `namespace <filename>` block
    after the fixed preamble, and appends `end <filename>` at the end.
    """
    namespace_name = path.stem

    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Match preamble block
    preamble_pattern = re.compile(
        r"^import Mathlib\nimport Aesop\n\nset_option maxHeartbeats 0\n\nopen BigOperators Real Nat Topology Rat Polynomial Complex",
        re.DOTALL,
    )
    content = "".join(lines)
    match = preamble_pattern.match(content)

    if not match:
        print(f"⚠️  Preamble not found in {path.name}, skipping namespace insertion.")
        return

    preamble_len = len(match.group(0))
    before = content[:preamble_len]
    after = content[preamble_len:]

    # Skip if already namespaced
    if re.search(rf"\bnamespace {namespace_name}\b", after):
        print(f"⏭️  {path.name} already contains `namespace {namespace_name}`, skipping.")
        return

    # # Save backup before overwriting
    # backup_path = path.with_name(path.stem + "_original.lean")
    # if not backup_path.exists():
    #     with backup_path.open("w", encoding="utf-8") as backup_f:
    #         backup_f.write(content)
    #     print(f"🗂️  Saved original as {backup_path.name}")

    # Construct wrapped content
    wrapped = (
        before
        + f"\nnamespace {namespace_name}\n\n"
        + after.rstrip()
        + f"\n\nend {namespace_name}\n"
    )

    with path.open("w", encoding="utf-8") as f:
        f.write(wrapped)

    print(f"✅ Wrapped {path.name} in namespace `{namespace_name}`")


# Regex to extract errors from `lake build` output
error_pattern = re.compile(r"error: (.*\.lean):(\d+):(\d+):")

# Find the bounds of the Lean declaration (e.g. theorem, def) causing the error
def find_theorem_bounds(lines, error_line_idx):
    start = None
    for i in range(error_line_idx, -1, -1):
        if lines[i].strip().startswith(('theorem', 'lemma', 'def', 'example')):
            start = i
            break
    if start is None:
        return None, None

    end = len(lines) - 2
    for j in range(start + 1, len(lines)):
        if lines[j].strip().startswith(('theorem', 'lemma', 'def', 'example')):
            end = j - 1
            break

    return start, end

# Comment out the identified lines
def comment_out_lines(lines, spans_to_comment):
    new_lines = lines[:]
    for start, end in spans_to_comment:
        for i in range(start, end + 1):
            if not new_lines[i].strip().startswith('--'):
                new_lines[i] = '-- ' + new_lines[i]
    return new_lines

# Process the error log and collect spans to comment
def collect_error_spans(error_output: str, root_dir : Path):
    spans_by_file = {}
    for match in error_pattern.finditer(error_output):
        file_path_raw, line_str, _ = match.groups()
        line_num = int(line_str) - 1
        path = (root_dir / file_path_raw)
        if not path.exists():
            print(f" File not found: {path}")
            continue

        if path not in spans_by_file:
            with path.open('r', encoding='utf-8') as f:
                spans_by_file[path] = {
                    "lines": f.readlines(),
                    "spans": []
                }

        lines = spans_by_file[path]["lines"]
        start, end = find_theorem_bounds(lines, line_num)
        if start is not None and end is not None:
            print(f" Will comment out lines {start+1}-{end+1} in {path.name}")
            spans_by_file[path]["spans"].append((start, end))
        else:
            print(f" Could not find theorem bounds in {path.name} around line {line_num+1}")
    return spans_by_file

# Write the modified files
def apply_comments(spans_by_file):
    for path, info in spans_by_file.items():
        lines = info["lines"]
        spans = info["spans"]

        # Avoid overlapping or duplicate spans
        spans = sorted(set(spans), key=lambda x: x[0])
        commented_lines = comment_out_lines(lines, spans)

        # Save original backup
        original_backup = path.with_name(path.stem + "_original.lean")
        if not original_backup.exists():
            with path.open('r', encoding='utf-8') as orig_f:
                original_content = orig_f.read()
            with original_backup.open('w', encoding='utf-8') as backup_f:
                backup_f.write(original_content)
            print(f" Saved original as {original_backup.name}")
        else:
            print(f" Original backup {original_backup.name} already exists, skipping backup.")

        # # Write new content
        # # First wrap in namespace
        # wrapped_lines = wrap_in_namespace(path, commented_lines)

        # with path.open('w', encoding='utf-8') as f:
        #     f.writelines(wrapped_lines)

        # Write new content
        with path.open('w', encoding='utf-8') as f:
            f.writelines(commented_lines)


# # Regex to extract failed module builds
# failed_build_pattern = re.compile(r"✖ \[\d+/\d+\] Building (Training\.\S+)")

# # Remove failed imports from Training.lean
# def remove_failed_imports_from_training(error_output: str, training_file_path: Path):
#     failed_modules = failed_build_pattern.findall(error_output)
#     if not failed_modules:
#         print("No failed Training modules found.")
#         return

#     with training_file_path.open('r', encoding='utf-8') as f:
#         lines = f.readlines()

#     # Remove lines that import the failed modules
#     new_lines = [
#         line for line in lines
#         if not any(line.strip() == f"import {mod}" for mod in failed_modules)
#     ]

#     if len(lines) != len(new_lines):
#         # Save backup
#         backup_path = training_file_path.with_name(training_file_path.stem + "_original.lean")
#         if not backup_path.exists():
#             with training_file_path.open('r', encoding='utf-8') as orig_f:
#                 original_content = orig_f.read()
#             with backup_path.open('w', encoding='utf-8') as backup_f:
#                 backup_f.write(original_content)
#             print(f"Saved original as {backup_path.name}")

#         # Write modified file
#         with training_file_path.open('w', encoding='utf-8') as f:
#             f.writelines(new_lines)
#         print(f"Removed {len(lines) - len(new_lines)} failed imports from {training_file_path.name}")
#     else:
#         print("No import lines removed from Training.lean.")

# Regex to capture "Built Training.XYZ"
built_pattern = re.compile(r"Built (Training\.\S+)")

def keep_only_successful_imports(error_output: str, training_file_path: Path):
    # Extract successful builds from log
    successful_modules = set(built_pattern.findall(error_output))

    with training_file_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import Training."):
            module = stripped[len("import "):]
            if module in successful_modules:
                new_lines.append(line)
            else:
                print(f"Removing import: {module} (not successfully built)", flush=True)
        else:
            new_lines.append(line)

    # Write only if changes occurred
    if len(lines) != len(new_lines):
        # Backup original
        backup_path = training_file_path.with_name(training_file_path.stem + "_original.lean")
        if not backup_path.exists():
            with training_file_path.open('r', encoding='utf-8') as orig_f:
                original_content = orig_f.read()
            with backup_path.open('w', encoding='utf-8') as backup_f:
                backup_f.write(original_content)
            print(f"Saved original as {backup_path.name}")

        # Write filtered import lines
        with training_file_path.open('w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"Updated {training_file_path.name} to keep only successfully built imports.")
    else:
        print("No changes made to Training.lean.")

# # Main entry point
# if __name__ == "__main__":
#     log_path = "/scratch/gpfs/CHIJ/Shange/projects/trace_repo/trace_our_theorem_mathlib4_small.log"
#     if not Path(log_path).exists():
#         print(f" Cannot find build output log: {log_path}")
#     else:
#         with open(log_path, "r", encoding="utf-8") as f:
#             error_output = f.read()
#         spans_by_file = collect_error_spans(error_output)
#         apply_comments(spans_by_file)


#         training_file_path = root_dir / "Training.lean"
#         remove_failed_imports_from_training(error_output, training_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=str, required=True, help="Path to the lake build log file")
    parser.add_argument("--root-dir", type=str, required=True, help="Path to the root Lean source directory")
    parser.add_argument("--remove-imports", action="store_true", help="If set, remove failed imports from Training.lean")

    args = parser.parse_args()

    log_path = Path(args.log)
    root_dir = Path(args.root_dir)

    ## add namespace, should be done in preprocessing
    # files_folder = root_dir / "Training"

    for lean_file in files_folder.rglob("*.lean"):
        wrap_in_namespace(lean_file)

    if not log_path.exists():
        print(f"Cannot find build output log: {log_path}")
    else:
        with log_path.open("r", encoding="utf-8") as f:
            error_output = f.read()

        if args.remove_imports:
            training_file_path = root_dir / "Training.lean"
            # remove_failed_imports_from_training(error_output, training_file_path)
            keep_only_successful_imports(error_output, training_file_path)

        else:
            spans_by_file = collect_error_spans(error_output, root_dir)
            apply_comments(spans_by_file)

        # if args.remove_imports:
        #     training_file_path = root_dir / "Training.lean"
        #     remove_failed_imports_from_training(error_output, training_file_path)

    print("script ended")

