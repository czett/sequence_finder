# OPP FILE OMG

import requests, time, csv

def convert_from_file(file_loc):
    with open(file_loc, "r") as file:
        proteins = [line.strip() for line in file.readlines()]
    return proteins

# def name_to_uniprot_id(name: str) -> str:
#     url = f"https://rest.uniprot.org/uniprotkb/search?query=gene_exact:{name}+AND+organism_id:9606&fields=accession&format=json"
#     response = requests.get(url)
#     if response.ok:
#         data = response.json()
#         if data.get("results"):
#             return data["results"][0]["primaryAccession"]
#     return None

def name_to_uniprot_id(name: str) -> str:
    # Nur die Accession (B7Z3V6) aus dem Entry Name (B7Z3V6_HUMAN) extrahieren
    accession = name.split('_')[0]
    
    # Jetzt direkt nach der Accession suchen (ist schneller und eindeutig)
    url = f"https://rest.uniprot.org/uniprotkb/search?query=accession:{accession}&fields=accession&format=json"
    
    response = requests.get(url)
    if response.ok:
        data = response.json()
        if data.get("results"):
            return data["results"][0]["primaryAccession"]
    return None

def get_aa_sequences(protein_names: list, new_file_name: str):
    with open(f"assets/results/{new_file_name}", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Gene", "Sequence", "Last 10", "Last 5", "Last 2", "Last 1"])

        for name in protein_names:
            print(f"bin bei {name}")
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
                    sequence[-10:],
                    sequence[-5:],
                    sequence[-2:],
                    sequence[-1:]
                ])
            else:
                writer.writerow([name, f"FASTA fetch error: {response.status_code}", "", "", "", ""])

            time.sleep(0.2)  # API freundlich

    # Kein yield mehr nötig hier, da synchron
    
print(name_to_uniprot_id("X5D2Y3_HUMAN"))