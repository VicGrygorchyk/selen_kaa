import os

from flask import Flask, render_template

# configure application
flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/")
def contacts():
    return render_template("contacts.html")


@flask_app.route("/law")
def law():
    return render_template("law.html")


@flask_app.route("/mediation")
def mediation():
    return render_template("mediation.html")


@flask_app.route("/school")
def school():
    return render_template("school.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(debug=True, port=port)
