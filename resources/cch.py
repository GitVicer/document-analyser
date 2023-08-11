from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import CCHModel
from schemas import CCHSchema
from resources.auth import login_required


blp = Blueprint("CCH", "cch")

@blp.route("/cch/<string:cch_id>")

class CCH(MethodView):
    
    
    @blp.response(200, CCHSchema)
    def get(self, cch_id):
        try:
            int(cch_id)
        except ValueError:
            abort(400, message="Please enter an integer")    
        cch = CCHModel.query.get_or_404(cch_id)
        return cch
    
    def delete(self, cch_id):
        try:
            int(cch_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        
        cch = CCHModel.query.get_or_404(cch_id)
        db.session.delete(cch)
        db.session.commit()
        return {"message": "cch deleted"}, 200
    
    
    @blp.response(200, CCHSchema)
    def put(self, cch_data, cch_id):
        try:
            int(cch_id)
        except ValueError:
            abort(400, message="Please enter an integer")
        cch = CCHModel.query.get([cch_id])

        if cch:
            cch.name = cch_data["name"]
        else:
            cch = CCHModel(id=cch_id, **cch_data)

        db.session.add(cch)
        db.session.commit()

        return cch

    
@blp.route("/cch")

class CCH_List(MethodView):
    
    @blp.response(200, CCHSchema(many=True))
    @login_required
    def get(self):
        return CCHModel.query.all()
        
    @blp.arguments(CCHSchema)
    @blp.response(201, CCHSchema)
    def post(self, cch_data):
        print(cch_data)
        cch = CCHModel(**cch_data)
        db.session.add(cch)
        db.session.commit()
        return cch
     
    def delete(self):
        cchs = CCHModel.query.all()
        for cch in cchs:
            db.session.delete(cch) 
        db.session.commit()
        return {"message": "All cchs deleted"}, 200




    

