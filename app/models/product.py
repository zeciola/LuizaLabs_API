from dataclasses import dataclass

from app import db


@dataclass()
class FavoriteProduct(db.Model):
    id: int = db.Column(db.Integer, autoincrement=True, primary_key=True)
    favorite: bool = db.Column(db.Boolean, nullable=False)
    client_id: int = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    product_id: int = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"<FavoriteProduct : {self.favorite} >"


@dataclass()
class Product(db.Model):
    id: int = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title: str = db.Column(db.String(2048), nullable=False, unique=True)
    image: str = db.Column(db.String(2048), nullable=False)
    amount: int = db.Column(db.Integer, nullable=False)
    price: float = db.Column(db.Numeric, nullable=False)
    brand: str = db.Column(db.String(2048), nullable=False)
    review_score: float = db.Column(db.Numeric, nullable=False)

    prod_favorite = db.relationship(
        FavoriteProduct,
        backref='Product',
        uselist=False
    )

    def __repr__(self):
        return f"<Product : {self.title} >"
