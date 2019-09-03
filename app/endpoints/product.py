from flask import Blueprint, request, jsonify
from http import HTTPStatus

from app import db
from app.models.product import FavoriteProduct
from app.serializers.product import favorite_product_share_schema
from ..models.product import Product
from ..serializers.product import product_share_schema

blueprint_product = Blueprint('product', __name__, url_prefix='/api')


@blueprint_product.route('/product/register', methods=['POST'])
def product_register():
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

            return result, HTTPStatus.CREATED.value
    except KeyError:
        return jsonify({'error': 'Payload is not valid'})
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST.value


@blueprint_product.route('/product/show/title', methods=['POST'])
def product_show_by_title():
    try:
        if request.method == 'POST':
            result = product_share_schema.dump(
                Product.query.filter_by(title=request.json['title']).first()
            )

        return jsonify(result), HTTPStatus.FOUND.value
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST.value


@blueprint_product.route('/product/<identificator>', methods=['GET'])
def product_show_by_id(identificator: int):
    if request.method == 'GET':
        result = product_share_schema.dump(
            Product.query.filter_by(id=identificator).first()
        )

    return jsonify(result), HTTPStatus.FOUND.value


@blueprint_product.route('/product/change/title/', methods=['PUT'])
def product_change_by_title():
    try:
        if request.method == 'PUT':

            title = request.json['title_update']

            product_query = Product.query.filter_by(title=title).first()

            if product_share_schema.dump(product_query) == {}:
                return jsonify({'msg': 'Product not found'}), HTTPStatus.NO_CONTENT.value

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

        return jsonify(result), HTTPStatus.OK.value
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}),HTTPStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST.value


@blueprint_product.route('/product/delete/title/', methods=['DELETE'])
def product_delete_by_title():
    try:
        if request.method == 'DELETE':

            title = request.json['title_delete']

            product_query = Product.query.filter_by(title=title).first()

            if product_share_schema.dump(product_query) == {}:
                return jsonify({'msg': 'Product not found'}), HTTPStatus.NO_CONTENT.value

            db.session.delete(product_query)

            db.session.commit()

        return jsonify(
            f'The product with title {request.json["title_delete"]} is deleted'
        ), HTTPStatus.OK.value
    except KeyError:
        return jsonify({'error': 'Payload is not valid'}), HTTPStatus.BAD_REQUEST.value
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST.value


@blueprint_product.route('/product/favorite/register', methods=['POST'])
def favorite_product_register():
    try:
        if request.method == 'POST':
            favorite = request.json['favorite']
            client_id = request.json['client_id']
            product_id = request.json['product_id']

            favorite_prod = FavoriteProduct(
                favorite=favorite,
                client_id=client_id,
                product_id=product_id
            )

            validate = favorite_product_share_schema.dump(
                FavoriteProduct.query.filter_by(
                    client_id=client_id,
                    product_id=product_id
                ).first()
            )

            if validate != {}:
                return jsonify(
                    {'error': 'O client já possui esse produto em sua lista de favoritos'}
                ), HTTPStatus.BAD_REQUEST.value

            db.session.add(favorite_prod)
            db.session.commit()

            result = favorite_product_share_schema.dump(
                FavoriteProduct.query.filter_by(
                    favorite=favorite,
                    client_id=client_id,
                    product_id=product_id
                ).first()
            )

            return result, HTTPStatus.CREATED.value
    except KeyError:
        return jsonify({'error': 'Payload is not valid'})
    except Exception as e:
        return jsonify({'error': e.orig.args}), HTTPStatus.BAD_REQUEST.value
