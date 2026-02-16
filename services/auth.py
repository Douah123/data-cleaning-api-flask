from functools import wraps

from flask import jsonify, session


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentification requise"}), 401
        return view_func(*args, **kwargs)

    return wrapped
