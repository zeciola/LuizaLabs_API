from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost:3306/luizalabs_flask_db'
app.config['JWT_SECRET_KEY'] = "Magalu gosta de programar no Luizalabs :)"
app.config['SECRET_KEY'] = "Magalu gosta de programar no Luizalabs :)"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app=app)
db = SQLAlchemy(app=app)
ma = Marshmallow(app=app)
migrate = Migrate(app=app, db=db)

from .endpoints.client import blueprint_client

app.register_blueprint(blueprint_client)

from .endpoints.product import blueprint_product

app.register_blueprint(blueprint_product)
