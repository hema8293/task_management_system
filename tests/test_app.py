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

    # Failing test for task creation
    def test_create_task(self):
        response = self.client.post('/create_task', data={
            'title': 'New Task'
        }, follow_redirects=True)
        self.assertIn(b'Task created successfully!', response.data)

    # Failing test for task completion
    def test_complete_task(self):
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            task = Task(title='Test Task', user_id=user.id)
            db.session.add(task)
            db.session.commit()
        
        response = self.client.post('/complete_task/1', follow_redirects=True)
        self.assertIn(b'Task marked as complete!', response.data)

    # Failing test for task deletion
    def test_delete_task(self):
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()
            task = Task(title='Test Task', user_id=user.id)
            db.session.add(task)
            db.session.commit()
        
        response = self.client.post('/delete_task/1', follow_redirects=True)
        self.assertIn(b'Task deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
