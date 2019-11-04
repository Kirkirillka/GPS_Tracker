from unittest import TestCase

from validators import JSONValidator
from generators import WIFIPayloadGenerator


class TestWIFIPayloadGenerator(TestCase):

    JSON_SCHEMA = "../schemas/wifi_payload_schema.json"
    ITERATION_LENGTH = 30

    def test_generate_on_wifi_info_sample(self):

        """
            Test if the producing an empty sample
        :return: None
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = WIFIPayloadGenerator()

        # Take only one sample from WifiInfoGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_to_iterate(self):

        """
            Test if we can use WifiInfoGenerator as an iterator
        :return:
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = WIFIPayloadGenerator()

        # Takes thirty samples from EmptySampleGenerator
        samples = [next(generator) for x in range(self.ITERATION_LENGTH)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
