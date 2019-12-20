from unittest import TestCase

from utils.logs.tools import read_logging_config

class TestRead_config(TestCase):
    def test_read_config(self):

        config = read_logging_config()

        self.assertTrue(isinstance(config,dict))
