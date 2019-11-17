from flask import Flask, render_template


ERROR = "I feel disturbance in force {}"

# configure application
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/")
def contacts():
    return render_template("contacts.html")


@app.route("/law")
def law():
    return render_template("law.html")


@app.route("/mediation")
def mediation():
    return render_template("mediation.html")


@app.route("/school")
def school():
    return render_template("school.html")
