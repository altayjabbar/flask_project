from flask import Flask ,render_template 

# create a flask instance
app  =  Flask(__name__)
# create a route derector
@app.route('/')
def index():
    first_name = 'Jabbarov'
    stuff = 'This is my firstpost'
    favorite_pizza = ['paperroni','chesse']
    return render_template('index.html',
            first_name=first_name,
            stuff = stuff,
            favorite_pizza = favorite_pizza,)

# localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

if __name__=='__main__':
    app.run(debug=True)
