# cette route permet de telecharger le fichier nettoye depuis son file_id

import os

from flask import Blueprint, jsonify, send_file, session

from models.clean_history import CleanHistory
from services.auth import login_required
from services.file_registry import FILE_REGISTRY


download_bp = Blueprint("download", __name__)


@download_bp.route("/download/<file_id>", methods=["GET"])
@login_required
def download_file(file_id):
    history_entry = CleanHistory.query.filter_by(
        file_id=file_id, user_id=session["user_id"]
    ).first()
    if not history_entry:
        return jsonify({"error": "Fichier introuvable"}), 404

    path = history_entry.output_path
    FILE_REGISTRY[file_id] = path

    if not os.path.exists(path):
        return jsonify({"error": "Fichier supprime"}), 404

    return send_file(path, as_attachment=True)
