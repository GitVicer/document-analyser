from db import db

class CCHModel(db.Model):
    __tablename__ = "CCH"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    request = db.Column(db.String, unique = True, nullable = False)
    response = db.Column(db.String, unique = True, nullable = False)


