# Python library import
import json
from abc import ABC, abstractmethod
from typing import Mapping

# 3-td party libraries
from deepdiff import DeepDiff
from jsonschema import Draft7Validator

# Project modules
from utils.tools import read_schema_from_file


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
    def get_schema(self):
        """
            Returns a class or description of how a valid schema should like
        :return: object
        """
        pass


class JSONValidator(AbstractValidator):
    """
        Validate an provided object to be a valid JSON Schema based object.

        Can use any JSON schema provided in file.
        When instantiating an object, provde a path to JSON Schema file

        > # Default behavior
        > validator = JSONValidator()
        >
        > other_validator = JSONValidator("gps_schema.json")


    """

    def __init__(self, schema: dict):
        """

        :param schema: a filepath to a JSON Schema stored in a file or a dict object containing JSON Schema
        """

        if isinstance(schema, dict):
            _schema = schema
        else:
            raise TypeError("A provided schema is not a dict object!")
        # Use already existing JSON validator
        self.internal_validator = Draft7Validator(_schema)

    def get_schema(self):

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

            try:
                normalized_sample = json.loads(sample)
            except Exception as e:
                raise ValueError("A supplied string is not a valid JSON object") from e

            sample = normalized_sample

        # check if we supplied with a dict or a sample was normalized
        if not isinstance(sample, dict):
            raise ValueError(f"A supplied object type '{type(sample)}' cannot be converted into JSON")

        # Ask a JSON Schema checker implementation to check if it is valid
        decision = self.internal_validator.is_valid(sample)

        return decision


class RawPayloadValidator(JSONValidator):
    SCHEMA_FILENAME = "raw_payload_schema.json"

    def __init__(self):
        _schema = read_schema_from_file(self.SCHEMA_FILENAME)

        super(RawPayloadValidator, self).__init__(_schema)


class WIFIPayloadValidator(JSONValidator):
    SCHEMA_FILENAME = "wifi_payload_schema.json"

    def __init__(self):
        _schema = read_schema_from_file(self.SCHEMA_FILENAME)

        super(WIFIPayloadValidator, self).__init__(_schema)


# Sets which validator to use on "message_type"
# message_type is supposed to be included in tuple VALIDATOR_MESSAGE_TYPES

VALIDATOR_MAPPING = {
    "raw": RawPayloadValidator,
    "wifi": WIFIPayloadValidator
}

# Sets which message types are allowed to be processed
VALIDATOR_MESSAGE_TYPES = ["raw", "wifi"]
