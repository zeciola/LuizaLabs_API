from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app import app
from app import db

from app.models.client import Client
from app.models.product import Product, FavoriteProduct

Migrate(app=app, db=db)
JWTManager(app=app)

@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Client=Client,
        Product=Product,
        FavoriteProduct=FavoriteProduct
    )
