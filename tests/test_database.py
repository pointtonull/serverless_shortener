"""
Database test cases
"""
import unittest

import moto
mock = moto.mock_dynamodb2()
mock.start()

from chalicelib.database import Urls, BadRequestError, NotFoundError


class TestDatabase(unittest.TestCase):
    """
    Tests the given example
    """

    def setUp(self):
        self.urls = Urls()

    def test__shorten__should_return_short(self):
        good_url = "http://google.com"
        result = self.urls.shorten(good_url)
        self.assertIsInstance(result, str)
        self.assertTrue(result)

    def test__shorten__should_raise__when_invalid(self):
        bad_url = "http//google.com"
        with self.assertRaises(BadRequestError):
            result = self.urls.shorten(bad_url)

    def test__lengthen__should_return_long_back(self):
        good_url = "http://google.com"
        short_url = self.urls.shorten(good_url)
        long_back = self.urls.lengthen(short_url)
        self.assertEqual(good_url, long_back)

    def test__lengthen__should_raise_invalid(self):
        bad_short_url = "SPAM"
        with self.assertRaises(BadRequestError):
            long_back = self.urls.lengthen(bad_short_url)

    def test__lengthen__should_raise_not_found(self):
        missing_short_url = "n1"
        with self.assertRaises(NotFoundError):
            long_back = self.urls.lengthen(missing_short_url)

