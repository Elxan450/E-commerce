from flask import render_template, request, redirect, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from models import User, Product, Image, Review, Category, Favorite, Contact, Subscriber
from forms import RegisterForm, LoginForm, ReviewForm, ContactForm, SubscriberForm
from werkzeug.security import check_password_hash
from extensions import db
import datetime

@app.route("/", methods = ['GET'])
def shop():
    product_name = request.args.get("product_name")
    print(product_name)
    try:
        products = Product.query.filter(Product.name.contains(product_name)).all()
    except:
        products = Product.query.all()

    products_num = len(products)
    categories = Category.query.all()

    return render_template("shop.html", products = products, categories = categories, products_num = products_num)

@app.route("/category/<string:category_name>/", methods = ['GET'])
def filter_category(category_name):
    category = Category.query.filter_by(name = category_name).first()
    products = Product.query.filter_by(category_id = category.id)
    products_num = Product.query.filter_by(category_id = category.id).count()
    categories = Category.query.all()
    return render_template("shop.html", products = products, categories = categories, products_num = products_num)

@app.route("/product/<string:product_name>/", methods = ['GET', 'POST'])
def detail(product_name):
    product = Product.query.filter_by(name = product_name).first()
    form = ReviewForm()
    if request.method == "POST":
        post_data = request.form
        form = ReviewForm(data = post_data)
        if form.validate_on_submit():
            review = Review(content = form.content.data, user_id = current_user.id, product_id = int(product.id))
            review.save()
            flash("Your review was submitted successfully", "success")
            return redirect(url_for("detail", product_name = product.name))
        else:
            flash("The form was not submitted correctly!", "danger")
            return redirect(url_for("detail", product_name = product.name))
    favorite = None
    if current_user.is_authenticated:
        favorite = Favorite.query.filter_by(user_id = current_user.id, product_id = product.id).first()
    similar_products =  Product.query.filter_by(category_id = product.category_id)
    reviews_num = Review.query.filter_by(product_id = product.id).count()
    return render_template("detail.html", product = product, similar_products = similar_products, form = form, reviews_num = reviews_num, fav = favorite)

@app.route("/add_favorites/<int:id>/", methods = ['POST'])
@login_required
def add_favorites(id):
    try:
        favorite = Favorite(user_id = current_user.id, product_id = id)
        favorite.save()
        flash("The product was added to the wishlist!", "success")
        return redirect(url_for("shop"))
    except:
        flash("Something went wrong!", "danger")
        return redirect(url_for("shop"))
    
@app.route("/favorites/")
@login_required
def favorites():
    products = Favorite.get_products(current_user.id)
    return render_template("favorites.html", products = products)

@app.route("/delete_favorite/<int:id>/", methods = ['POST'])
@login_required
def delete_favorite(id):
    try:
        favorite = Favorite.query.filter_by(user_id = current_user.id, product_id = id).first()
        favorite.remove()
        flash("The product was deleted from the wishlist", "success")   
        return redirect(url_for("shop"))
    except:
        flash("Something went wrong", "warning")   
        return redirect(url_for("shop"))
    
@app.route("/contact/", methods = ['POST', 'GET'])
def contact():
    form = ContactForm()
    if request.method == "POST":
        post_data = request.form
        form = ContactForm(data = post_data)
        if form.validate_on_submit():
            contact = Contact(name = form.name.data, email = form.email.data, subject = form.subject.data, message = form.message.data)
            contact.save()
            flash("Your message was submitted successfully", "success")
            return redirect(url_for("shop"))
        else:
            flash("The form was not submitted correctly!", "danger")
            return redirect(url_for("shop"))
    return render_template("contact.html", form = form)

@app.context_processor
def context_processor():
    sub_form = SubscriberForm()
    favorites_num = 0
    if current_user.is_authenticated:
        favorites_num = Favorite.query.filter_by(user_id = current_user.id).count()
    return dict(sub_form = sub_form, favorites_num = favorites_num)

@app.route("/subscribe/", methods = ['POST'])
def subscribe():
    post_data = request.form
    form = SubscriberForm(data = post_data)
    if form.validate_on_submit():
        subscriber = Subscriber(name = form.name.data, email = form.email.data)
        subscriber.save()
        flash("Your message was submitted successfully", "success")
        return redirect(url_for("shop"))
    else:
        flash("The form was not submitted correctly!", "danger") 
        return redirect(url_for("shop"))

#Review crud
@app.route("/review_edit/<string:product_name>/<int:review_id>/", methods = ['GET', 'POST'])
@login_required
def review_edit(product_name, review_id):
    review = Review.query.filter_by(id = review_id).first()
    form = ReviewForm(content = review.content)
    if request.method == 'POST':
        post_data = request.form
        form = ReviewForm(data = post_data)
        if form.validate_on_submit():
            review.content = form.content.data
            review.edited = True
            review.last_edited = datetime.datetime.now()
            review.save()
            flash("Your review was edited successfully!", "success")
            return redirect(url_for("detail", product_name = product_name))
        else:
            flash("The form was not submittes correctly!", "danger")
            return redirect(url_for("detail", product_name = product_name))
    return render_template("review_edit.html", form = form)

@app.route("/review_delete/<string:product_name>/<int:review_id>/", methods = ['GET', 'POST'])
@login_required
def review_delete(product_name, review_id):
    try:
        review = Review.query.filter_by(id = review_id).first()
        review.remove()
        flash("The review was deleted", "success")   
        return redirect(url_for("detail", product_name = product_name))
    except:
        flash("Something went wrong", "warning")   
        return redirect(url_for("detail", product_name = product_name))

#Authentication
@app.route("/register/", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        post_data = request.form
        form = RegisterForm(data = post_data)
        if form.validate_on_submit():
            if form.password1.data == form.password2.data:
                user = User(first_name = form.first_name.data, last_name = form.last_name.data, email = form.email.data, username = form.username.data, password = form.password1.data)
                user.save()
                flash("You registered successfully", "success")
                return redirect(url_for("login"))
            else:
                flash("The passwords do not match!", "danger")
                return redirect(url_for("register"))
        else:
            flash("The form was not submittes correctly!", "danger")
            return redirect(url_for("register"))
        
    return render_template("register.html", form = form)

@app.route("/login/", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        post_data = request.form
        form = LoginForm(data = post_data)
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You logged in successfully!", "success")
                return redirect(url_for("shop"))
            else:
                flash("Username or password is not correct!", "warning")
                return redirect(url_for("login"))
        else:
            flash("The form was not submitted correctly!", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form = form)

@app.route("/logout/")
@login_required
def logout():   
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("shop"))

# privilage_required_routes = ['/admin/']
# @app.before_request
# def before_request():
#     if request.path in privilage_required_routes:
#         if (not current_user.is_authenticated) or (not current_user.is_superuser):
#             flash("You cannot access the admin panel!", "danger")
#             return redirect(url_for('shop'))

        

