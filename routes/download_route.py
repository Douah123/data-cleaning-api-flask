#cette route permet de telecharger le fichier nettoyer en recuperant l'URL généré pae notre route 
# clean. Donc quand le User clique sur telecharger il recupere cette route

from flask import Blueprint, send_file, jsonify
from services.file_registry import FILE_REGISTRY
import os

download_bp = Blueprint("download", __name__)

@download_bp.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):

    if file_id not in FILE_REGISTRY:
        return jsonify({"error": "Fichier introuvable"}), 404

    path = FILE_REGISTRY[file_id]

    if not os.path.exists(path):
        return jsonify({"error": "Fichier supprimé"}), 404

    return send_file(path, as_attachment=True)
