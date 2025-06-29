import os
import csv

def count_csv_rows(root_dir, output_log_file='log_righe_csv.csv'):
    """
    Scansiona una directory radice e le sue sottocartelle per file CSV,
    conta le righe di ogni file e genera un file di log CSV.

    Args:
        root_dir (str): Il percorso della directory radice da cui iniziare la scansione.
        output_log_file (str): Il nome del file CSV di output per il log.
    """
    with open(output_log_file, 'w', newline='', encoding='utf-8') as log_file:
        log_writer = csv.writer(log_file, delimiter=';')
        log_writer.writerow(['NomeCartella', 'numerorighe']) # Intestazione del file di log

        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.csv'):
                    filepath = os.path.join(dirpath, filename)
                    row_count = 0
                    try:
                        with open(filepath, 'r', newline='', encoding='utf-8') as csv_file:
                            csv_reader = csv.reader(csv_file)
                            row_count = sum(1 for row in csv_reader)
                            # Se vuoi escludere l'intestazione, uncommenta la riga seguente:
                            # if row_count > 0:
                            #     row_count -= 1
                    except Exception as e:
                        print(f"Errore durante la lettura del file {filepath}: {e}")
                        continue

                    # Il "NomeCartella" sarà il percorso relativo del file CSV rispetto alla root_dir
                    relative_path = os.path.relpath(filepath, root_dir)
                    log_writer.writerow([relative_path, row_count])

    print(f"File di log generato con successo: {output_log_file}")

# --- Come usare il codice ---
if __name__ == "__main__":
    # Specifica la directory da cui vuoi iniziare la scansione
    # Sostituisci 'percorso/alla/tua/directory' con il percorso effettivo
    directory_da_scansionare = './' # Esempio: la directory corrente
    # directory_da_scansionare = 'C:/Users/TuUtente/Documenti/MieiDati' # Esempio su Windows
    # directory_da_scansionare = '/home/tuoutente/dati_csv' # Esempio su Linux/macOS

    count_csv_rows(directory_da_scansionare)