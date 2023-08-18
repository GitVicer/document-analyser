from db import db

class UploadedDocumentModel(db.Model):
    __tablename__ = "UploadedDocuments"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    identified_keywords = db.Column(db.Text)
    document_type_id = db.Column(db.Integer, db.ForeignKey('DocumentTypes.id'))
