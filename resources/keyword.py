from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import KeywordModel
from schemas import KeywordSchema

blp = Blueprint("Keyword", "Keyword")

# Keyword Endpoint
@blp.route("/keyword/<int:keyword_id>")
class Keyword(MethodView):

    @blp.response(200, KeywordSchema)
    def get(self, keyword_id):
        try:
            keyword = KeywordModel.query.get_or_404(keyword_id)
            return keyword

        except SQLAlchemyError:
            abort(500, message="Database error")

    @blp.response(204)
    def delete(self, keyword_id):
        try:
            keyword = KeywordModel.query.get_or_404(keyword_id)
            db.session.delete(keyword)
            db.session.commit()
            return "", 204

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

    @blp.arguments(KeywordSchema)
    @blp.response(200, KeywordSchema)
    def put(self, keyword_data, keyword_id):
        try:
            keyword = KeywordModel.query.get(keyword_id)

            if keyword:
                keyword.keyword = keyword_data["keyword"]
                keyword.document_type_id = keyword_data["document_type_id"]
            else:
                keyword = KeywordModel(id=keyword_id, **keyword_data)

            db.session.add(keyword)
            db.session.commit()
            return keyword

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")


# Keyword List Endpoint
@blp.route("/keyword")
class KeywordList(MethodView):

    @blp.response(200, KeywordSchema(many=True))
    def get(self):
        try:
            return KeywordModel.query.all()

        except SQLAlchemyError:
            abort(500, message="Database error")

    @blp.arguments(KeywordSchema)
    @blp.response(201, KeywordSchema)
    def post(self, keyword_data):
            keyword = KeywordModel(**keyword_data)
            db.session.add(keyword)
            db.session.commit()
            return keyword


    @blp.response(204)
    def delete(self):
        try:
            keywords = KeywordModel.query.all()
            for keyword in keywords:
                db.session.delete(keyword)
            db.session.commit()
            return "", 204

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")
