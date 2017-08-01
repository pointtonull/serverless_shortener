"""
App interface tests cases
"""
import unittest

import moto
mock = moto.mock_dynamodb2()
mock.start()

import app


class TestApp(unittest.TestCase):
    """
    Tests the given example
    """

    def test__get_root__returns_valid_dict(self):
        result = app.get_root()
        self.assertIsInstance(result, dict)
        self.assertIn("service", result)
        self.assertIn("endpoints", result)

    def test__get_create_short__accepts_no_argument(self):
        self.assertEqual(0, app.get_create_short.__code__.co_argcount)
