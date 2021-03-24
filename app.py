import os
from datetime import datetime
import requests
from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://grin:fgolden1306!@localhost/goldennet'
app.config['SECRET_KEY'] = '12345'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['UPLOAD_FOLDER'] = '/www/goldennet/Admin/static/shop_img'
app.config['SHOP_GROUP_FOLDER'] = '/www/goldennet/Admin/static/shop_group_img'
app.config['UPLOAD_FOLDER_NEWS'] = '/www/goldennet/Admin/static/news_img'

app.config['DEBUG'] = False
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
from models import *

ALLOWED_EXTENSIONS = set(['ico', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home
@app.route('/')
def admin():
    return render_template('index.html')


# Group
@app.route('/main-group')
def main_group():
    parent_group = ParentGroup.query.all()
    sub_group = SubGroup.query.all()
    return render_template('pages/group-add.html', parent_group=parent_group, sub_group=sub_group)


@app.route("/add-main-group", methods=['POST'])
def add_group():
    name = request.form.get('name')
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['SHOP_GROUP_FOLDER'], filename))
            pg = ParentGroup(name=name,
                             img='https://mag.golden.net.ua/static/shop_group_img/' + filename)
            db.session.add(pg)
            db.session.commit()
        else:
            pg = ParentGroup(name=name)
            db.session.add(pg)
            db.session.commit()

    return redirect('/main-group')


@app.route("/delete-parent-group=<int:id>")
def delete_parent_group(id):
    ParentGroup.query.filter(ParentGroup.id == id).delete()
    db.session.commit()
    return redirect('/main-group')


# subGroup
@app.route("/add-sub-group", methods=['POST'])
def product_add_sub_group():
    p_name = request.form.get('p_name')
    p_id = request.form.get('p_id')
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['SHOP_GROUP_FOLDER'], filename))
            p = SubGroup(tag=p_name, parent_id=p_id,
                         img='https://mag.golden.net.ua/static/shop_group_img/' + filename)
            db.session.add(p)
            db.session.commit()
        else:
            p = SubGroup(tag=p_name, parent_id=p_id)
            db.session.add(p)
            db.session.commit()

    return redirect('/main-group')


@app.route("/delete-sub-group=<int:id>")
def delete_sub_group(id):
    SubGroup.query.filter(SubGroup.id == id).delete()
    db.session.commit()
    return redirect('/main-group')


# Product
@app.route('/product')
def product():
    products = Product.query.all()
    parent_group = ParentGroup.query.all()
    sub_group = SubGroup.query.all()
    return render_template('pages/product.html', parent_group=parent_group, sub_group=sub_group, products=products)


@app.route("/product-add", methods=['POST'])
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

            p = Product(name=name, description=description, short_description=short_description,
                        price=price, discount=discount, group_id=group_id,
                        img='https://mag.golden.net.ua/static/shop_img/' + filename)
            db.session.add(p)
            db.session.commit()
        else:
            p = Product(name=name, description=description, short_description=short_description,
                        price=price, discount=discount, group_id=group_id)
            db.session.add(p)
            db.session.commit()
    return redirect('/product')


@app.route('/product-edit=<int:id>')
def product_edit(id):
    products_group = SubGroup.query.all()
    product = Product.query.filter(Product.id == id)
    return render_template('pages/product-edit.html', products_group=products_group, product=product)


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


# NEWS
@app.route("/news")
def news():
    news = News.query.all()
    return render_template('pages/news.html', news=news)


@app.route("/news-add", methods=['POST'])
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


# API

# GROUP-LIST
@app.route('/api/main-group-list/p')
def main_group_json():
    group = ParentGroup.query.all()
    group_schema = ParentGroupSchema(many=True)
    output = group_schema.dump(group)
    return jsonify({'data': output})


# SUB-GROUP-LIST
@app.route('/api/sub-group-list/p=<int:id>')
def sub_group_json(id):
    group = SubGroup.query.filter(SubGroup.parent_id == id)
    group_schema = SubGroupSchema(many=True)
    output = group_schema.dump(group)
    return jsonify({'data': output})


# SITE_PODUCT_GROUP_API
@app.route('/api/product-list/p=<int:id>')
def product_json(id):
    product = Product.query.filter(Product.group_id == id)
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(product)
    return jsonify({'data': output})


# SITE_NEWS_API
@app.route('/api/news-list/p')
def news_json():
    news = News.query.all()
    news_schema = NewsSchema(many=True)
    output = news_schema.dump(news)
    return jsonify({'data': output})


# SITE_NEWS_API_FILTER
@app.route('/api/news-one-filter-list/p=<int:id>')
def news_filter_json(id):
    news = News.query.filter(News.id == id).first()
    news_schema = NewsSchema()
    output = news_schema.dump(news)
    return jsonify({'data': output})


# GENERATE_SCRF_TOKEN
@app.route('/api/csrf/cookie', methods=['GET'])
def token():
    res = {'csrfToken': generate_csrf()}
    return jsonify(res)


# QUESTION_API
@app.route('/api/question', methods=['POST'])
def question_api():
    # GetFormData
    FormData = request.get_json()

    # GetTime
    now = datetime.now()
    dt_string = str(now.strftime("%d.%m.%Y %H:%M:%S"))

    # ReSendPost
    url = 'https://apiv2.golden.net.ua/v2/private/customers/question'
    headers = {
        'Content-type': 'application/json',
        'X-Auth-Key': '697d2532-4c71-4e64-b9c3-a203e9af03e4'
    }

    json = {
        "agreement_id": 11988,
        "reason_id": 12,
        "phone": FormData['phone'],
        "destination_time": dt_string,
        "comment": '\n' + 'Звернення: ' + FormData['name'] + '\n' + 'Причина: ' + FormData['message']
    }

    response = requests.post(url, json=json, headers=headers)
    print(response.text)
    return ""


@app.errorhandler(404)
def page_not_found(e):
    return '<h1 style="text-align:center;color:red;">Error 404 , Страница не найдена;)<h1/>' \
           '<p style="text-align:center;">Текст ошибки :</p>'+  '<p style="text-align:center;">' + str(e) + '<p/>'\
           '<br> <p style="text-align:center;">Обратитесь к администратору</p> <br>'


@app.errorhandler(500)
def server_error(e):
    return '<h1 style="text-align:center;color:red;">Error 500 , Ошибка сервера;)<h1/>' \
           '<p style="text-align:center;">Текст ошибки :</p>'+  '<p style="text-align:center;">' + str(e) + '<p/>'\
           '<br> <p style="text-align:center;">Обратитесь к администратору</p> <br>'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
