from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserViewsTestCase(TestCase):
    """Tests for website functionality."""

    def setUp(self):
        """Add sample user."""
        User.query.delete()
        
        user = User(first_name = "Sky", last_name = "Heart", image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSDW6BAjwutEPaFdaZJYbhYDCUwfqtjz5Vcg&usqp=CAU")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_list_users(self):
        with app.test_request_context():
            with app.test_client() as client:
                resp = client.get("/users")
                html = resp.get_data(as_text = True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('Sky', html)
        
    def test_view_user_page(self):
        with app.test_request_context():
            with app.test_client() as client:
                resp = client.get(f"/users/{self.user_id}")
                html = resp.get_data(as_text = True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("<h1>Sky's Page</h1>", html)
                self.assertIn(self.user.last_name, html)
    
    def test_add_user(self):
        with app.test_request_context():
            with app.test_client() as client:
                new_user = {"first_name" : "Hero", "last_name" : "Gaga", "image_url" : "www.google.com"}
                resp = client.post("/users/new", data=new_user, follow_redirects=True)
                html = resp.get_data(as_text= True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("Hero Gaga", html)

