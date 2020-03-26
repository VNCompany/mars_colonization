from flask import Flask, url_for, request, render_template
from data import db_session
import os

from data.users import *
from data.jobs import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    return render_template("journal.html", spec_link=url_for('static', filename="css/journal_style.css"),
                           actions=session.query(Jobs).all())


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/database.sqlite")
    app.run(host='0.0.0.0', port=port)
