from app import db, ma
from datetime import datetime


class ProductGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(140))
    product_id = db.relationship('Product', backref='group', lazy="dynamic")

    def __repr__(self):
        return '<ProductGroup id: {}, name: {}>'.format(self.id, self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    img = db.Column(db.String(100))
    description = db.Column(db.Text())
    short_description = db.Column(db.String(150))
    price = db.Column(db.String(100))
    discount = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.now())
    group_id = db.Column(db.Integer, db.ForeignKey('product_group.id'))

    def __repr__(self):
        return '<Product id: {}, name: {}>'.format(self.id, self.name)

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
class ProductGroupSchema(ma.ModelSchema):
    class Meta:
        model = ProductGroup

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    img = db.Column(db.String(100))
    text = db.Column(db.Text())
    short_text = db.Column(db.String(150))
    created = db.Column(db.DateTime, default=datetime.now())

class NewsSchema(ma.ModelSchema):
    class Meta:
        model = News
