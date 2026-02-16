from flask import Blueprint, jsonify, session

from models.clean_history import CleanHistory
from services.auth import login_required


history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
@login_required
def get_history():
    user_id = session["user_id"]
    history = (
        CleanHistory.query.filter_by(user_id=user_id)
        .order_by(CleanHistory.cleaned_at.desc())
        .all()
    )

    results = [entry.to_dict() for entry in history]

    return jsonify({"history": results}), 200
