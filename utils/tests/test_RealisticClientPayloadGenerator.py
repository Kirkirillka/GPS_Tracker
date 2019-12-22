from unittest import TestCase


from utils.validators import WIFIPayloadValidator
from utils.generators import RealisticClientPayloadGenerator

from utils.tools import read_schema_from_file


class TestRealisticClientPayloadGenerator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.JSON_SCHEMA_PATH = "wifi_payload_schema.json"

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("wifi_payload_schema.json")
        self.validator = WIFIPayloadValidator()
        self.generator = RealisticClientPayloadGenerator()
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
        for index in range(self.ITERATION_LENGTH):

            sample = generator.get()
            is_valid = validator.validate(sample)

            self.assertTrue(is_valid)