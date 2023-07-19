from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


##WTForm

class AddCafeForm(FlaskForm):
    name = StringField("Name of Cafe", validators=[DataRequired()])
    map_url = StringField("Map url", validators=[DataRequired(), URL()])
    img_url = StringField("Img url", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField(validators=[DataRequired()])
    has_toilet = BooleanField(validators=[DataRequired()])
    has_wifi = BooleanField(validators=[DataRequired()])
    can_take_calls = BooleanField(validators=[DataRequired()])
    seats = StringField("Number of seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee price in pounds", validators=[DataRequired()])
    submit = SubmitField("Submit Cafe")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit comment")


