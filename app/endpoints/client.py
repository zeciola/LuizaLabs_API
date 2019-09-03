from flask import Blueprint, jsonify, request
from http import HTTPStatus

from app import db
from ..models.client import Client
from ..serializers.client import client_share_schema

blueprint_client = Blueprint('client', __name__, url_prefix='/api')


@blueprint_client.route('/client/register', methods=['POST'])
def client_register():
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

            return result, HTTPStatus.CREATED.value
        else:
            return jsonify({'error': 'generate password fail'}), HTTPStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST.value


@blueprint_client.route('/client/show/email', methods=['POST'])
def client_show_by_email():
    if request.method == 'POST':
        result = client_share_schema.dump(
            Client.query.filter_by(email=request.json['email']).first()
        )

    return jsonify(result), HTTPStatus.FOUND.value


@blueprint_client.route('/client/change/email/', methods=['PUT'])
def client_change_by_email():
    if request.method == 'PUT':

        email = request.json['email_update']

        client_query = Client.query.filter_by(email=email).first()

        if client_share_schema.dump(client_query) == {}:
            return jsonify({'msg': 'Client not found'}), HTTPStatus.NO_CONTENT.value

        client_query.fullname = request.json['fullname']
        client_query.email = request.json['email']
        client_query.password = request.json['password']

        db.session.commit()

        result = client_share_schema.dump(
            Client.query.filter_by(email=request.json['email']).first()
        )

    return jsonify(result), HTTPStatus.OK.value

@blueprint_client.route('/client/delete/email/', methods=['DELETE'])
def client_delete_by_email():
    if request.method == 'DELETE':

        email = request.json['email_delete' ]

        client_query = Client.query.filter_by(email=email).first()

        if client_share_schema.dump(client_query) == {}:
            return jsonify({'msg': 'Client not found'}), HTTPStatus.NO_CONTENT.value

        db.session.delete(client_query)

        db.session.commit()

    return jsonify(
        f'The client with email {request.json["email_delete"]} is deleted'
        ), HTTPStatus.OK.value

