from flask import Flask, url_for, request, render_template, redirect
import flask_login
from flask_login import LoginManager, login_user, logout_user, login_required
from data import db_session
import os

from data.users import *
from data.jobs import *
from data.departments import *

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


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


class LoginForm(FlaskForm):
    login = StringField("Login / email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")


class JobForm(FlaskForm):
    team_leader = IntegerField("Team leader id", validators=[DataRequired()])
    job = StringField("Job")
    work_size = StringField("Work size")
    collaborators = StringField("Collaborators")
    start_date = DateField("Start date", default=datetime.datetime.now)
    end_date = DateField("End date")
    is_finished = BooleanField("Is finished")
    submit = SubmitField("Add")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("journal.html", title="Главная страница",
                           actions=jobs, spec_link=url_for('static', filename="css/journal_style.css"))


@app.route("/job_add", methods=['GET', 'POST'])
def job_add():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
        )
        session.add(job)
        session.commit()
        return redirect("/index")
    else:
        return render_template("job_add.html", title="New job", form=form,
                               spec_link=url_for('static', filename="css/jadd.css"))


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", title="Authorization", form=form,
                               spec_link=url_for('static', filename="css/login_style.css"),
                               error="Invalid login or password")
    else:
        return render_template("login.html", title="Authorization", form=form,
                               spec_link=url_for('static', filename="css/login_style.css"))


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
    # db_session.global_init("C:\\Users\\victor\\Desktop\\db.sqlite")
    db_session.global_init("db/database.sqlite")
    app.run(host='127.0.0.1', port=5000)
