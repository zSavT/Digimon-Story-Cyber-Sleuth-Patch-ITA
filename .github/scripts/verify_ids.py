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
                
                # Read original (ID and Speaker columns for all rows)
                orig_data = []
                try:
                    with open(orig_filepath, 'r', encoding='utf-8', newline='') as f:
                        reader = csv.reader(f)
                        try:
                            header = next(reader) # skip header
                        except StopIteration:
                            pass
                        
                        for line_num, row in enumerate(reader, start=2):
                            if row:
                                if len(row) < 2:
                                    print(f"WARNING: Row {line_num} in original file '{rel_path}' has fewer than 2 columns.")
                                    # Still append whatever is there to compare
                                    orig_data.append((row[0] if len(row) > 0 else '', '', line_num))
                                else:
                                    orig_data.append((row[0], row[1], line_num))
                except Exception as e:
                    print(f"ERROR: Failed to read original file {orig_filepath}: {e}")
                    failures += 1
                    continue
                
                # Read translated (ID and Speaker columns for all rows)
                tran_data = []
                try:
                    with open(tran_filepath, 'r', encoding='utf-8', newline='') as f:
                        reader = csv.reader(f)
                        try:
                            header = next(reader) # skip header
                        except StopIteration:
                            pass
                        
                        for line_num, row in enumerate(reader, start=2):
                            if row:
                                if len(row) < 2:
                                    tran_data.append((row[0] if len(row) > 0 else '', '', line_num))
                                else:
                                    tran_data.append((row[0], row[1], line_num))
                except Exception as e:
                    print(f"ERROR: Failed to read translated file {tran_filepath}: {e}")
                    failures += 1
                    continue
                
                # Compare row by row
                if len(orig_data) != len(tran_data):
                    print(f"MISMATCH in file '{rel_path}': Row count differs!")
                    print(f"  Original rows:   {len(orig_data)}")
                    print(f"  Translated rows: {len(tran_data)}")
                    failures += 1
                    continue
                
                file_has_error = False
                for i in range(len(orig_data)):
                    orig_id, orig_speaker, orig_line = orig_data[i]
                    tran_id, tran_speaker, tran_line = tran_data[i]
                    
                    if orig_id != tran_id or orig_speaker != tran_speaker:
                        print(f"MISMATCH in file '{rel_path}' at row index {i} (Original line {orig_line}, Translated line {tran_line}):")
                        print(f"  Original:   ID={orig_id}, Speaker={orig_speaker}")
                        print(f"  Translated: ID={tran_id}, Speaker={tran_speaker}")
                        file_has_error = True
                        break
                        
                if file_has_error:
                    failures += 1
                
                checked_files += 1
                
    print(f"\nChecked {checked_files} files.")
    if failures > 0:
        print(f"Verification failed with {failures} error(s).")
        sys.exit(1)
    else:
        print("Verification completed successfully! All files are fully aligned.")
        sys.exit(0)

if __name__ == "__main__":
    verify_csv_alignment()
