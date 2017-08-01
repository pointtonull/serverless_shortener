"""
Regexs tests cases
"""

import unittest

from chalicelib import regexs


class Test_URLS_Regex(unittest.TestCase):
    """
    Tests the given example
    """

    def test__url_regex__should_validate_good_urls(self):
        good_urls = [
            "http://localhost:8000",
            "http://google.com",
            "https://google.com"
            ]
        for good_url in good_urls:
            self.assertTrue(regexs.url.match(good_url), msg=good_url)

    def test__url_regex__should_detect_bad_urls(self):
        bad_urls = [
            "htp://localhost:8000",
            "http:///google.com",
            "https://google..com",
            "localhost:8000/url"
            ]
        for bad_url in bad_urls:
            self.assertFalse(regexs.url.match(bad_url), msg=bad_url)
