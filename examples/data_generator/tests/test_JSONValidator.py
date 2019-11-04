from unittest import TestCase
from validators import JSONValidator

from json import load


class TestJSONValidator(TestCase):

    WRONG_DATA_PATH = "../payloads/dump_payload_wrong_dataset.json"
    RIGHT_DATA_PATH = "../payloads/dump_payload_right_dataset.json"
    JSON_SCHEMA = "../schemas/dump_payload_schema.json"

    """
        Test if JSONValidator class works correctly in the way:

        - Contains the right schema defined in the project
        - Can correctly detect datasets with the right schema
        - Can correctly detect datasets with any wrong schema
        - Does not allow any objects except for dict and strings, which can be parsed into dict after
    """

    def test_dump_payload_schema(self):

        """
            Support utility to encapsulate routines for schema checking tests
        :param schema_path:
        :return:
        """

        # read existing scheme
        with open(self.JSON_SCHEMA) as file:
            schema = load(file)

        validator = JSONValidator(self.JSON_SCHEMA)
        is_identical = validator.compare_schema(schema)

        self.assertTrue(is_identical)

    def test_right_data(self):

        dataset_path = self.RIGHT_DATA_PATH

        # read a sample data
        with open(dataset_path) as file:
            correct_samples = load(file)

        validator = JSONValidator(self.JSON_SCHEMA)
        is_valid = all([validator.validate(sample) for sample in correct_samples])

        self.assertTrue(is_valid)

    def test_wrong_data(self):

        dataset_path = self.WRONG_DATA_PATH

        # read a sample data
        with open(dataset_path) as file:
            wrong_samples = load(file)

        validator = JSONValidator(self.JSON_SCHEMA)
        is_not_valid = all([not validator.validate(sample) for sample in wrong_samples])

        self.assertTrue(is_not_valid)

    def test_validate_not_correct_data(self):

        """
            Test if JSONValidator raise ValueError on every object which cannot be transformed into dict -> JSON
        :return: None
        """

        # Just take any types

        any_wrong_samples = [object(), 1, "hello world", 123.32, []]

        validator = JSONValidator(self.JSON_SCHEMA)

        for wrong_sample in any_wrong_samples:
            with self.assertRaises(ValueError):
                validator.validate(wrong_sample)