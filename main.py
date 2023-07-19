from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddCafeForm, RegisterForm, LoginForm, CommentForm
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('appconfigsecretkey')
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)


# log in as admin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    map_url = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    has_sockets = db.Column(db.Boolean(), nullable=False)
    has_toilet = db.Column(db.Boolean(), nullable=False)
    has_wifi = db.Column(db.Boolean(), nullable=False)
    can_take_calls = db.Column(db.Boolean(), nullable=False)
    seats = db.Column(db.String(100))
    coffee_price = db.Column(db.Integer)


class Cafes(db.Model):
    __tablename__ = 'cafes'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100), nullable=False, unique=True)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(100), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("cafes.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    text = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()

    # all Flask routes below
    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/cafes")
    def cafes():
        # display all current relative info from updated db
        cafe = Cafe.query.all()
        print(cafes)
        return render_template("cafes.html", all_cafes=cafe)


    @app.route("/add", methods=["POST", "GET"])
    def add():
        # add form allowing user to add cafe to db
        form = AddCafeForm()
        return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
