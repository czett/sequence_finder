# Protein Sequence Fetcher

Mini-Webtool zum automatischen Abrufen von UniProt-Aminosäuresequenzen für eine Liste von Protein-Namen  
(z. B. ASPH_HUMAN).

Hinweis: Nur für menschliche Proteine (Homo sapiens).

## Setup
``` bash
pip install flask requests
```

## Start
``` bash
python3 app.py
```

Browser: http://127.0.0.1:7300

## Nutzung
- Datei mit einem Protein-Namen pro Zeile hochladen
- Ergebnis-CSV liegt in assets/results/
