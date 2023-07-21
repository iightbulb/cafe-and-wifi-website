from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import AddCafeForm, RegisterForm, LoginForm, CommentForm
from dotenv import load_dotenv
import os
from flask_gravatar import Gravatar
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


def configure():
    load_dotenv()


configure()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('appconfigsecretkey')
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

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


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()

    def admin_only(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.id != 1:
                return abort(403)
            return f(*args, **kwargs)

        return decorated_function

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
        if form.validate_on_submit():
            new_post = Cafe(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets=form.has_sockets.data,
                has_toilet=form.has_toilet.data,
                has_wifi=form.has_wifi.data,
                can_take_calls=form.can_take_calls.data,
                seats=form.seats.data,
                coffee_price=form.coffee_price.data,
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("cafes"))
        return render_template("cafe.html", form=form, current_user=current_user)


    @app.route("/post/<int:cafe_id>", methods=["POST", "GET"])
    def show_cafe(cafe_id):
        requested_cafe = Cafe.query.get(cafe_id)
        return render_template("cafe.html", cafe=requested_cafe, current_user=current_user)


    @app.route("/register", methods=["POST", "GET"])
    def register():
        register_form = RegisterForm()
        if register_form.validate_on_submit():
            if User.query.filter_by(email=register_form.email.data).first():
                flash("You've already signed up with that email, log in instead!")
                return redirect(url_for('login'))

            password_hash_with_salt = generate_password_hash(
                register_form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )

            new_user = User(

                email=register_form.email.data,
                name=register_form.name.data,
                password=password_hash_with_salt
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            return redirect(url_for('cafes'))
        return render_template("register.html", form=register_form, current_user=current_user)


    @app.route('/login', methods=["GET", "POST"])
    def login():
        login_form = LoginForm()

        if login_form.validate_on_submit():
            input_email = login_form.email.data
            input_password = login_form.password.data

            user = User.query.filter_by(email=input_email).first()

            if not user:
                flash("That email doesn't exist.")
                return redirect(url_for('login'))

            elif not check_password_hash(pwhash=user.password, password=input_password):
                flash("Incorrect password.")
                return redirect(url_for('login'))

            else:
                login_user(user)
                return redirect(url_for('cafes'))

        return render_template("login.html", form=login_form, current_user=current_user)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for("cafes"))


    @app.route("/delete/<int:cafe_id>")
    def delete_post(cafe_id):
        post_to_delete = Cafe.query.get(cafe_id)
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('cafes'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
