from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


class UserModelTestCase(TestCase):
    """Tests model for Users."""

    def setUp(self):
        """Remove any existing users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_full_name_property(self):
        user = User(first_name="Bob", last_name="Dylan")
        self.assertEqual(user.full_name, "Bob Dylan")