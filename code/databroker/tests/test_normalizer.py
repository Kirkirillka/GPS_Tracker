import json
from unittest import TestCase

from utils.generators import WIFIPayloadGenerator, RawPayloadGenerator

from databroker.model import Normalizer
from databroker.test_utils import get_correct_data_with_correct_scheme, get_correct_data_with_wrong_scheme


class TestNormalizer(TestCase):

    def setUp(self) -> None:
        pass

    def test_normalize_correct_data_wrong_scheme(self):
        data = get_correct_data_with_wrong_scheme()

        normalizer = Normalizer()

        json_dict = normalizer.normalize(data)

        self.assertFalse(isinstance(json_dict, dict))
        self.assertEqual(json_dict, None)

    def test_normalize_correct_data_right_scheme(self):
        dataset = get_correct_data_with_correct_scheme()

        normalizer = Normalizer()

        for row in dataset:
            json_dict = normalizer.normalize(row)

            self.assertTrue(isinstance(json_dict, dict))
            self.assertGreater(len(json_dict), 0)


    def test_normalize_from_generators(self):
        normalizer = Normalizer()

        # For each registered JSON-valid generators
        for g_class in (WIFIPayloadGenerator, RawPayloadGenerator):

            # Instantiate generator and take one sample
            generator = g_class()
            sample = generator.get()

            # Transform JSON-valid dictionary into different castable objects
            testing_dataset = (
                sample,  # dict itself
                json.dumps(sample),  # str
                json.dumps(sample).encode()  # bytes
            )

            # For each test sample
            for test_sample in testing_dataset:
                # Check if it can be normalized into valid data structure (JSON-valid dictionary)
                n_object = normalizer.normalize(test_sample)

                self.assertTrue(isinstance(n_object, dict))
                self.assertTrue(n_object is not None)
