from unittest import TestCase
from validators import JSONValidator

from json import load


class TestJSONValidator(TestCase):
    def test_get_valid_schema(self):

        # read existing scheme
        with open("valid_scheme.json") as file:
            scheme = load(file)

        validator = JSONValidator()
        is_identical = validator.compare_schema(scheme)

        self.assertTrue(is_identical)

    def test_validate_right_dataset(self):

        # read a sample data
        with open("correct_data.json") as file:
            correct_samples = load(file)

        validator = JSONValidator()
        is_valid = all([True for sample in correct_samples if validator.validate(sample) is True])

        self.assertTrue(is_valid)

    def test_validate_wrong_dataset(self):

        # read a sample data
        with open("wrong_data.json") as file:
            wrong_samples = load(file)

        validator = JSONValidator()
        is_not_valid = all([True for sample in wrong_samples if validator.validate(sample) is False])

        self.assertTrue(is_not_valid)
