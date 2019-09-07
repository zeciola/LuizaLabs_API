from flask import url_for
from http import HTTPStatus

from ..flask_base_for_tests import BaseTestAPI


class TestClient(BaseTestAPI):

    def test_client_register(self):
        response = self.app_client.post(url_for('client.client_register'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        expect = {
            'email': 'test@test.com.br',
            'fullname': 'UnitTest',
            'id': 1,
            'password': 'pbkdf2:sha256:150000$MfDv92Af$d11b1b0f54b196d0b3ec83416bd5bf8def186e6cd2cecc8dd96fa1a0f663cb74'
        }

        self.assertEqual(response.json.keys(), expect.keys())
        self.assertEqual(response.json['email'], expect['email'])
        self.assertEqual(response.json['fullname'], expect['fullname'])
        self.assertEqual(response.json['id'], expect['id'])
        self.assertIn('pbkdf2:sha256:', response.json['password'])

    def test_client_register_missing_fields(self):
        # Miss email

        self.client.pop('email')

        response = self.app_client.post(url_for('client.client_register'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertEqual(response.json, expect)

        # Miss fullname

        self.client = {
            'email': 'test@test.com.br',
            'fullname': 'UnitTest',
            'password': 'pbkdf2:sha256:150000$MfDv92Af$d11b1b0f54b196d0b3ec83416bd5bf8def186e6cd2cecc8dd96fa1a0f663cb74'
        }

        self.client.pop('fullname')

        response = self.app_client.post(url_for('client.client_register'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(response.json, expect)

        # Miss password

        self.client = {
            'email': 'test@test.com.br',
            'fullname': 'UnitTest',
            'password': 'pbkdf2:sha256:150000$MfDv92Af$d11b1b0f54b196d0b3ec83416bd5bf8def186e6cd2cecc8dd96fa1a0f663cb74'
        }

        self.client.pop('password')

        response = self.app_client.post(url_for('client.client_register'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(response.json, expect)

    def test_client_register_create_two_clients_equals(self):
        self.create_client()

        response = self.app_client.post(url_for('client.client_register'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # import ipdb; ipdb.set_trace()

        expect = {'error': """(1062, "Duplicate entry \'test@test.com.br\' for key \'email\'")"""}

        self.assertEqual(response.json, expect)

    def test_client_show_by_email(self):
        self.create_client()

        token = self.create_token()

        response = self.app_client.post(
            url_for('client.client_show_by_email'),
            json={'email': self.client['email']}, headers=token
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        expect = {
            'email': 'test@test.com.br',
            'fullname': 'UnitTest',
            'id': 1,
            'password': 'pbkdf2:sha256:150000$CDKEviM2$7e72f71f5689f94c5f158b500d21d0000b2c00414a53650e9e4a473f0a11b2e8'
        }

        self.assertEqual(response.json.keys(), expect.keys())
        self.assertEqual(response.json['email'], expect['email'])
        self.assertEqual(response.json['fullname'], expect['fullname'])
        self.assertEqual(response.json['id'], expect['id'])
        self.assertIn('pbkdf2:sha256:', response.json['password'])

    def test_client_show_by_email_not_send_email(self):
        self.create_client()
        token = self.create_token()

        response = self.app_client.post(
            url_for('client.client_show_by_email'),
            json={'nope': 'nope'}, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}
        self.assertEqual(response.json, expect)

    def test_client_change_by_email(self):
        self.create_client()
        token = self.create_token()

        payload = {
            "email_update": "test@test.com.br",
            "fullname": "Update",
            "email": "update@update.com.br",
            "password": "12345"
        }

        response = self.app_client.put(
            url_for('client.client_change_by_email'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {
            'email': 'update@update.com.br',
            'fullname': 'Update',
            'id': 1,
            'password': 'pbkdf2:sha256:150000$CDKEviM2$7e72f71f5689f94c5f158b500d21d0000b2c00414a53650e9e4a473f0a11b2e8'
        }

        self.assertEqual(response.json.keys(), expect.keys())
        self.assertEqual(response.json['email'], expect['email'])
        self.assertEqual(response.json['fullname'], expect['fullname'])
        self.assertEqual(response.json['id'], expect['id'])
        self.assertIn('pbkdf2:sha256:', response.json['password'])

    def test_client_change_by_email_missing_fields(self):
        self.create_client()
        token = self.create_token()

        payload = {
            #"email_update": "test@test.com.br",
            "fullname": "Update",
            "email": "update@update.com.br",
            "password": "12345"
        }

        response = self.app_client.put(
            url_for('client.client_change_by_email'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}

        self.assertEqual(response.json, expect)

        payload = {
            "email_update": "test@test.com.br",
            #"fullname": "Update",
            #"email": "update@update.com.br",
            #"password": "12345"
        }

        response = self.app_client.put(
            url_for('client.client_change_by_email'),
            json=payload, headers=token
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.assertEqual(response.json, expect)
        ...