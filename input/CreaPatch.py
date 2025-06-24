import os
import shutil
import datetime

def collect_csv_with_structure(source_dirs, destination_dir="Patch", log_file="log.txt"):
    """
    Raccoglie i file CSV dalle directory sorgente, mantenendo la struttura delle cartelle originali.
    Copia sia i CSV trovati nella cartella 'tradotto' sia quelli trovati
    allo stesso livello della cartella 'tradotto' (se 'tradotto' non esiste).
    Crea un file di log per registrare le operazioni e le assenze.
    """

    os.makedirs(destination_dir, exist_ok=True)
    print(f"La cartella di destinazione '{destination_dir}' è stata creata (o esiste già).")

    found_files_count = 0
    
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"--- Log delle operazioni CSV - {datetime.datetime.now()} ---\n\n")
        print(f"Il file di log '{log_file}' è stato creato/azzerato.")

        for base_dir in source_dirs:
            if not os.path.isdir(base_dir):
                print(f"Attenzione: La directory sorgente '{base_dir}' non esiste. Saltata.")
                log.write(f"ATTENZIONE: La directory sorgente '{base_dir}' non esiste o non è accessibile.\n")
                continue

            print(f"\nScansione della directory: {base_dir}...")
            for entry_name in os.listdir(base_dir):
                current_parent_path = os.path.join(base_dir, entry_name)
                
                if not os.path.isdir(current_parent_path):
                    continue # Ignora i file a questo livello

                tradotto_path = os.path.join(current_parent_path, "tradotto")
                # Costruisci il percorso di destinazione per mantenere la struttura
                relative_path_from_base = os.path.relpath(current_parent_path, base_dir)
                target_sub_dir = os.path.join(destination_dir, base_dir, relative_path_from_base)
                os.makedirs(target_sub_dir, exist_ok=True) # Crea le cartelle di destinazione
                copied_from_tradotto = False 
                
                if os.path.isdir(tradotto_path):
                    # Caso 1: La cartella 'tradotto' è presente
                    print(f"  Trovata cartella 'tradotto' in: {tradotto_path}")
                    log.write(f"TROVATA: Cartella 'tradotto' presente in '{current_parent_path}'.\n")

                    for filename in os.listdir(tradotto_path):
                        if filename.endswith(".csv"):
                            source_file_path = os.path.join(tradotto_path, filename)
                            destination_file_path = os.path.join(target_sub_dir, filename)
                            try_copy_file(source_file_path, destination_file_path, log)
                            found_files_count += 1
                            copied_from_tradotto = True
                    
                    if not copied_from_tradotto:
                         print(f"    Nessun file CSV trovato in '{tradotto_path}'.")
                         log.write(f"    ATTENZIONE: Trovata cartella 'tradotto' ma nessun file CSV al suo interno in '{tradotto_path}'.\n")

                else:
                    # Caso 2: La cartella 'tradotto' NON è presente
                    print(f"  NON TROVATA: Cartella 'tradotto' non presente in '{current_parent_path}'.")
                    log.write(f"NON TROVATA: Cartella 'tradotto' non presente in '{current_parent_path}'. Cerco CSV allo stesso livello.\n")

                    # Cerca i file CSV direttamente nella cartella 'current_parent_path'
                    copied_from_parent = False
                    for filename in os.listdir(current_parent_path):
                        if filename.endswith(".csv"):
                            source_file_path = os.path.join(current_parent_path, filename)
                            destination_file_path = os.path.join(target_sub_dir, filename)
                            try_copy_file(source_file_path, destination_file_path, log)
                            found_files_count += 1
                            copied_from_parent = True
                    
                    if not copied_from_parent:
                        print(f"    Nessun file CSV trovato in '{current_parent_path}' (dopo l'assenza di 'tradotto').")
                        log.write(f"    ATTENZIONE: Cartella 'tradotto' non trovata e nessun file CSV presente in '{current_parent_path}'.\n")
                        
    # --- Riepilogo Finale ---
    if found_files_count > 0:
        print(f"\n--- Operazione completata! ---\nTotale {found_files_count} file CSV copiati nella cartella '{destination_dir}', mantenendo la struttura originale.")
        log.write(f"\n--- Operazione completata! ---\nTotale {found_files_count} file CSV copiati con successo in '{destination_dir}'.\n")
    else:
        print(f"\n--- Operazione completata! ---\nNessun file CSV trovato e copiato.")
        log.write(f"\n--- Operazione completata! ---\nNessun file CSV è stato copiato.\n")

def try_copy_file(source_path, destination_path, log_handle):
    """Funzione helper per provare a copiare un file e loggare il risultato."""
    try:
        shutil.copy2(source_path, destination_path)
        print(f"    Copiato '{os.path.basename(source_path)}' in '{destination_path}'")
        log_handle.write(f"    COPIATO: '{source_path}' in '{destination_path}'.\n")
        return True
    except Exception as e:
        print(f"    Errore durante la copia di '{os.path.basename(source_path)}': {e}")
        log_handle.write(f"    ERRORE COPIA: Impossibile copiare '{source_path}' in '{destination_path}' - {e}\n")
        return False

if __name__ == "__main__":
    source_directories_to_scan = ["text", "message"]
    collect_csv_with_structure(source_directories_to_scan, log_file="log.txt")