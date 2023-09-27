from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app import app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
admin = Admin(app)
