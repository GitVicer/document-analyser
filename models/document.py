from db import db

class DocumentModel(db.Model):
    __tablename__ = "Documents"

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String, unique = True, nullable = False)
    client_id = db.Column(db.String, unique = True, nullable = False)
