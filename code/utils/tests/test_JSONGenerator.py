from unittest import TestCase

from utils.validators import JSONValidator
from utils.generators import JSONGenerator
from utils.field_gens import DUMP_PAYLOAD_FIELDS_TEMPLATE

from utils.tools import read_schema_from_file, read_payload_from_file


def return_incorrect_payload(*args, **kwargs):

    return [object(), 1, "hello world", 123.32, []]


class TestJSONValidator(TestCase):

    """
        Test if JSONValidator class works correctly in the way:

        - Contains the right schema defined in the project
        - Can correctly detect datasets with the right schema
        - Can correctly detect datasets with any wrong schema
        - Does not allow any objects except for dict and strings, which can be parsed into dict after
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.RIGHT_DATA_PATH = "dump_payload_right_dataset.json"
        cls.WRONG_DATA_PATH = "dump_payload_wrong_dataset.json"
        cls.JSON_SCHEMA_PATH = "dump_payload_schema.json"

    def setUp(self) -> None:

        self.wrong_data = read_payload_from_file(self.WRONG_DATA_PATH)
        self.right_data = read_payload_from_file(self.RIGHT_DATA_PATH)
        self.json_schema = read_schema_from_file(self.JSON_SCHEMA_PATH)
        self.incorrect_samples = return_incorrect_payload()

        self.validator = JSONValidator(self.json_schema)

    def test_schema(self):

        """
            Support utility to encapsulate routines for schema checking tests
        :param schema_path:
        :return:
        """

        # read existing scheme
        schema = self.json_schema

        validator = self.validator
        is_identical = validator.compare_schema(schema)

        self.assertTrue(is_identical)

    def test_right_data(self):

        # read a sample data
        payload = self.right_data

        validator = self.validator
        is_valid = all([validator.validate(sample) for sample in payload])

        self.assertTrue(is_valid)

    def test_wrong_data(self):

        # read a sample data
        payload = self.wrong_data

        validator = self.validator
        is_not_valid = all([not validator.validate(sample) for sample in payload])

        self.assertTrue(is_not_valid)

    def test_incorrect_data(self):

        """
            Test if JSONValidator raise ValueError on every object which cannot be transformed into dict -> JSON
        :return: None
        """

        # Just take any types

        incorrect_data = self.incorrect_samples

        validator = JSONValidator(self.json_schema)

        for incorrect_sample in incorrect_data:
            with self.assertRaises(ValueError):
                validator.validate(incorrect_sample)


class TestJSONGenerator(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.ITERATION_LENGTH = 30

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("dump_payload_schema.json")
        self.validator = JSONValidator(self.json_schema)
        self.generator = JSONGenerator(DUMP_PAYLOAD_FIELDS_TEMPLATE)

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
