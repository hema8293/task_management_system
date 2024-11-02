import unittest
from app import create_app, db
from app.models import User, Task

class TaskManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)
        self.assertIn(b'Your account has been created!', response.data)

    def test_create_task(self):
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()

        with self.client:
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            response = self.client.post('/create_task', data={
                'title': 'New Task'
            }, follow_redirects=True)
            self.assertIn(b'Task created successfully!', response.data)

    def test_complete_task(self):
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            task = Task(title='Test Task', user_id=user.id)
            db.session.add(task)
            db.session.commit()

        with self.client:
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            response = self.client.post('/complete_task/1', follow_redirects=True)
            self.assertIn(b'Task marked as complete!', response.data)

    def test_delete_task(self):
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            task = Task(title='Test Task', user_id=user.id)
            db.session.add(task)
            db.session.commit()

        with self.client:
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            response = self.client.post('/delete_task/1', follow_redirects=True)
            self.assertIn(b'Task deleted successfully!', response.data)

    def test_create_task_missing_title(self):
        with self.client:
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            response = self.client.post('/create_task', data={
                'title': ''
            }, follow_redirects=True)
            self.assertIn(b'Title is required to create a task.', response.data)

    def test_unauthorized_task_completion(self):
        with self.app.app_context():
            another_user = User(username='anotheruser', password='anotherpassword')
            db.session.add(another_user)
            db.session.commit()
            task = Task(title='Another User Task', user_id=another_user.id)
            db.session.add(task)
            db.session.commit()

        with self.client:
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            }, follow_redirects=True)
            response = self.client.post('/complete_task/1', follow_redirects=True)
            self.assertIn(b'Unauthorized action.', response.data)

if __name__ == '__main__':
    unittest.main()
