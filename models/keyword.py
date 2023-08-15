from db import db

class KeywordModel(db.Model):
    __tablename__ = "Keywords"

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String, unique=True, nullable=False)
    document_type_id = db.Column(db.Integer, db.ForeignKey('DocumentTypes.id'))
