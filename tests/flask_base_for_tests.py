from unittest import TestCase

from flask import url_for
from json import loads

from app import app


class BaseTestAPI(TestCase):

    def setUp(self):
        self.app = app
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
            "price": 100.10,
            "brand": "UnitTest Python",
            "review_score": 10.0
        }

        self.favorite_product = {
            "favorite": True,
            "client_id": 1,
            "product_id": 1
        }

    def tearDown(self):
        self.app.db.drop_all()

    def create_client(self):
        self.app_client.post(url_for('client.client_register'), json=self.client)

    def create_product(self):
        self.app_client.post(url_for('product.product_register'), json=self.product)

    def create_favorite_product(self):
        self.app_client.post(url_for('product.favorite_product_register'), json=self.favorite_product)

    def create_token(self):
        self.client.pop("fullname")

        login_token = self.app_client.post(url_for('auth.login'), json=self.client)

        return loads(login_token.data.decode())["acess_token"]
