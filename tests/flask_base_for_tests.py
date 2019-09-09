from unittest import TestCase

from flask import url_for
from json import loads

from app import app, db

SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/luizalabs_test.db"
TESTING = True


class BaseTestAPI(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        app.config['JWT_SECRET_KEY'] = "Magalu gosta de programar no Luizalabs :)"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config['FLASK_DEBUG'] = TESTING
        app.config['FLASK_ENV'] = 'Development'
        app.config['FLASK_APP'] = 'app/main.py'
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        app.db = db

        return app

    def setUp(self):
        self.app = self.create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.app_client = self.app.test_client()
        self.app.db.create_all()

        self.client = {
            "fullname": "UnitTest",
            "email": "test@test.com.br",
            "password": "12345"
        }

        self.product = {
            "title": "Unit",
            "image": "s3/product/test.jpg",
            "amount": 10,
            "price": 100.0,
            "brand": "UnitTest Python",
            "review_score": 10.0
        }

        self.favorite_product = {
            "favorite": True,
            "client_id": 1,
            "product_id": 1
        }

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    # TODO: fazer a criação direto no banco com SQL_ALCHEMY em vez de utilizar os endpoints
    def create_client(self, *args,**kwargs):
        self.app_client.post(url_for('client.client_register'), json=self.client)

    def create_product(self, *args,**kwargs):
        self.app_client.post(url_for('product.product_register'), json=self.product, headers=self.create_token())

    def create_favorite_product(self, *args, **kwargs):
        self.app_client.post(
            url_for('product.favorite_product_register'),
            json=self.favorite_product,
            headers=self.create_token()
        )

    def create_token(self, *args, **kwargs):
        payload = {
            "email": self.client['email'],
            "password": self.client['password']
        }

        login_token = self.app_client.post(url_for('auth.login'), json=payload)

        return loads(login_token.data.decode())['msg']["access_token"]
