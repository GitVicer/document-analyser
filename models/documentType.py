from db import db

class DocumentTypeModel(db.Model):
    __tablename__ = "DocumentTypes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    keywords = db.relationship('KeywordModel', backref='document_type', lazy='dynamic')
