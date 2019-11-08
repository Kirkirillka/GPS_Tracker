from unittest import TestCase

from databroker.classes import Normalizer
from databroker.test_utils import get_correct_data_with_correct_scheme, get_correct_data_with_wrong_scheme


class TestNormalizer(TestCase):

    def setUp(self) -> None:
        pass

    def test__try_cast(self):
        self.fail()

    def test_normalize_correct_data_wrong_scheme(self):

        data = get_correct_data_with_wrong_scheme()

        normalizer = Normalizer()

        json_dict = normalizer.normalize(data)

        self.assertTrue(isinstance(dict, json_dict))
        self.assertGreater(len(json_dict), 0)

    def test_normalize_correct_data_right_scheme(self):

        data = get_correct_data_with_correct_scheme()

        normalizer = Normalizer()

        json_dict = normalizer.normalize(data)

        self.assertTrue(isinstance(dict, json_dict))
        self.assertGreater(len(json_dict), 0)
