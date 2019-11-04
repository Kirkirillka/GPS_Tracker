from unittest import TestCase

from validators import JSONValidator
from generators import WifiInfoGenerator


class TestWifiInfoGenerator(TestCase):
    def test_generate_on_wifi_info_sample(self):

        """
            Test if the producing an empty sample
        :return: None
        """

        validator = JSONValidator("wifi_status_schema.json")
        generator = WifiInfoGenerator()

        # Take only one sample from WifiInfoGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_to_iterate(self):

        """
            Test if we can use WifiInfoGenerator as an iterator
        :return:
        """

        validator = JSONValidator("wifi_status_schema.json")
        generator = WifiInfoGenerator()

        # Takes thirty samples from EmptySampleGenerator
        samples = [next(generator) for x in range(30)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
