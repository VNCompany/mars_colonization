from flask import Flask, url_for, request, render_template
import os

app = Flask(__name__)


@app.route("/<title_value>")
@app.route("/index/<title_value>")
def index(title_value):
    return render_template('base.html', title=title_value)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
