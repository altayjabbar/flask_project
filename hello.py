from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# create a flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key that no one supported to know"


# create a Form class
class NameForm(FlaskForm):
    name = StringField("what is Your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a route derector
@app.route("/")
def index():
    first_name = "Jabbarov"
    stuff = "This is my firstpost"
    favorite_pizza = ["paperroni", "chesse"]
    return render_template(
        "index.html",
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza,
    )


# localhost:5000/user/john
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# create name page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NameForm()
    # validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
