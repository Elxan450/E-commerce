from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@127.0.0.1:3306/project'
app.config['SECRET_KEY'] = 'my_project'
app.secret_key = 'any random string'

from controllers import *
from models import *
from extensions import *

class ProductView(ModelView):
    form_columns = ['name', 'price', 'discounted_price', 'description', 'category_id', 'images']

class ImageView(ModelView):
    form_columns = ['image_url', 'product_id']
    column_list = ['image_url', 'product_id']

# class ProductView(ModelView):
#     inline_models = [(Image, dict(form_class=ImageView))]

class ReviewView(ModelView):
    form_columns = ['content', 'date', 'last_edited', 'edited', 'user_id', 'product_id']
    column_list = ['content', 'date', 'last_edited', 'edited', 'user_id', 'product_id']

class FavoriteView(ModelView):
    form_columns = ['user_id', 'product_id']
    column_list = ['user_id', 'product_id']

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(ImageView(Image, db.session))
admin.add_view(ReviewView(Review, db.session))
admin.add_view(FavoriteView(Favorite, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Subscriber, db.session))

if __name__ == "__main__":
    app.init_app(db)
    app.init_app(migrate)
    app.run(port = 5000, debug = True)