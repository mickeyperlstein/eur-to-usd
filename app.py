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

    import rule_engine
    import datetime
    datetime.datetime.fromisoformat()
    # match a literal first name and applying a regex to the email
    rule = rule_engine.Rule(
        'first_name == "Luke" and email =~ ".*@rebels.org$"'
    )  # => <Rule text='first_name == "Luke" and email =~ ".*@rebels.org$"' >
    rule.matches({
        'first_name': 'Luke', 'last_name': 'Skywalker', 'email': 'luke@rebels.org'
    })  # => True
    rule.matches({
        'first_name': 'Darth', 'last_name': 'Vader', 'email': 'dvader@empire.net'
    })  # => False

