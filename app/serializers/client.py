from marshmallow import ValidationError, fields, validates

from app import ma
from app.models.client import Client


class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client
        fields = [
            'id',
            'fullname',
            'email',
            'password',
        ]

    fullname = fields.Str(required=True)
    email = fields.Str(required=True, unique=True)
    password = fields.Str(required=True)

    @validates('id')
    def validates_id(self, value):
        raise ValidationError("Please, don't send id")


client_share_schema = ClientSchema()
clients_share_schema = ClientSchema(many=True)
