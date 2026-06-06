import os
import csv
import sys

def verify_csv_alignment():
    original_base = "File Originali"
    translated_base = "File Tradotti"
    
    if not os.path.exists(original_base):
        print(f"Error: Original base directory '{original_base}' does not exist.")
        sys.exit(1)
    if not os.path.exists(translated_base):
        print(f"Error: Translated base directory '{translated_base}' does not exist.")
        sys.exit(1)
        
    failures = 0
    checked_files = 0
    
    for root, _, files in os.walk(original_base):
        for filename in files:
            if filename.endswith(".csv"):
                orig_filepath = os.path.join(root, filename)
                
                # Get the relative path to locate the corresponding translated file
                rel_path = os.path.relpath(orig_filepath, original_base)
                tran_filepath = os.path.join(translated_base, rel_path)
                
                if not os.path.exists(tran_filepath):
                    print(f"ERROR: Corresponding translated file not found for: {rel_path}")
                    failures += 1
                    continue
                
                # Read original IDs (first two data rows)
                orig_ids = []
                try:
                    with open(orig_filepath, 'r', encoding='utf-8', newline='') as f:
                        reader = csv.reader(f)
                        try:
                            header = next(reader)
                        except StopIteration:
                            # Empty file
                            pass
                        
                        for _ in range(2):
                            try:
                                row = next(reader)
                                if row:
                                    orig_ids.append(row[0])
                            except StopIteration:
                                break
                except Exception as e:
                    print(f"ERROR: Failed to read original file {orig_filepath}: {e}")
                    failures += 1
                    continue
                
                # Read translated IDs (first two data rows)
                tran_ids = []
                try:
                    with open(tran_filepath, 'r', encoding='utf-8', newline='') as f:
                        reader = csv.reader(f)
                        try:
                            header = next(reader)
                        except StopIteration:
                            pass
                        
                        for _ in range(2):
                            try:
                                row = next(reader)
                                if row:
                                    tran_ids.append(row[0])
                            except StopIteration:
                                break
                except Exception as e:
                    print(f"ERROR: Failed to read translated file {tran_filepath}: {e}")
                    failures += 1
                    continue
                
                # Compare
                if orig_ids != tran_ids:
                    print(f"MISMATCH in file '{rel_path}':")
                    print(f"  Original first IDs:   {orig_ids}")
                    print(f"  Translated first IDs: {tran_ids}")
                    failures += 1
                
                checked_files += 1
                
    print(f"\nChecked {checked_files} files.")
    if failures > 0:
        print(f"Verification failed with {failures} error(s).")
        sys.exit(1)
    else:
        print("Verification completed successfully! All files are aligned.")
        sys.exit(0)

if __name__ == "__main__":
    verify_csv_alignment()
