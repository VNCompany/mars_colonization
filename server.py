from flask import Flask, url_for, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"

prfs = [
    ('e1', "инженер-исследователь"),
    ('e2', "пилот"),
    ('e3', "строитель"),
    ('e4', "экзобиолог"),
    ('e5', "врач"),
    ('e6', "инженер по терраформированию"),
    ('e7', "климатолог"),
    ('e8', "специалист по радиационной защите"),
    ('e9', "астрогеолог"),
    ('e10', "гляциолог"),
    ('e11', "инженер жизнеобеспечения"),
    ('e12', "метеоролог"),
    ('e13', "оператор марсохода")
]


class AstronautForm(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])
    education = SelectField("Выберите образование",
                            choices=[('e1', 'Начальное'), ('e2', 'Среднее'), ('e2', 'Высшее')])
    profession = RadioField("Выберите профессию", choices=prfs)
    sex = RadioField("Выбретие пол", choices=[('male', 'Мужской'), ('female', 'Женский')])
    motivation = TextAreaField("Комментарий")
    ready = BooleanField("Готовы остаться на Марсе?")
    submit = SubmitField("Отправить")


class LoginForm(FlaskForm):
    id1 = StringField("Id астронавта", validators=[DataRequired()])
    token1 = PasswordField("Пароль астронавта", validators=[DataRequired()])
    id2 = StringField("Id капитана", validators=[DataRequired()])
    token2 = PasswordField("Пароль капитана", validators=[DataRequired()])
    submit = SubmitField("Доступ")


@app.route("/<title_value>")
@app.route("/index/<title_value>")
def index(title_value):
    return render_template('base.html', title=title_value)


@app.route("/training/<prof>")
def training(prof: str):
    prof_result = prof.lower()

    if "инженер" in prof_result or "строитель" in prof_result:
        prof_result = 1
    else:
        prof_result = 0

    return render_template('training.html', title=prof, p=prof_result)


@app.route("/list_prof/<ltype>")
def list_prof(ltype):
    profs = [
        "инженер-исследователь",
        "пилот",
        "строитель",
        "экзобиолог",
        "врач",
        "инженер по терраформированию",
        "климатолог",
        "специалист по радиационной защите",
        "астрогеолог",
        "гляциолог",
        "инженер жизнеобеспечения",
        "метеоролог",
        "оператор марсохода"
    ]

    return render_template('list_prof.html', title=ltype, ltype=ltype, profs=profs)


@app.route("/answer", methods=['POST', 'GET'])
@app.route("/auto_answer", methods=['POST', 'GET'])
def auto_answer():
    form = AstronautForm()
    if form.validate_on_submit():
        education = form.education.data
        if education == "e1":
            education = "Начальное"
        elif education == "e2":
            education = "Среднее"
        elif education == "e3":
            education = "Высшее"
        d = {
            "title": "Анкета",
            "surname": form.surname.data,
            "name": form.name.data,
            "education": education,
            "profession": [prof[1] for prof in prfs if prof[0] == form.profession.data][0],
            "sex": form.sex.data,
            "motivation": form.motivation.data,
            "ready": form.ready.data
        }
        return render_template("auto_answer.html", title="Ответ",
                               spec_link=url_for('static', filename="css/form2_style.css"), form=d)
    else:
        return render_template("form_1.html", title="Анкета", form=form,
                               spec_link=url_for('static', filename="css/form_style.css"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return "OK"
    else:
        return render_template("login.html", title="Аварийный доступ",
                               spec_link=url_for('static', filename="css/login.css"),
                               form=form)


@app.route("/distribution")
def distribution():
    li = [
        "Антон Павлов",
        "Иван Иванов",
        "Вася Пупкин"
    ]
    return render_template("distribution.html", title="По каютам", people=li)


@app.route("/table/<sex>/<int:age>")
def cabin_table(sex, age: int):
    if age < 21:
        age = url_for('static', filename="img/emblems/little.png")
        if sex == "male":
            sex = "lightskyblue"
        else:
            sex = "violet"
    else:
        age = url_for('static', filename="img/emblems/big.png")
        if sex == "male":
            sex = "cornflowerblue"
        else:
            sex = "palevioletred"
    return render_template("cabin_table.html", title="Cabin Table", sex=sex, age=age)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
