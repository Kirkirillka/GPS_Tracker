from unittest import TestCase

from validators import JSONValidator
from field_gens import gen_empty_sample_packet


class TestGen_empty_sample_packet(TestCase):
    def test_gen_empty_sample_packet(self):

        """
            Test if the producing sample has a valid JSON scheme
        :return: None
        """

        validator = JSONValidator()

        empty_sample = gen_empty_sample_packet()

        self.assertTrue(validator.validate(empty_sample))
