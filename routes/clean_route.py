from flask import Blueprint, request, jsonify, request, send_file
from services.data_cleaner import clean_data
from services.data_loader import load_file
from services.exportation import export_file

clean_bp = Blueprint("clean", __name__)

@clean_bp.route("/clean/report", methods = ["POST"])

def clean_file():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    file = request.files["file"]

    df, file_type = load_file(file)

    cleaned_df, report = clean_data(df)

    output_path = export_file(cleaned_df, file)

    return jsonify({
        "status": "success",
        "lignes_avant": len(df),
        "lignes_apres": len(cleaned_df),
        "rapport": report,
        "fichier_sortie": output_path
    })

@clean_bp.route("/clean/download", methods = ["POST"])

def clean_file_download():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    file = request.files["file"]

    df, file_type = load_file(file)

    cleaned_df, report = clean_data(df)

    output_path = export_file(cleaned_df, file)

    return send_file(
        output_path,
        as_attachment=True,
        download_name=file.filename 
    
    )
