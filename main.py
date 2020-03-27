from flask import Flask, url_for, request, render_template
from data import db_session
import os

from data.users import *
from data.jobs import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


class RegisterForm(FlaskForm):
    login = StringField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password",
                             [
                                 DataRequired(),
                                 EqualTo('repeat_password', message="Passwords don't match")
                             ])
    repeat_password = PasswordField("Repeat password")
    surname = StringField("Surname")
    name = StringField("Name")
    age = StringField("Age")
    position = StringField("Position")
    speciality = StringField("Speciality")
    address = StringField("Address")
    submit = SubmitField("Submit")


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    return render_template("journal.html", spec_link=url_for('static', filename="css/journal_style.css"),
                           actions=session.query(Jobs).all())


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return render_template("success.html", title="Registration",
                               color="green", text="Registration successfully!")
    else:
        return render_template("register.html", title="Registration",
                               spec_link=url_for('static', filename="css/register_style.css"),
                               form=form)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/database.sqlite")
    app.run(host='0.0.0.0', port=port)
