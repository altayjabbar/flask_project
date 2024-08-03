from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# create a flask instance
app = Flask(__name__)
# add DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# secret key
app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"

# initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# create model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<Name %r>" % self.name

# create a Form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                favorite_color=form.favorite_color.data,  # Corrected spelling here
            )
            db.session.add(user)
            db.session.commit()
            flash("User Added Successfully")
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_color.data = ''
    our_users = User.query.order_by(User.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = User.query.order_by(User.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("There was a problem deleting the user")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

# update database record
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_color = request.form["favorite_color"]

        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return redirect(url_for("update", id=id))
        except:
            db.session.rollback()
            flash("Error! Looks like there was a problem... try again!")
    return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator
@app.route("/")
def index():
    first_name = "Jabbarov"
    stuff = "This is my first post"
    favorite_pizza = ["pepperoni", "cheese"]
    return render_template("index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully")
    return render_template("name.html", name=name, form=form)

if __name__ == "__main__":
    app.run(debug=True)
