from flask import Blueprint, jsonify, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from app import db
from ..models.client import Client
from ..serializers.client import client_share_schema

blueprint_client = Blueprint('client', __name__, url_prefix='/api')


@blueprint_client.route('/client/register', methods=['POST'])
def client_register() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':
            fullname = request.json['fullname']
            email = request.json['email']
            password = request.json['password']

            client = Client(fullname=fullname, email=email, password=password)
            password = Client.hash_password(password=password)

            if client.verify_password(password=password):

                client.password = password

                db.session.add(client)
                db.session.commit()

                result = client_share_schema.dump(
                    Client.query.filter_by(email=email).first()
                )
                return result, HTTPStatus.CREATED
            else:
                return jsonify({'error': 'generate password fail'}), HTTPStatus.BAD_REQUEST

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST


@blueprint_client.route('/client/show/email', methods=['POST'])
@jwt_required
def client_show_by_email() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':
            result = client_share_schema.dump(
                Client.query.filter_by(email=request.json['email']).first()
            )

            return jsonify(result), HTTPStatus.FOUND

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST


@blueprint_client.route('/client/change/email/', methods=['PUT'])
@jwt_required
def client_change_by_email() -> (dict, HTTPStatus):
    try:
        if request.method == 'PUT':

            email = request.json['email_update']
            client_query = Client.query.filter_by(email=email).first()

            if not client_share_schema.dump(client_query):
                return jsonify({'msg': 'Client not found'}), HTTPStatus.NO_CONTENT

            client_query.fullname = request.json['fullname']
            client_query.email = request.json['email']
            client_query.password = request.json['password']

            db.session.commit()

            result = client_share_schema.dump(
                Client.query.filter_by(email=request.json['email']).first()
            )

            return jsonify(result), HTTPStatus.OK

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST


@blueprint_client.route('/client/delete/email/', methods=['DELETE'])
@jwt_required
def client_delete_by_email() -> (dict, HTTPStatus):
    try:
        if request.method == 'DELETE':

            email = request.json['email_delete']
            client_query = Client.query.filter_by(email=email).first()
            if not client_share_schema.dump(client_query):
                return jsonify({'msg': 'Client not found'}), HTTPStatus.OK

            db.session.delete(client_query)
            db.session.commit()

        return jsonify(
            {'msg': f'The client with email {request.json["email_delete"]} is deleted'}
        ), HTTPStatus.OK

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST
