from flask import Blueprint, request, jsonify
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.product import FavoriteProduct
from app.serializers.product import favorite_product_share_schema, favorites_products_share_schema
from ..models.product import Product
from ..serializers.product import product_share_schema

blueprint_product = Blueprint('product', __name__, url_prefix='/api')


@blueprint_product.route('/product/register', methods=['POST'])
@jwt_required
def product_register() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':
            title = request.json['title']
            image = request.json['image']
            amount = request.json['amount']
            price = request.json['price']
            brand = request.json['brand']
            review_score = request.json['review_score']

            product = Product(
                title=title,
                image=image,
                amount=amount,
                price=price,
                brand=brand,
                review_score=review_score
            )

            db.session.add(product)
            db.session.commit()

            result = product_share_schema.dump(
                Product.query.filter_by(title=title).first()
            )

            return result, HTTPStatus.CREATED

    except KeyError:
        return jsonify({'error': 'Payload is not valid'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/show/title', methods=['POST'])
@jwt_required
def product_show_by_title() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':
            result = product_share_schema.dump(
                Product.query.filter_by(title=request.json['title']).first()
            )

        return jsonify(result), HTTPStatus.FOUND
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/<identifier>', methods=['GET'])
@jwt_required
def product_show_by_id(identifier: int) -> (dict, HTTPStatus):
    if request.method == 'GET':
        result = product_share_schema.dump(
            Product.query.filter_by(id=identifier).first()
        )

    return jsonify(result), HTTPStatus.FOUND


@jwt_required
@blueprint_product.route('/product/change/title/', methods=['PUT'])
def product_change_by_title() -> (dict, HTTPStatus):
    try:
        if request.method == 'PUT':
            title = request.json['title_update']
            product_query = Product.query.filter_by(title=title).first()
            if product_share_schema.dump(product_query) == {}:
                return jsonify({'msg': 'Product not found'}), HTTPStatus.BAD_REQUEST

            product_query.title = request.json['title']
            product_query.image = request.json['image']
            product_query.amount = request.json['amount']
            product_query.price = request.json['price']
            product_query.brand = request.json['brand']
            product_query.review_score = request.json['review_score']

            db.session.commit()

            result = product_share_schema.dump(
                Product.query.filter_by(title=request.json['title']).first()
            )

            return jsonify(result), HTTPStatus.OK

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/delete/title/', methods=['DELETE'])
@jwt_required
def product_delete_by_title() -> (dict, HTTPStatus):
    try:
        if request.method == 'DELETE':
            title = request.json['title_delete']
            product_query = Product.query.filter_by(title=title).first()

            if product_share_schema.dump(product_query) == {}:
                return jsonify({'msg': 'Product not found'}), HTTPStatus.BAD_REQUEST

            db.session.delete(product_query)
            db.session.commit()

        return jsonify(
            f'The product with title {request.json["title_delete"]} is deleted'
        ), HTTPStatus.OK
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/favorite/register', methods=['POST'])
@jwt_required
def favorite_product_register() -> (dict, HTTPStatus):
    try:
        if request.method == 'POST':
            favorite = request.json['favorite']
            client_id = request.json['client_id']
            product_id = request.json['product_id']

            validate = favorite_product_share_schema.dump(
                FavoriteProduct.query.filter_by(
                    client_id=client_id,
                    product_id=product_id
                ).first()
            )
            if validate:
                return jsonify(
                    {'error': 'The client already has this product on their favorites list'}
                ), HTTPStatus.BAD_REQUEST

            favorite_prod = FavoriteProduct(
                favorite=favorite,
                client_id=client_id,
                product_id=product_id
            )
            db.session.add(favorite_prod)
            db.session.commit()

            result = favorite_product_share_schema.dump(
                FavoriteProduct.query.filter_by(
                    favorite=favorite,
                    client_id=client_id,
                    product_id=product_id
                ).first()
            )

            return result, HTTPStatus.CREATED

    except KeyError:
        return jsonify({'error': 'Payload is not valid'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/favorite/show/client/<identifier>', methods=['GET'])
@jwt_required
def favorite_product_show_by_client_id(identifier: int) -> (dict, HTTPStatus):
    try:
        if request.method == 'GET':
            result = favorites_products_share_schema.dump(
                FavoriteProduct.query.filter_by(client_id=identifier).all()
            )
            if not result:
                return jsonify({
                    'msg': f'client id {identifier} not found'
                }), HTTPStatus.BAD_REQUEST

            return jsonify(result), HTTPStatus.FOUND

    except KeyError:
        return jsonify({'error': 'Payload is not valid'})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/favorite/change/', methods=['PUT'])
@jwt_required
def favorite_product_change() -> (dict, HTTPStatus):
    try:
        if request.method == 'PUT':

            favorite_product = request.json['favorite_update']
            favorite_product_query = FavoriteProduct.query.filter_by(product_id=favorite_product['product_id'],
                                                                     client_id=favorite_product['client_id']).first()

            if not product_share_schema.dump(favorite_product_query):
                return jsonify({'msg': 'Favorite product not found'}), HTTPStatus.BAD_REQUEST

            if not isinstance(request.json['favorite'], bool):
                return jsonify({
                    'error': 'Please send boolean type in favorite field'
                }), HTTPStatus.BAD_REQUEST

            favorite_product_query.favorite = request.json['favorite']
            favorite_product_query.client_id = request.json['client_id']
            favorite_product_query.product_id = request.json['product_id']

            db.session.commit()

            result = favorite_product_share_schema.dump(
                FavoriteProduct.query.filter_by(
                    product_id=request.json['product_id'],
                    client_id=request.json['client_id']).first()
            )

            return jsonify(result), HTTPStatus.OK

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST


@blueprint_product.route('/product/favorite/delete/', methods=['DELETE'])
@jwt_required
def favorite_product_delete() -> (dict, HTTPStatus):
    try:
        if request.method == 'DELETE':

            favorite_product_query = FavoriteProduct.query.filter_by(product_id=request.json['product_id'],
                                                                     client_id=request.json['client_id']).first()

            if not favorite_product_share_schema.dump(favorite_product_query):
                return jsonify({'msg': 'Favorite product not found'}), HTTPStatus.BAD_REQUEST

            db.session.delete(favorite_product_query)
            db.session.commit()

        return jsonify(
            {'msg': 'The client product favorite is deleted'}
        ), HTTPStatus.OK

    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST
    except SQLAlchemyError as e:
        return jsonify({'error': str(e.__dict__.get('orig'))}), HTTPStatus.BAD_REQUEST
