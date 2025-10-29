import requests, time, csv

def convert_from_file(file_loc):
    with open(file_loc, "r") as file:
        proteins = [line.strip() for line in file.readlines()]
    return proteins

def name_to_uniprot_id(name: str):
    """
    ULTRA-FINAL ROBUSTE LOGIK:
    Verwendet den vollständigen String ('name') als allgemeinen Query, 
    da dies Entry Names, Accessions und Gen-Namen am besten abdeckt.
    Die Beschränkung auf den Menschen (organism_id:9606) bleibt erhalten.
    """
    search_term = name
    
    # Der Query durchsucht alle wichtigen Felder (ID, Accession, Gene, Protein Name)
    # und ist auf Homo sapiens beschränkt.
    url = f"https://rest.uniprot.org/uniprotkb/search?query={search_term}+AND+organism_id:9606&fields=accession&format=json"
    
    response = requests.get(url)
    
    if response.ok:
        data = response.json()
        if data.get("results"):
            # Gibt die primäre Accession des ersten Suchergebnisses zurück
            return data["results"][0]["primaryAccession"]
            
    return None

def get_aa_sequences(protein_names: list, new_file_name: str):
    # DIESE FUNKTION BLEIBT UNVERÄNDERT, DA SIE KORREKT IST
    try:
        with open(f"assets/results/{new_file_name}", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Gene", "Sequence", "Last 10", "Last 5", "Last 2", "Last 1"])

            for name in protein_names:
                print(f"Bearbeite: {name}")
                
                uniprot_id = name_to_uniprot_id(name)
                
                if not uniprot_id:
                    writer.writerow([name, "UniProt ID not found", "", "", "", ""])
                    continue

                url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
                response = requests.get(url)
                
                if response.ok:
                    content = response.text.split("\n")
                    sequence = "".join(line for line in content if not line.startswith(">")).strip()

                    writer.writerow([
                        name,
                        sequence,
                        sequence[-10:] if len(sequence) >= 10 else sequence,
                        sequence[-5:] if len(sequence) >= 5 else sequence,
                        sequence[-2:] if len(sequence) >= 2 else sequence,
                        sequence[-1:] if len(sequence) >= 1 else sequence
                    ])
                else:
                    writer.writerow([name, f"FASTA fetch error: {response.status_code} ({uniprot_id})", "", "", "", ""])

                time.sleep(0.1)
    except FileNotFoundError:
        print("\nFEHLER: Das Verzeichnis 'assets/results/' existiert möglicherweise nicht.")
    except Exception as e:
        print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}")

# Testaufruf am Ende
print(name_to_uniprot_id("ASPH2_HUMAN"))