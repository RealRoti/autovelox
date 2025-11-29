import pandas as pd
import json
import re
import os

def parse_comuni_robusto(filepath):
    """
    Legge il file codici-comuni.txt cercando di gestire righe sminchiate.
    Logica: Cerca un codice catastale (lettera + 3 cifre).
    Se lo trova, assume che la riga successiva sia il nome e quella dopo la provincia.
    """
    comuni = {}
    
    if not os.path.exists(filepath):
        print(f"ERRORE: Il file '{filepath}' non esiste. Assicurati che sia nella stessa cartella.")
        return {}

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        # Pulisco le righe vuote e spazi extra
        lines = [line.strip() for line in f if line.strip()]

    # Regex per Codice Catastale (Es: A001, M200)
    # L'inizio riga ^ e fine riga $ assicurano che sia solo il codice
    code_pattern = re.compile(r'^[A-Z]\d{3}$')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Se la riga sembra un codice catastale
        if code_pattern.match(line):
            code = line
            
            # Controllo se c'è una riga dopo (il Nome)
            if i + 1 < len(lines):
                # Se la riga successiva è un altro codice, allora questo record è rotto, salto
                if code_pattern.match(lines[i+1]):
                    i += 1
                    continue
                
                name = lines[i+1]
                prov = "ND" # Default se manca la provincia
                
                next_idx_jump = 2 # Di base salto Codice e Nome
                
                # Controllo se c'è la terza riga (Provincia)
                if i + 2 < len(lines):
                    potential_prov = lines[i+2]
                    # La provincia è solitamente 2 lettere. E non deve essere un codice catastale.
                    if len(potential_prov) == 2 and not code_pattern.match(potential_prov):
                        prov = potential_prov
                        next_idx_jump = 3 # Salto anche la provincia
                
                comuni[code] = {
                    'nome': name,
                    'prov': prov,
                    'type': 'comune'
                }
                
                i += next_idx_jump
                continue
        
        i += 1
        
    return comuni

def main():
    # 1. Caricamento e Parsing Comuni
    print("--- Inizio Elaborazione ---")
    print("Lettura codici-comuni.txt in corso...")
    comuni_dict = parse_comuni_robusto('codici-comuni.txt')
    print(f" -> Trovati {len(comuni_dict)} comuni nel dizionario.")

    # 2. Caricamento CSV Autovelox
    print("Lettura csv in corso...")
    try:
        # on_bad_lines='skip' salta le righe del CSV irrimediabilmente rotte
        df = pd.read_csv('export-censimento-mit.csv', on_bad_lines='skip', dtype=str)
        
        # Pulisco i nomi delle colonne da spazi extra
        df.columns = df.columns.str.strip()
        
        # Riempio i codici mancanti per evitare crash
        df['Codice Catastale'] = df['Codice Catastale'].fillna('SCONOSCIUTO')
        
    except Exception as e:
        print(f"ERRORE critico nella lettura del CSV: {e}")
        return

    # Struttura dati finale
    output_data = {
        "metadata": {
            "totale_velox": len(df),
            "data_generazione": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
        },
        "comuni": [],
        "altri_enti": []
    }

    # Raggruppo i velox per codice catastale per efficienza
    grouped = df.groupby('Codice Catastale')
    codici_processati = set()

    # Funzione helper per pulire i campi
    def clean(val):
        if pd.isna(val) or val.lower() in ['nan', 'null', 'nd', '///']:
            return ""
        return str(val).strip()

    # 3. Associo Velox ai Comuni (Ciclo su TUTTI i comuni del txt)
    print("Associazione velox ai comuni...")
    for code, info in comuni_dict.items():
        codici_processati.add(code)
        lista_velox = []
        
        # Se questo comune ha velox nel CSV
        if code in grouped.groups:
            group = grouped.get_group(code)
            for _, row in group.iterrows():
                lista_velox.append({
                    "modello": clean(row.get('Modello')),
                    "tipo": clean(row.get('Tipo')),
                    "note": clean(row.get('Note')), # Contiene spesso l'indirizzo
                    "decreto": clean(row.get('Decreto'))
                })
        
        # Aggiungo alla lista (anche se lista_velox è vuota, come richiesto)
        output_data["comuni"].append({
            "codice": code,
            "nome": info['nome'],
            "prov": info['prov'],
            "has_velox": len(lista_velox) > 0,
            "count": len(lista_velox),
            "velox": lista_velox
        })

    # 4. Gestione "Altri Enti" (Polizia, Unioni, Codici strani presenti nel CSV ma non nel TXT)
    print("Elaborazione altri enti (Polizia, Unioni, ecc)...")
    for code, group in grouped:
        if code not in codici_processati:
            # Cerco di recuperare un nome dalla colonna "Denominazione"
            denominazione = "Ente Sconosciuto"
            if 'Denominazione' in group.columns:
                denominazioni_possibili = group['Denominazione'].dropna().unique()
                if len(denominazioni_possibili) > 0:
                    denominazione = clean(denominazioni_possibili[0])
            
            lista_velox = []
            for _, row in group.iterrows():
                lista_velox.append({
                    "modello": clean(row.get('Modello')),
                    "tipo": clean(row.get('Tipo')),
                    "note": clean(row.get('Note')),
                    "decreto": clean(row.get('Decreto'))
                })

            output_data["altri_enti"].append({
                "codice": code,
                "nome": denominazione,
                "count": len(lista_velox),
                "velox": lista_velox
            })

    # 5. Salvataggio JSON
    print("Salvataggio file 'velox.json'...")
    with open('velox.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("Fatto! Ora apri index.html per vedere i risultati.")

if __name__ == "__main__":
    main()