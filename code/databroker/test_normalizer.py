from unittest import TestCase

from databroker.classes import Normalizer


class TestNormalizer(TestCase):

    def setUp(self) -> None:
        pass

    def test__try_cast(self):
        self.fail()

    def test_normalize(self):

        normalizer = Normalizer()

        json_dict = normalizer.normalize()

        self.assertTrue(isinstance(dict, json_dict))
        self.assertGreater(len(json_dict), 0)
