from flask import Flask, render_template, request, redirect, url_for
import os
import old_logic

app = Flask(__name__)
UPLOAD_DIR = "assets/uploaded"
RESULTS_DIR = "assets/results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["protein-csv"]
    original_filename = f.filename
    save_path = os.path.join(UPLOAD_DIR, original_filename)
    f.save(save_path)

    output_filename = f"sq_{original_filename}"
    output_path = os.path.join(RESULTS_DIR, output_filename)

    # Hier synchron verarbeiten, blockierend
    proteins = old_logic.convert_from_file(save_path)
    old_logic.get_aa_sequences(proteins, output_filename)

    return f"Fertig! Ergebnis liegt in assets/results/{output_filename}"

if __name__ == "__main__":
    app.run(debug=True, port=7300)
