"""Blogly application.

NOTES: delete post route is not set to delete all items from the database, and therefor won't work. 
--> The other delete routes get around this by manually cycling through and deleting connections. 
--> I was not able to get the SQLAlchemy ON CASCADE DELETE feature to work.

The html and python for editing a post does not include the tags update. I would just cpoy the code over from the '/users/user_id/posts/new' route. 


"""
 
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    user = User.query.get_or_404(user_id)

    for post in user.posts:
        for tag in post.posttag:
            PostTag.query.filter(PostTag.post_id == post.id).delete()
        Post.query.filter(Post.id == post.id).delete()

    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods = ['POST', 'GET'])
def create_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all() 

    if request.method == 'GET':
        return render_template('new_post_form.html', user=user, tags=tags)
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now()
        #Current date and time. 
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        new_post = Post(title = title, content=content, created_at = created_at, user_id = user.id, tags=tags)
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
 
@app.route('/tags')
def view_list_of_all_tags():
    """View list of all tags with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_list_of_posts_with_tag_and_link_to_edit_or_delete(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tag_related_posts.html', posts=posts, tag=tag)

@app.route('/tags/new', methods = ['POST','GET'])
def create_new_tag():
    """ get: Shows a form to add a new tag.
        post: Process add form, adds tag, and redirect to tag list.
    """
    tags = Tag.query.all()
    if request.method == 'GET':
        return render_template('new_tag.html')
    
    if request.method == 'POST':
        tag_name = request.form['tag_name']

        for tag in tags:
            if tag.name == tag_name:
                flash("That tag already exists. Please enter a new tag.", "duplicate_tag")
                return redirect('/tags/new')
        
        tag = Tag(name = tag_name)
        db.session.add(tag)
        db.session.commit()

        return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods = ['POST', 'GET'])
def edit_a_tag_name(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'GET':
        return render_template('edit_tag_name.html', tag = tag)
    
    if request.method == 'POST':
        new_name = request.form['tag_name_edit']
        if new_name != '':
            tag.name = new_name

        db.session.commit()
        
        return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag_from_website(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    for post in tag.posttag:
        pt = PostTag.query.filter(post.tag_id == tag.id).delete()
    
    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()

    return redirect('/tags')


@app.route('/all-posts')
def view_all_posts():
    posts = Post.query.all()
    return render_template('all_posts.html', posts = posts)