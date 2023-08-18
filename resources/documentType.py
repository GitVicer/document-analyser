from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import DocumentTypeModel
from schemas import DocumentTypeSchema


blp = Blueprint("DocumentType", "DocumentType")

@blp.route("/document_type/<string:document_type_id>")

class DocumentType(MethodView):
    
    
    @blp.response(200, DocumentTypeSchema)
    def get(self, DocumentType_id):
        try:
            int(DocumentType_id)
        except ValueError:
            abort(400, message="Please enter an integer")    
        DocumentType = DocumentTypeModel.query.get_or_404(DocumentType_id)
        return DocumentType
    
    def delete(self, DocumentType_id):
        try:
            int(DocumentType_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        
        DocumentType = DocumentTypeModel.query.get_or_404(DocumentType_id)
        db.session.delete(DocumentType)
        db.session.commit()
        return {"message": "DocumentType deleted"}, 200
    
    
    @blp.response(200, DocumentTypeSchema)
    def put(self, DocumentType_data, DocumentType_id):
        try:
            int(DocumentType_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        DocumentType = DocumentTypeModel.query.get([DocumentType_id])

        if DocumentType:
            DocumentType.name = DocumentType_data["name"]
        else:
            DocumentType = DocumentTypeModel(id=DocumentType_id, **DocumentType_data)

        db.session.add(DocumentType)
        db.session.commit()

        return DocumentType

    
@blp.route("/DocumentType")

class DocumentType_List(MethodView):
    
    @blp.response(200, DocumentTypeSchema(many=True))
    #@login_required
    def get(self):
        print('-------------------------here')
        return DocumentTypeModel.query.all()
        
    @blp.arguments(DocumentTypeSchema)
    @blp.response(201, DocumentTypeSchema)
    def post(self, DocumentType_data):
        print(DocumentType_data)
        DocumentType = DocumentTypeModel(**DocumentType_data)
        db.session.add(DocumentType)
        db.session.commit()
        return DocumentType
     
    def delete(self):
        DocumentTypes = DocumentTypeModel.query.all()
        for DocumentType in DocumentTypes:
            db.session.delete(DocumentType) 
        db.session.commit()
        return {"message": "All DocumentTypes deleted"}, 200




    

