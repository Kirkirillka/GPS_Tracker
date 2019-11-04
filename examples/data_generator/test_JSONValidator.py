from unittest import TestCase
from validators import JSONValidator

from json import load


class TestJSONValidator(TestCase):

    wrong_data_path = "wrong_data.json"
    right_data_path = "correct_data.json"

    """
        Test if JSONValidator class works correctly in the way:

        - Contains the right schema defined in the project
        - Can correctly detect datasets with the right schema
        - Can correctly detect datasets with any wrong schema
        - Does not allow any objects except for dict and strings, which can be parsed into dict after
    """

    def test_empty_samples_schema(self):

        """
            Support utility to encapsulate routines for schema checking tests
        :param schema_path:
        :return:
        """

        # read existing scheme
        with open("valid_schema.json") as file:
            schema = load(file)

        validator = JSONValidator("valid_schema.json")
        is_identical = validator.compare_schema(schema)

        self.assertTrue(is_identical)

    def test_correct_empty_samples_dataset(self):

        dataset_path = self.right_data_path

        # read a sample data
        with open(dataset_path) as file:
            correct_samples = load(file)

        validator = JSONValidator("valid_schema.json")
        is_valid = all([validator.validate(sample) for sample in correct_samples])

        self.assertTrue(is_valid)

    def test_wrong_empty_samples_dataset(self):

        dataset_path = self.wrong_data_path

        # read a sample data
        with open(dataset_path) as file:
            wrong_samples = load(file)

        validator = JSONValidator("valid_schema.json")
        is_not_valid = all([not validator.validate(sample) for sample in wrong_samples])

        self.assertTrue(is_not_valid)

    def test_get_valid_empty_message_schema(self):

        """
            Test if an instantiated object from JSONValidator contains an valid schema set by the project
        :return:
        """

        pass

    def test_get_valid_wifi_status_schema(self):
        """
            Test if an instantiated object from JSONValidator contains an valid schema set by the project
        :return:
        """

        pass


    def test_validate_empty_message_right_dataset(self):

        """
            Test if JSONValidator validate the correct dataset as a right dataset as well
        :return: None
        """

        pass

    def test_validate_emtpy_message_wrong_dataset(self):

        """
            Test if JSONValidator validate the correct dataset as a wrong dataset as well
        :return: None
        """
        pass

    def test_validate_not_correct_data(self):

        """
            Test if JSONValidator raise ValueError on every object which cannot be transformed into dict -> JSON
        :return: None
        """

        # Just take any types

        any_wrong_samples = [ object(), 1, "hello world", 123.32, []]

        validator = JSONValidator("valid_schema.json")

        for wrong_sample in any_wrong_samples:
            with self.assertRaises(ValueError):
                validator.validate(wrong_sample)