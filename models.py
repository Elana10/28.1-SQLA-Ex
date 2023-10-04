"""Models for Blogly."""
 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
db = SQLAlchemy()
  
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(30),
                           nullable = False)
    last_name = db.Column(db.String(30),
                          nullable = False)
    image_url = db.Column(db.String(),
                          nullable = True) 
    posts = db.relationship(
                    'Post',
                    backref = "user",
                    cascade = "all, delete-orphan")
     
    @property
    def full_name(self):
        """Return full name of user. """
        return f"{self.first_name} {self.last_name}" 
    
    def __repr__(self):
        return f"User : {self.first_name} {self.last_name}"

class Post(db.Model):
    """Blog post."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(60),
                      nullable = False)
    content = db.Column(db.String())
    created_at = db.Column(db.DateTime,
                        nullable = False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="CASCADE"))
    posttag = db.relationship(
                    'PostTag', 
                    backref = 'post')

    def __repr__(self):
        return f"Title: {self.title} user: {self.user.first_name}"

class Tag(db.Model):
    """Tag that can be added to posts."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, 
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.String(50),
                     nullable = False, 
                     unique = True)
    
    posts = db.relationship(
            'Post', 
            secondary = "posts_tags", 
            backref = "tags",
            cascade = "all, delete"
            )
    
    posttag = db.relationship( 
            'PostTag',
            backref = "tag"
    )

    
    def __repr__(self):
        return f"Tag #: {self.id} Name: {self.name}"

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'), 
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'), 
                       primary_key = True)
    
