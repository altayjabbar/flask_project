from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create a flask instance
app = Flask(__name__)
# add DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# secret key
app.config["SECRET_KEY"] = "my super secret key that no one supported to know"

# initialize the database
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()


# create model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Name %r>" % self.name


# create a Form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])

    submit = SubmitField("Submit")


class NameForm(FlaskForm):
    name = StringField("what is Your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a route derector
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.name.data = ""
        flash("User Added Successfully")
    our_users = User.query.order_by(User.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


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
        form.name.data = ""
        flash("Form Submitted Successfully")
    return render_template("name.html", name=name, form=form)


if __name__ == "__main__":
    app.run(debug=True)
