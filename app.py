"""Blogly application."""
 
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime
from sqlalchemy import desc

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
    posts = Post.query.order_by(desc(Post.created_at)).limit(5)
    return render_template('recent_posts.html', posts = posts)

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

        return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>/edit', methods = ['POST', 'GET'])
def edit_post(post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)

    if request.method == 'GET':
        return render_template('edit_post_page.html', post=post)
    
    if request.method == 'POST':
        title = request.form['title']
        if title != '':
            post.title = title
        content = request.form['content']
        if content != '':
            post.content = content
        post.created_at = datetime.now()

        db.session.commit()

        return redirect(f'/posts/{post_id}')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_the_user(user_id):
    """Deletes the user from the database."""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/posts/new', methods = ['POST', 'GET'])
def create_new_post_form(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return render_template('new_post_form.html', user=user)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now()
        #Current date and time. 

        new_post = Post(title = title, content=content, created_at = created_at, user_id = user.id)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{user.id}')
    
@app.route('/posts/<int:post_id>')
def view_single_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("view_single_post.html", post=post)

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect('/users')
 