from unittest import TestCase

from utils.validators import RawPayloadValidator
from utils.generators import RawPayloadGenerator

from utils.tools import read_schema_from_file


class TestRawPayloadGenerator(TestCase):

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("raw_payload_schema.json")
        self.validator = RawPayloadValidator()
        self.generator = RawPayloadGenerator()
        self.ITERATION_LENGTH = 30

    def test_generate(self):

        """
            Test if the producing an empty sample having a valid JSON scheme
        :return: None
        """

        validator = self.validator
        generator = self.generator

        # Take only one sample from JSONGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_iterate(self):

        """
            Test if we can use JSONGenerator as an iterator
        :return:
        """

        validator = self.validator
        generator = self.generator

        # Takes thirty samples from JSONGenerator
        _ = [next(generator) for x in range(self.ITERATION_LENGTH)]

        is_valid = all([validator.validate(sample) for sample in _])

        self.assertTrue(is_valid)
