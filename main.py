from flask import Flask, url_for, request, render_template
from data import db_session
import os

from data.users import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    captain = User(
        surname="Scott",
        name="Ridley",
        age=21,
        position="captain",
        speciality="research engineer",
        address="module_1",
        email="scott_chief@mars.org"
    )
    user1 = User(
        surname="Pavlov",
        name="Anton",
        age=25,
        position="colonist",
        speciality="builder",
        address="module_2",
        email="pavlov.anton@bing.com"
    )
    user2 = User(
        surname="Ivanov",
        name="Ivan",
        age=20,
        position="colonist",
        speciality="doctor",
        address="module_3",
        email="ivan777@mail.ru"
    )
    user3 = User(
        surname="Vasiliy",
        name="Pupkin",
        age=22,
        position="colonist",
        speciality="meteorologist",
        address="module_4",
        email="vpup@yandex.ru"
    )

    session.add(captain)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
    return "Данные добавлены!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/database.sqlite")
    app.run(host='0.0.0.0', port=port)
