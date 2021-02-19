import os
from flask import Flask, render_template, url_for, redirect, request, session, request,jsonify
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://grin:fgolden1306!@localhost/goldennet'
app.config['SECRET_KEY'] = '12345'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['UPLOAD_FOLDER'] = '/www/goldennet/Admin/static/shop_img'
app.config['UPLOAD_FOLDER_NEWS'] = '/www/goldennet/Admin/static/news_img'

app.config['DEBUG'] = True
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
from models import *

ALLOWED_EXTENSIONS = set(['ico','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def admin():
    return render_template('index.html')


@app.route("/product-add-group",methods = ['POST'])
def product_add_group():
    group = request.form.get('group')

    pg = ProductGroup(tag=group)
    db.session.add(pg)
    db.session.commit()

    return redirect('/product')


@app.route("/product-delete-group=<int:id>")
def product_delete_group(id):
    pdg = ProductGroup.query.filter(ProductGroup.id == id).delete()
    db.session.commit()
    return redirect('/product')

#SITE_PODUCT_GROUP_API
@app.route('/api/group-list/p')
def group_json():
    group = ProductGroup.query.all()
    group_schema = ProductGroupSchema(many=True)
    output = group_schema.dump(group)
    return jsonify({'group': output})


@app.route('/product')
def product():
    products = Product.query.all()
    products_group = ProductGroup.query.all()
    return render_template('pages/product.html', products=products,products_group=products_group)

@app.route("/product-add",methods = ['POST'])
def product_add():
    name = request.form.get('name')
    description = request.form.get('description')
    short_description = request.form.get('short_description')
    price = request.form.get('price')
    discount = request.form.get('discount')
    group_id = request.form.get('group_id')

    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            p = Product(name=name,description=description,short_description=short_description,
                        price=price,discount=discount, group_id= group_id,img='https://mag.golden.net.ua/static/shop_img/' + filename)
            db.session.add(p)
            db.session.commit()
        else:
            p = Product(name=name,description=description,short_description=short_description,
                        price=price,discount=discount, group_id= group_id)
            db.session.add(p)
            db.session.commit()
    return redirect('/product')

@app.route('/product-edit=<int:id>')
def product_edit(id):
    products_group = ProductGroup.query.all()
    product = Product.query.filter(Product.id == id)
    return render_template('pages/product-edit.html',  products_group=products_group, product=product)

@app.route("/product-edit-add=<int:id>", methods=['POST'])
def product_edit_add(id):
    product = Product.query.filter(Product.id == id).first()
    name = request.form.get('name')
    description = request.form.get('description')
    short_description = request.form.get('short_description')
    price = request.form.get('price')
    discount = request.form.get('discount')
    group_id = request.form.get('group_id')

    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.img = 'https://mag.golden.net.ua/static/shop_img/' + filename

        product.name = name
        product.description = description
        product.shor_description = short_description
        product.price = price
        product.discount = discount
        product.group_id = group_id
        db.session.commit()

    return redirect(url_for('product'))


@app.route("/product-delete=<int:id>")
def product_delete(id):
    pdg = Product.query.filter(Product.id == id).delete()
    db.session.commit()
    return redirect('/product')


#SITE_PRODUCT_API
@app.route('/api/product-list/p')
def product_json():
    product = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(product)
    return jsonify({'products': output})

#SITE_PRODUCT_API+GROUP
@app.route('/api/product-list/pg')
def product_pg_json():
    product = db.session.query(Product.name,  Product.img, Product.description, \
         Product.short_description, Product.price,  Product.discount, ProductGroup.tag) \
        .outerjoin(ProductGroup, Product.group_id == ProductGroup.id)
    product_schema = ProductSchema(many=True)
    a ={}
    for p in product:
        a.update(p)
    # data, errors =  product_schema.dump([{'name': x[0], 'img': x[1],\
    # 'description': x[2], 'short_description': x[3],'price': x[4], 'discount': x[5]} for x in product])
    # output = product_schema.dump(errors)
    print(a)
    return jsonify({'products': data})



#NEWS
@app.route("/news")
def news():
    news = News.query.all()
    return render_template('pages/news.html', news=news)

@app.route("/news-add",methods = ['POST'])
def news_add():
    title = request.form.get('title')
    text = request.form.get('text')
    short_text = request.form.get('short_text')
    img = request.form.get('img')

    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_NEWS'], filename))

            n = News(title=title, text=text, short_text=short_text,
                        img='https://mag.golden.net.ua/static/news_img/' + filename)
            db.session.add(n)
            db.session.commit()
        else:
            n = News(title=title, text=text, short_text=short_text)
            db.session.add(n)
            db.session.commit()
    return redirect('/news')

@app.route('/news-edit=<int:id>')
def news_edit(id):
    news = News.query.filter(News.id == id)
    return render_template('pages/news-edit.html', news=news)

@app.route("/news-edit-add=<int:id>", methods=['POST'])
def news_edit_add(id):
    news = News.query.filter(News.id == id).first()
    title = request.form.get('title')
    short_text = request.form.get('short_text')
    text = request.form.get('text')
    img = request.form.get('img')

    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER_NEWS'], filename))
            news.img = 'https://mag.golden.net.ua/static/news_img/' + filename

        news.title = title
        news.short_text = short_text
        news.text = text
        db.session.commit()

    return redirect(url_for('news'))

@app.route("/news-delete=<int:id>")
def news_delete(id):
    n = News.query.filter(News.id == id).delete()
    db.session.commit()
    return redirect('/news')

#SITE_NEWS_API
@app.route('/api/news-list/p')
def news_json():
    news = News.query.all()
    news_schema = NewsSchema(many=True)
    output = news_schema.dump(news)
    return jsonify({'news': output})

#SITE_NEWS_API_FILTER
@app.route('/api/news-one-filter-list/p=<int:id>')
def news_filter_json(id):
    news = News.query.filter(News.id == id).first()
    news_schema = NewsSchema()
    output = news_schema.dump(news)
    return jsonify({'news': output})








if __name__ == "__main__":
    app.run(host='0.0.0.0')
