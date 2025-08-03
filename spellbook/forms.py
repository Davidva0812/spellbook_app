from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, BooleanField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_login import current_user
from spellbook.models import User


class NewSpellForm(FlaskForm):
    name = StringField("Spell's name", validators=[DataRequired()])
    school = StringField("School of Magic", validators=[DataRequired()])
    level = IntegerField("Level", validators=[DataRequired(), NumberRange(min=1, max=5)])
    description = TextAreaField("Describe it")
    image = FileField("Upload the spell's image", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    #author = current_user
    submit = SubmitField("Save")


class NewUserForm(FlaskForm):
    username = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("E- mail address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Password again",
                                     validators=[
                                         DataRequired(),
                                         EqualTo("password",
                                                 message="Does not match the password provided above.")
                                     ])
    submit = SubmitField("Registration")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already used. Please add another name!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already used. Please add another name!")


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("I will stay logged in")
    submit = SubmitField("Log in")