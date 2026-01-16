# Voici notre chef d'orchestre principal ce fichier contient notre route clean qui recoit un fichier
#avec les options ou pas le nettoie et l'exporte avec un identifiant unique, une URL de telechargement
# Et les statistiques avant et apres upload

from flask import Blueprint, request, jsonify, request
from services.data_cleaner import clean_data
from services.data_loader import load_file
from services.exportation import export_file
from services.pipeline.validators import valider_options
from services.pipeline.pipeline_runner import run_pipeline

clean_bp = Blueprint("clean", __name__)

@clean_bp.route("/clean", methods = ["POST"])

def clean_file():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nom de fichier invalide"}), 400

    normalize = request.form.get("normalize", "false").lower() == "true"

    method = request.form.get("method", "")

    method = method.lower() if method else None
    
    df, file_type = load_file(file)
    options = {
    "normalize": normalize,
    "method": method
        }
    try:
        options = valider_options(options)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    cleaned_df, stats_avant, stats_apres = run_pipeline(df, options)

    output_path = export_file(cleaned_df, file.filename)

    return jsonify({
        "statistiques_avant": stats_avant,
        "statistiques_apres": stats_apres,
        "fichier_sortie": output_path["output_filename"],
        "download_url":f"/download/{output_path['file_id']}"
        
    })


