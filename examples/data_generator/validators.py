from abc import ABC, abstractmethod
from typing import  Mapping

import json
from json.decoder import JSONDecodeError

from deepdiff import DeepDiff
from jsonschema import Draft7Validator


class AbstractValidator(ABC):

    """
        AbstractValidator class contains naming for methods as a validator, which is used to check the validity of data
        provided by GPS devices.

        All real Validators (JSONValidator, ProtobufValidator, etc.) must inherit from this abstract class
    """

    @abstractmethod
    def validate(self, sample):
        """
            Returns True if a sample is the provided data structure is in valid scheme
        :return: book
        """
        pass

    @abstractmethod
    def get_valid_schema(self):
        """
            Returns a class or description of how a valid schema should like
        :return: object
        """
        pass


class JSONValidator(AbstractValidator):

    """
        Validate an provided object to be a valid JSON Schema based object.

        Can use any JSON schema provided in file.
        When instantiating an object, provde a path to JSON Schema file (default is "valid_schema.json",
        that default for payload empty sample)

        > # Default behavior
        > validator = JSONValidator()
        >
        > other_validator = JSONValidator("gps_schema.json")


    """

    def __init__(self, schema_filepath="valid_schema.json"):
        """

        :param schema_filepath: a filepath to a JSON Schema stored in a file
        """
        _schema = self._read_schema_from_file(schema_filepath)
        # Use already existing JSON validator
        self.internal_validator = Draft7Validator(_schema)

    @staticmethod
    def _read_schema_from_file(schema_filepath):

        """
            Reads a schema from provided file to JSON schema

        :exception IOError:
            Raise IOError if a file with scheme is not found
        :return: dict
        """

        try:
            with open(schema_filepath) as file:
                schema = json.load(file)

        except IOError as e:
            raise FileNotFoundError("A file with schema is not found!")
        except JSONDecodeError as e:
            raise e

        return schema

    def get_valid_schema(self):

        """
            Returns the scheme provided at initialization
        :return: dict
        """

        # Simple pass through to internal validator
        return self.internal_validator.schema

    def compare_schema(self, schema: dict):

        """
            Returns if the provided schema is the same as used in the current JSON validator
        :param schema: dict
            suggested schema
        :return: bool
            True if the schema is identical, False otherwise
        """

        internal_schema = self.internal_validator.schema
        decision = True if not DeepDiff(internal_schema, schema) else False

        return decision

    def validate(self, sample: Mapping[str, dict]):

        # check if we supplied with a string
        if isinstance(sample, str):

            normalized_sample = None

            try:
                normalized_sample = json.loads(sample)
            except Exception as e:
                raise ValueError("A supplied string is not a valid JSON object")

            sample = normalized_sample

        # check if we supplied with a dict or a sample was normalized
        if not isinstance(sample, dict):
            raise ValueError(f"A supplied object {type(sample)} cannot be converted into JSON")

        # Ask a JSON Schema checker implementation to check if it is valid
        decision = self.internal_validator.is_valid(sample)

        return decision




