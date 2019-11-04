from unittest import TestCase

from validators import JSONValidator
from generators import JSONGenerator
from field_gens import DUMP_PAYLOAD_FIELDS_TEMPLATE


class TestJSONGenerator(TestCase):


    JSON_SCHEMA = "../schemas/dump_payload_schema.json"
    ITERATION_LENGTH = 30

    def test_generate_on_dump_sample(self):

        """
            Test if the producing an empty sample having a valid JSON scheme
        :return: None
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = JSONGenerator(DUMP_PAYLOAD_FIELDS_TEMPLATE)

        # Take only one sample from JSONGenerator
        sample = generator.get()

        self.assertTrue(validator.validate(sample))

    def test_generator_to_iterate(self):

        """
            Test if we can use JSONGenerator as an iterator
        :return:
        """

        validator = JSONValidator(self.JSON_SCHEMA)
        generator = JSONGenerator(DUMP_PAYLOAD_FIELDS_TEMPLATE)

        # Takes thirty samples from JSONGenerator
        samples = [next(generator) for x in range(30)]

        is_valid = all([validator.validate(sample) for sample in samples])

        self.assertTrue(is_valid)
