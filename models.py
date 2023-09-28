"""Models for Blogly."""
 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
db = SQLAlchemy()
  
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
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
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}" 
    
    def __repr__(self):
        return f"User : {self.first_name} {self.last_name}"

class Post(db.Model):
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
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref = "posts")

    def __repr__(self):
        return f"Title: {self.title} user: {self.user.first_name}"
    
