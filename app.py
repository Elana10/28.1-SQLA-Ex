"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ponyboy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

app.app_context().push()
# ACCESS FLASK WITHIN IPYTHON AND HAVE SESSIONS
 
@app.route('/')
def home_page():
    """Hold please."""
    return redirect ('/users')

@app.route('/users')
def list_users():
    """Queries the database for all current entries in alphabetical order and passes the list to list.html where jinja iterates over the list to display an unordered list."""
    users = User.query.order_by(User.first_name).all()
    return render_template('list.html', users=users)

@app.route('/users/new', methods = ["POST","GET"])
def add_user_form():
    """Handle the route for /users/new with either a GET or POST request. 
    - Get request will show the new user form on user_page.html template.
    - Post request will handle the entered user information by adding it to the database AND redirect to web page to the user list page. """
    if request.method == 'GET':
        return render_template('new_user.html')

    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url =  request.form["image_url"]

        new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    
@app.route('/users/<int:user_id>')
def view_user_page(user_id):
    """View an individual user page."""
    user = User.query.get_or_404(user_id)
    return render_template('user_page.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST', 'GET'])
def edit_user(user_id):
    """Edit an individual user. """
    user = User.query.get_or_404(user_id)
    
    if request.method == 'GET':
        return render_template('edit_user_page.html', user=user)

    if request.method == 'POST':
        first_name = request.form["first_name"]
        if first_name != '':
            user.first_name = first_name
        last_name = request.form["last_name"]
        if last_name != '':
            user.last_name = last_name
        image_url =  request.form["image_url"]
        if image_url != '':
            user.image_url = image_url

        db.session.commit()

        # return f"first: {user.first_name} last: {user.last_name} url: {user.image_url}"
        return redirect(f'/users/{user.id}')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_the_user(user_id):
    """Deletes the user from the database."""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/')