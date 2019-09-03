from dataclasses import dataclass
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from .product import FavoriteProduct


@dataclass()
class Client(db.Model):
    id: int = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullname: str = db.Column(db.String(128), nullable=False)
    email: str = db.Column(db.String(128), nullable=False, unique=True)
    password: str = db.Column(db.String(128), nullable=False)
    favorite_products = db.relationship(FavoriteProduct, backref=backref('client'))

    def hash_password(password) -> str:
        return generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(password, self.password)

    def __repr__(self):
        return f"<Client : {self.fullname} >"
