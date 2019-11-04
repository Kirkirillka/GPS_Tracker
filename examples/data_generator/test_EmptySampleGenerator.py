from unittest import TestCase

from validators import JSONValidator
from generators import EmptySampleGenerator


class TestEmptySampleGenerator(TestCase):
    def test_generate_on_empty_sample(self):

        """
            Test if the producing an empty sample
        :return: None
        """

        validator = JSONValidator("valid_schema.json")
        generator = EmptySampleGenerator()

        # Take only one sample from EmptySampleGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_to_iterate(self):

        """
            Test if we can use EmptySampleGenerator as an iterator
        :return:
        """


        generator = EmptySampleGenerator()
        validator = JSONValidator("valid_schema.json")

        # Takes thirty samples from EmptySampleGenerator
        samples = [next(generator) for x in range(30)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
