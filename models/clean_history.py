from datetime import datetime

from services.db import db


class CleanHistory(db.Model):
    __tablename__ = "clean_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    file_id = db.Column(db.String(36), nullable=False, unique=True, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    output_filename = db.Column(db.String(255), nullable=False)
    output_path = db.Column(db.String(500), nullable=False)
    cleaned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "original_filename": self.original_filename,
            "cleaned_at": self.cleaned_at.isoformat() + "Z",
        }
