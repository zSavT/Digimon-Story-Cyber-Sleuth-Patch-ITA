import os
import csv
import re

def trova_testi_lunghi(cartella_iniziale):
    testi_lunghi = []

    # Itera su tutte le cartelle e sottocartelle
    for root, _, files in os.walk(cartella_iniziale):
        for nome_file in files:
            if nome_file.endswith(".csv"):
                percorso_file = os.path.join(root, nome_file)
                try:
                    if "tradotto" in root:
                        with open(percorso_file, 'r', encoding='utf-8') as file_csv:
                            # Leggi la prima riga per trovare l'intestazione
                            reader = csv.reader(file_csv, delimiter=',')
                            header = next(reader) 

                            try:
                                english_column_index = header.index("English")
                            except ValueError:
                                print(f"Colonna 'English' non trovata nel file: {nome_file}. Saltando.")
                                continue 

                            for riga in reader:
                                if len(riga) > english_column_index:
                                    testo = riga[english_column_index]
                                    # Rimuovi eventuali tag HTML (se presenti) e spazi extra
                                    testo_pulito = re.sub(r'<[^>]*>', '', testo).strip()
                                    
                                    # Conta il numero di caratteri di nuova riga
                                    numero_newline = testo_pulito.count('\n')
                                    if len(testo_pulito) > 60 and (numero_newline == 1 or numero_newline == 2):
                                        testi_lunghi.append(f"{root}\\{nome_file}:\n\t {testo_pulito}\n\n")
                    else:
                        print(f"{root} ignorato.")
                except UnicodeError:
                    print(f"Errore di codifica nel file: {nome_file}. Saltando.")
                except Exception as e:
                    print(f"Errore durante la lettura del file {nome_file}: {e}. Saltando.")

    return testi_lunghi

def scrivi_testi_su_file(testi, nome_file_output="Controllo.txt"):
    with open(nome_file_output, 'w', encoding='utf-8') as file_output:
        for testo in testi:
            file_output.write(testo + '\n')

if __name__ == "__main__":
    cartella_corrente = os.path.dirname(os.path.abspath(__file__))
    testi_trovati = trova_testi_lunghi(cartella_corrente)
    scrivi_testi_su_file(testi_trovati)
    print("Testi lunghi trovati e salvati in Controllo.txt")