# test.py
import unittest
import sys
import os

# To resolve the import error, Python needs to recognize min_example as a module by including its directory in sys.path. Here’s a summary of a couple of solutions based on your setup:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app  # Import directly if `app.py` is in the root `min_example`


class FlaskAppTests(unittest.TestCase):
    # This decorator makes setUpClass a class method rather than an instance method. This means it’s run once for the entire class, rather than before each individual test method. The cls is passed to setUpClass instead of self, representing the class itself rather than an instance of the class.
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()  # Create a test client

    def test_hello_world(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, World!", response.data)

    def test_hello_route(self):
        response = self.client.get("/hello/John")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, John!", response.data)

    def test_user_profile(self):
        response = self.client.get("/user/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User 1", response.data)

    def test_post_route(self):
        response = self.client.post("/post/", json={"id": 1, "name": "Item1"})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Item created", response.data)

    def test_search_route(self):
        response = self.client.get("/search/?id=2")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User 2", response.data)

    def test_subpath_route(self):
        response = self.client.get("/path/subdir/subsubdir")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Subpath subdir/subsubdir", response.data)


if __name__ == "__main__":
    unittest.main()
