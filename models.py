from flask import redirect, flash, url_for
from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You firstly have to log in!", "warning")
    return redirect(url_for("login"))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(30), nullable = False)
    username = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    profile_image = db.Column(db.String(50), nullable = False, default = "img/default-user.webp")
    is_active = db.Column(db.Boolean, nullable = False)
    is_superuser = db.Column(db.Boolean, nullable = False)
    reviews = db.relationship('Review', backref = 'User', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref = 'User', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, username, password, profile_image = "img/default-user.webp" ,is_active = True, is_superuser = False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.profile_image = profile_image
        self.is_active = is_active
        self.is_superuser = is_superuser

    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)

    def chech_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)

    def __init__(self, name):
        self.name = name

    def num_products(self):
        num_products = Product.query.filter_by(category_id = self.id).count()
        return num_products

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    discounted_price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    images = db.relationship('Image', backref = 'product', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref = 'product', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref = 'product', cascade='all, delete-orphan')

    def __init__(self, name, price, discounted_price, description, category_id):
        self.name = name
        self.price = price
        self.discounted_price = discounted_price
        self.description = description
        self.category_id = category_id

    def first_image(self):
        image = Image.query.filter_by(product_id = self.id).first()
        return image.image_url

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image_url = db.Column(db.String(50), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id')) 

    def __init__(self, image_url, product_id):
        self.image_url = image_url
        self.product_id = product_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    last_edited = db.Column(db.DateTime, nullable = False)
    edited = db.Column(db.Boolean, nullable = False, default = False)

    def __init__(self, content, user_id, product_id):
        self.content = content
        self.user_id = user_id
        self.product_id = product_id
        self.date = datetime.datetime.now()
        self.last_edited = datetime.datetime.now()

    def user(self):
        user = User.query.filter_by(id = self.user_id).first()
        return user

    def user_name(self):
        user = User.query.filter_by(id = self.user_id).first()
        return f'{user.first_name} {user.last_name}' 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))    

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def get_products(user_id):
        favorites = Favorite.query.filter_by(user_id = user_id)
        products = []
        for favorite in favorites:
            products.append(Product.query.filter_by(id = favorite.product_id).first())
        return products

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    subject = db.Column(db.String(100), nullable = False)
    message = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False)

    def __init__(self, name, email, subject, message):
        self.name = name
        self.email = email
        self.subject = subject 
        self.message = message
        self.date = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()