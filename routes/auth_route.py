from flask import Blueprint, jsonify, request, session
import re
from werkzeug.security import check_password_hash, generate_password_hash

from models.user import User
from services.db import db


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
PASSWORD_PATTERN = re.compile(r"^[A-Z](?=.*\d)[A-Za-z\d]{7,}$")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not username or not email or not password:
        return jsonify({"error": "username, email et password sont obligatoires"}), 400
    if not PASSWORD_PATTERN.match(password):
        return jsonify({
            "error": (
                "Mot de passe invalide: minimum 8 caracteres, commencer par une "
                "majuscule et contenir des lettres et des chiffres"
            )
        }), 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        return jsonify({"error": "Utilisateur deja existant"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur cree", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email et password sont obligatoires"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Identifiants invalides"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Connexion reussie", "user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Deconnexion reussie"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Non connecte"}), 401

    user = User.query.get(user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"error": "Utilisateur introuvable"}), 404

    return jsonify({"user": user.to_dict()}), 200
