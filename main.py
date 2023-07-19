from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from dotenv import load_dotenv


def configure():
    load_dotenv()


configure()

app = Flask(__name__)
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


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Cafes(db.Model):
    __tablename__ = 'cafes'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100), unique=True, nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("cafes.id"))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

    # all Flask routes below
    @app.route("/")
    def home():
        return render_template("index.html")


    @app.route("/cafes", methods=["POST", "GET"])
    def cafes():
        form = Cafes.query.all()
        return render_template("cafes.html", form=form)


    @app.route("/add")
    def add():
        return render_template("add.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
