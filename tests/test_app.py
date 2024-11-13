import unittest
from app import create_app, db
from app.models import User, Task
from flask_login import current_user

class TaskManagementTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.drop_all()

    def login_user(self):
        """Helper method to log in the test user."""
        return self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)

    def test_user_registration(self):
        """Test user registration functionality."""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertIn(b'Your account has been created!', response.data)

    def test_user_login(self):
        """Test user login functionality."""
        response = self.login_user()
        self.assertIn(b'You have been logged in!', response.data)

    def test_create_task(self):
        """Test creating a task."""
        self.login_user()
        response = self.client.post('/create_task', data={
            'title': 'Test Task'
        }, follow_redirects=True)
        self.assertIn(b'Task created successfully!', response.data)

    def test_task_list_display(self):
        """Test if the task list displays correctly for the logged-in user."""
        self.login_user()
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_report_page(self):
        """Test access to the report page."""
        self.login_user()
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Report', response.data)

if __name__ == '__main__':
    unittest.main()
