from unittest import TestCase

from validators import JSONValidator
from generators import JSONGenerator
from field_gens import empty_message


class TestJSONGenerator(TestCase):
    def test_generate_on__empty_sample(self):

        """
            Test if the producing an empty sample having a valid JSON scheme
        :return: None
        """

        validator = JSONValidator()
        generator = JSONGenerator(empty_message)

        # Take only one sample from JSONGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_to_iterate(self):

        """
            Test if we can use JSONGenerator as an iterator
        :return:
        """

        validator = JSONValidator()
        generator = JSONGenerator(empty_message)

        # Takes thirty samples from JSONGenerator
        samples = [next(generator) for x in range(30)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
