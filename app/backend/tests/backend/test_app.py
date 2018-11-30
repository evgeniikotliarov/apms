import unittest

# from backend.tests.backend.fake_app_factory import TestAppFactory
from backend.tests.backend.fake_app_factory import TestAppFactory


class AppTestCase(unittest.TestCase):
    def test_create_app(self):
        app = TestAppFactory().create_app()
        self.assertIsNotNone(app)
