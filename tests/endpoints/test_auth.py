from flask import url_for

from ..flask_base_for_tests import BaseTestAPI
from http import HTTPStatus


class TestAuth(BaseTestAPI):
    def test_create_token(self):

        self.create_client()
        self.client.pop('fullname')

        response = self.app_client.post(url_for('auth.login'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        expect = {
            "msg": {
                "access_token": {
                    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Njc3NDM2MTAsIm5iZiI6MTU2Nzc0MzYxMCwianRpIjoiNDNiNzQxYzAtMGJlOC00ZGQwLWE1NDYtMDRmMGZlOTNiOWI4IiwiZXhwIjoxNTY3NzQ0MjEwLCJpZGVudGl0eSI6MiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.spTGXsx6PZ8J3pw9RPNXexhdyRZaRjKjkuBc3QL8m0E"
                },
                "refresh_token": {
                    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Njc3NDM2MTAsIm5iZiI6MTU2Nzc0MzYxMCwianRpIjoiNjg2ZTE3MjEtZGY1Zi00ZWY3LWFiNjQtODViNTNlYTAwZTNlIiwiZXhwIjoxNTcwMzM1NjEwLCJpZGVudGl0eSI6MiwidHlwZSI6InJlZnJlc2gifQ.FSWLhcCPrYtdw3IjHKdboxtZ7BKjZq03pXaZt0vwUnA"
                }
            }
        }
        self.assertEqual(
            response.json['msg'].keys(), expect['msg'].keys()
        )
        self.assertEqual(
            response.json['msg']['access_token'].keys(),
            expect['msg']['access_token'].keys()
        )
        self.assertEqual(
            response.json['msg']['refresh_token'].keys(),
            expect['msg']['refresh_token'].keys()
        )

    def test_create_token_missing_fields(self):

        self.create_client()
        self.client.pop('fullname')
        self.client.pop('email')

        response = self.app_client.post(url_for('auth.login'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}
        self.assertEqual(response.json, expect)

        self.client.update({
            "email": "test@test.com.br",
            "password": "12345"
        })
        self.client.pop("password")

        response = self.app_client.post(url_for('auth.login'), json=self.client)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Payload is not valid'}
        self.assertEqual(response.json, expect)

    def test_create_toke_wrong_password(self):

        self.create_client()
        self.client.pop('fullname')
        self.client.update({'password': 'wrong'})

        response = self.app_client.post(url_for('auth.login'), json=self.client)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        expect = {'error': 'Invalid credentials, please insert a valid credential'}

        self.assertEqual(response.json, expect)
