from flask import Flask
from flask_smorest import Api
from resources.cch import blp as cchblueprint
from resources.document import blp as documentblueprint
from resources.auth import blp as authblueprint
from db import db 
from resources.auth import oauth
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

    db.init_app(app)
    api = Api(app)
    oauth.init_app(app)
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(cchblueprint)
    api.register_blueprint(documentblueprint)
    api.register_blueprint(authblueprint)

    return app    

def connect():
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)

    # create a cursor

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



