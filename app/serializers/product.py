from marshmallow import fields

from app import ma


class ProductSchema(ma.ModelSchema):
    class Meta:
        fields = [
            'id',
            'title',
            'image',
            'amount',
            'price',
            'brand',
            'review_score',
        ]

    title = fields.Str(required=True)
    image = fields.Str(required=True, unique=True)
    amount = fields.Int(required=True)
    price = fields.Float(required=True)
    brand = fields.Str(required=True)
    review_score = fields.Float(required=True)

    # @validate('id')
    # def validates_id(self, value):
    #     raise ValidationError("Please, don't send id")


product_share_schema: ProductSchema = ProductSchema()
products_share_schema: ProductSchema = ProductSchema(many=True)


class FavoriteProductSchema(ma.ModelSchema):
    class Meta:
        fields = [
            'id',
            'favorite',
            'client_id',
            'product_id'
        ]

    favorite = fields.Bool(required=True)
    client_id = fields.Int(required=True)
    product_id = fields.Int(required=True)

    # @validate('id')
    # def validates_id(self, value):
    #     raise ValidationError("Please, don't send id")


favorite_product_share_schema: FavoriteProductSchema = FavoriteProductSchema()
favorites_products_share_schema: FavoriteProductSchema = FavoriteProductSchema(many=True)
