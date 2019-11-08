from unittest import TestCase

from databroker.classes import Normalizer
from databroker.test_utils import get_correct_data_with_correct_scheme, get_correct_data_with_wrong_scheme


class TestNormalizer(TestCase):

    def setUp(self) -> None:
        pass

    def test_normalize_correct_data_wrong_scheme(self):

        data = get_correct_data_with_wrong_scheme()

        normalizer = Normalizer()

        json_dict = normalizer.normalize(data)

        self.assertFalse(isinstance(json_dict, dict ))
        self.assertEqual(json_dict, None)

    def test_normalize_correct_data_right_scheme(self):

        dataset = get_correct_data_with_correct_scheme()

        normalizer = Normalizer()

        for row in dataset:

            json_dict = normalizer.normalize(row)

            self.assertTrue(isinstance(json_dict, dict ))
            self.assertGreater(len(json_dict), 0)
