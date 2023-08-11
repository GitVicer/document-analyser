from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import DocumentModel
from schemas import DocumentSchema
from resources.auth import login_required

blp = Blueprint("Documents", "documents")

@blp.route("/document/<string:document_id>")

class Document(MethodView):
    
    @blp.response(200, DocumentSchema)
    def get(self, document_id):
        try:
            int(document_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        document = DocumentModel.query.get_or_404(document_id)
        return document
    
    def delete(self, document_id):
        try:
            int(document_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        document = DocumentModel.query.get_or_404(document_id)
        db.session.delete(document)
        db.session.commit()
        return {"message": "document deleted"}
    
    @blp.response(200, DocumentSchema)
    def put(self, document_data, document_id):
        document = DocumentModel.query.get(document_id)

        if document:
            document.name = document_data["name"]
        else:
            document = DocumentModel(id=document_id, **document_data)

        db.session.add(document)
        db.session.commit()

        return document

@blp.route("/document")
class DocumentList(MethodView):
    
    
    @blp.response(200, DocumentSchema(many=True))
    @login_required
    def get(self):
        return DocumentModel.query.all()
    
    
    @blp.arguments(DocumentSchema)
    @blp.response(201, DocumentSchema)
    def post(self, document_data):
        document = DocumentModel(**document_data)

        try:
            db.session.add(document)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Name exists")    
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the document.")

        return document
    
    def delete(self):
        documents = DocumentModel.query.all()
        for document in documents:
            db.session.delete(document)
        db.session.commit()
        return {"message": "All documents deleted"}, 200

    
    