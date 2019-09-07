from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from http import HTTPStatus

from ..models.client import Client

blueprint_auth = Blueprint('auth', __name__, url_prefix='/api')


@blueprint_auth.route('/login', methods=['POST'])
def login() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':

            email = request.json['email']
            password = request.json['password']

            client = Client.query.filter_by(email=email).first()

            if client.verify_password(password=password):
                access_token = create_access_token(
                    identity=client.id, expires_delta=timedelta(minutes=10)
                )
                refresh_token = create_refresh_token(
                    identity=client.id
                )
                msg_token = dict(
                    access_token={'Authorization': f'Bearer {access_token}'},
                    refresh_token={'Authorization': f'Bearer {refresh_token}'},
                )

                return jsonify(dict(msg=msg_token)), HTTPStatus.OK
            else:
                return jsonify(
                    {'error': 'Invalid credentials, please insert a valid credential'}), HTTPStatus.BAD_REQUEST
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': e.args[0]}), HTTPStatus.BAD_REQUEST
