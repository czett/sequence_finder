import requests, time, csv

csv_location = "assets/heme.csv"

with open(csv_location, "r") as file:
    proteins = [line.strip() for line in file.readlines()]

def name_to_uniprot_id(name: str) -> str:
    url = f"https://rest.uniprot.org/uniprotkb/search?query=gene_exact:{name}+AND+organism_id:9606&fields=accession&format=json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        if data.get("results"):
            return data["results"][0]["primaryAccession"]
    return None


def get_aa_sequences(protein_names: list) -> dict:
    aa_seq = {}

    with open("assets/new.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Gene", "Sequence", "Last 10", "Last 5", "Last 2", "Last 1"])

        for index, name in enumerate(protein_names):
            uniprot_id = name_to_uniprot_id(name)
            if not uniprot_id:
                aa_seq[name] = "UniProt ID not found"
                continue

            url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
            response = requests.get(url)
            if response.ok:
                content = response.text.split("\n")
                sequence = "".join(line for line in content if not line.startswith(">")).strip()

                aa_seq[name] = {
                    "sequence": sequence,
                    "last_10": sequence[-10:],
                    "last_5": sequence[-5:],
                    "last_2": sequence[-2:],
                    "last_1": sequence[-1:]
                }

                writer.writerow([name, sequence, sequence[-10:], sequence[-5:], sequence[-2:], sequence[-1:]])
                print(f"Protein no. {index + 1} saved.")
            else:
                aa_seq[name] = f"FASTA fetch error: {response.status_code}"

            time.sleep(0.5)

    return aa_seq

print(get_aa_sequences(proteins))