from flask import Flask
from flask_smorest import Api
from resources.documentType import blp as documenttypeblueprint
from resources.uploadDocument import blp as uploaddocumentblueprint
from resources.keyword import blp as keywordblueprint
from db import db 
import psycopg2
from config import config, database_uri_config


def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "Document porter API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri_config()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"   # To visualize the api go to http://127.0.0.1:5000/swagger-ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["JWT_SECRET_KEY"] = "12345"

    app.secret_key="my secret key"

    # db.init_app(app)
    api = Api(app)
    
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(documenttypeblueprint)
    api.register_blueprint(uploaddocumentblueprint)
    api.register_blueprint(keywordblueprint)

    return app    

def connect():
    try:
        connection = None
        params = config()
        print(params)
        connection = psycopg2.connect(**params)

    #create a cursor

        cur = connection.cursor()

        print ( "postgresql db version :")
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)    
    finally:
        if connection is not None:
            connection.close()
            print('database connection terminated')

connect()



