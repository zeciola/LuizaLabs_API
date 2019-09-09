from flask import url_for
from http import HTTPStatus

from ..flask_base_for_tests import BaseTestAPI


class TestProduct(BaseTestAPI):

    def test_product_register(self):
        self.create_client()
        token = self.create_token()

        payload = {
            "title": "Unit",
            "image": "s3/product/test.jpg",
            "amount": 10,
            "price": 100.50,
            "brand": "Product Test Inc.",
            "review_score": 10.0
        }
        response = self.app_client.post(url_for('product.product_register'), json=payload, headers=token)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        expect = {
            "title": "Unit",
            "image": "s3/product/test.jpg",
            "amount": 10,
            "id": 1,
            "price": 100.50,
            "brand": "Product Test Inc.",
            "review_score": 10.0
        }
        self.assertDictEqual(response.json, expect)

    def test_product_register_missing_fields(self):
        self.create_client()
        token = self.create_token()

        payload = {
            # "title": "Unit",
            "image": "s3/product/test.jpg",
            "amount": 10,
            "id": 1,
            # "price": 100.10,
            "brand": "UnitTest Python",
            # "review_score": 10.0
        }
        response = self.app_client.post(url_for('product.product_register'), json=payload, headers=token)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}
        self.assertDictEqual(response.json, expect)

    def test_product_show_by_title(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            "title": "Unit"
        }
        response = self.app_client.post(url_for('product.product_show_by_title'), json=payload, headers=token)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        expect = {
            'amount': 10,
            'brand': 'UnitTest Python',
            'id': 1,
            'image': 's3/product/test.jpg',
            'price': 100.0,
            'review_score': 10.0,
            'title': 'Unit'
        }
        self.assertDictEqual(response.json, expect)

    def test_product_show_by_title_not_send_title(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {}
        response = self.app_client.post(url_for('product.product_show_by_title'), json=payload, headers=token)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}
        self.assertDictEqual(response.json, expect)

    def test_product_show_by_id(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        response = self.app_client.get(url_for('product.product_show_by_id', identifier=1), headers=token)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        expect = {
            'amount': 10,
            'brand': 'UnitTest Python',
            'id': 1,
            'image': 's3/product/test.jpg',
            'price': 100.0,
            'review_score': 10.0,
            'title': 'Unit'
        }
        self.assertDictEqual(response.json, expect)

    def test_product_show_by_id_not_found_id(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        response = self.app_client.get(url_for('product.product_show_by_id', identifier=777), headers=token)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {"msg": "Product with id 777 not found"}
        self.assertDictEqual(response.json, expect)

    def test_product_change_by_title(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            "title_update": "Unit",
            "title": "Update_test",
            "image": "s3/product/update.jpg",
            "amount": 10,
            "price": 101.10,
            "brand": "Update Inc.",
            "review_score": 9.9
        }

        response = self.app_client.put(
            url_for('product.product_change_by_title'),
            json=payload, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {
            'amount': 10,
            'brand': 'Update Inc.',
            'id': 1,
            'image': 's3/product/update.jpg',
            'price': 101.1,
            'review_score': 9.9,
            'title': 'Update_test'
        }

        self.assertDictEqual(response.json, expect)

    def test_product_change_by_title_missing_fields(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            # "title_update": "Unit",
            "title": "Update_test",
            "image": "s3/product/update.jpg",
            # "amount": 10,
            "price": 101.10,
            # "brand": "Update Inc.",
            # "review_score": 9.9
        }

        response = self.app_client.put(
            url_for('product.product_change_by_title'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertDictEqual(response.json, expect)

        ...

    def test_product_delete_by_title(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            "title_delete": "Unit"
        }

        response = self.app_client.delete(
            url_for('product.product_delete_by_title'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {'msg': f'The product with title {payload["title_delete"]} is deleted'}

        self.assertDictEqual(response.json, expect)

    def test_product_delete_by_title_not_send_title(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            # "title_delete": "Unit"
        }

        response = self.app_client.delete(
            url_for('product.product_delete_by_title'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_register(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        response = self.app_client.post(
            url_for('product.favorite_product_register'),
            json=self.favorite_product,
            headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        expect = {
            'client_id': 1,
            'favorite': True,
            'id': 1,
            'product_id': 1
        }

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_register_missing_fields(self):
        self.create_client()
        self.create_product()
        token = self.create_token()

        payload = {
            # "favorite": True,
            "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.post(
            url_for('product.favorite_product_register'),
            json=payload,
            headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_register_validate_client_have_favorite_product(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()
        token = self.create_token()

        payload = {
            "favorite": True,
            "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.post(
            url_for('product.favorite_product_register'),
            json=payload,
            headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'The client already has this product on their favorites list'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_show_by_client_id(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        client_id = 1

        response = self.app_client.get(
            url_for(
                'product.favorite_product_show_by_client_id', identifier=client_id),
            headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        expect = [
            {'client_id': 1,
             'favorite': True,
             'id': 1,
             'product_id': 1}
        ]

        self.assertListEqual(response.json, expect)

    def test_favorite_product_show_by_client_id(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        client_id = 777

        response = self.app_client.get(
            url_for(
                'product.favorite_product_show_by_client_id', identifier=client_id),
            headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {
            'msg': f'client id {client_id} not found'
        }

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_change(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            "favorite_update": {
                "client_id": 1,
                "product_id": 1
            },
            "favorite": False,
            "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.put(
            url_for('product.favorite_product_change'),
            json=payload, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {
            'client_id': 1,
            'favorite': False,
            'id': 1,
            'product_id': 1
        }

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_change_validate_to_change(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        self.client = {
            "fullname": "Change",
            "email": "change@change.com.br",
            "password": "12345"
        }
        self.create_client(self.client)

        self.product = {
            "title": "Change product",
            "image": "s3/product/test.jpg",
            "amount": 10,
            "price": 100.0,
            "brand": "Change Prouct .Inc",
            "review_score": 10.0
        }
        self.create_product(self.product, self.create_token(self.client))

        self.favorite_product = {
            "favorite": True,
            "client_id": 2,
            "product_id": 2
        }
        self.create_favorite_product(self.favorite_product, self.create_token(self.client))

        token = self.create_token(self.client)

        payload = {
            "favorite_update": {
                "client_id": 1,
                "product_id": 1
            },
            "favorite": True,
            "client_id": 2,
            "product_id": 2
        }

        response = self.app_client.put(
            url_for('product.favorite_product_change'),
            json=payload, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {
            "error": "The client already has this product on their favorites list,"
            f" you can not change client_id: {payload['client_id']} and product_id: {payload['product_id']}"
            f" with favotite: {payload['favorite']}"
        }

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_change_missing_fields(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            # "favorite_update": {
            #     "client_id": 1,
            #     "product_id": 1
            # },
            "favorite": False,
            # "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.put(
            url_for('product.favorite_product_change'),
            json=payload, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_change_send_not_favorite_boolean(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            "favorite_update": {
                "client_id": 1,
                "product_id": 1
            },
            "favorite": 'False',
            "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.put(
            url_for('product.favorite_product_change'),
            json=payload, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Please send boolean type in favorite field'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_delete(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            "client_id": 1,
            "product_id": 1
        }

        response = self.app_client.delete(
            url_for(
                'product.favorite_product_delete'
            ),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {'msg': 'The client product favorite is deleted'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_delete_missing_fields(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            "client_id": 1,
            # "product_id": 1
        }

        response = self.app_client.delete(
            url_for(
                'product.favorite_product_delete'
            ),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertDictEqual(response.json, expect)

    def test_favorite_product_delete_not_found(self):
        self.create_client()
        self.create_product()
        self.create_favorite_product()

        token = self.create_token()

        payload = {
            "client_id": 777,
            "product_id": 777
        }

        response = self.app_client.delete(
            url_for(
                'product.favorite_product_delete'
            ),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {'msg': 'Favorite product not found'}

        self.assertDictEqual(response.json, expect)
