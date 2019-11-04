from unittest import TestCase

from validators import JSONValidator
from generators import RawPayloadGenerator


class TestRawPayloadGenerator(TestCase):

    JSON_SCHEMA = "../schemas/raw_payload_schema.json"
    ITERATION_LENGTH = 30

    def test_generate_on_raw_payload(self):

        """
            Test if the producing an empty sample
        :return: None
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = RawPayloadGenerator()

        # Take only one sample from EmptySampleGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_as_iterator(self):

        """
            Test if we can use RawPayloadGenerator as an iterator
        :return:
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = RawPayloadGenerator()

        # Takes thirty samples from EmptySampleGenerator
        samples = [next(generator) for x in range(self.ITERATION_LENGTH)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
