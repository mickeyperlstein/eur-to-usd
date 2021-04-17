import os

from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


@app.route("/", methods=["POST"])
def my_form_post():

    euros = request.form["euros"]
    usd = round(2.25, 2)

    return render_template("form.html", euros=euros, usd=usd)


if __name__ == "__main__":
    is_dev = os.environ.get('USERNAME', 'root') != 'root'
    app.run(debug=is_dev, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


