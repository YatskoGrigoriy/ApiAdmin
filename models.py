from app import db, ma
from datetime import datetime


class ParentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    def __repr__(self):
        return '<ParentGroup id: {}, name: {}>'.format(self.id, self.name)


class SubGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(200))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent_group.id', ondelete='CASCADE'))


    def __repr__(self):
        return '<ProductGroup id: {}, name: {}>'.format(self.id, self.tag)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('sub_group.id'))
    name = db.Column(db.String(200))
    img = db.Column(db.String(100))
    description = db.Column(db.Text())
    short_description = db.Column(db.Text())
    price = db.Column(db.String(100))
    discount = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Product id: {}, name: {}>'.format(self.id, self.name)


class ParentGroupSchema(ma.ModelSchema):
    class Meta:
        model = ParentGroup


class SubGroupSchema(ma.ModelSchema):
    class Meta:
        model = SubGroup


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product


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
