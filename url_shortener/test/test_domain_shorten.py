import unittest
from url_shortener import app_config
from url_shortener.domain import shorten as ShortenDomain
from url_shortener.exception import DataValidationError, ResourceNotFound


class TestDomainShorten(unittest.TestCase):

    def setUp(self):
        app_config.CONFIG = app_config.DevConfig

    def test_shorten_code(self):
        with self.assertRaises(DataValidationError):
            ShortenDomain._shorten_code(999)

        short_code = ShortenDomain._shorten_code('https://www.google.com/')
        self.assertIsInstance(short_code, str)
        self.assertEqual(len(short_code), 5)

    def test_create_shorten_url(self):
        with self.assertRaises(DataValidationError):
            ShortenDomain.create('www.google.com')

        with self.assertRaises(ResourceNotFound):
            ShortenDomain.create('http://www.google.com/fake')

        short_url = ShortenDomain.create('https://www.google.com')
        self.assertIsInstance(short_url, str)
        self.assertTrue(short_url.startswith(app_config.CONFIG.URL_PREFIX))
