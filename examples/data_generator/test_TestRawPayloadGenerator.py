from test_JSONGenerator import TestJSONGenerator

from validators import RawPayloadValidator
from generators import RawPayloadGenerator

from utilities import read_schema_from_file

class TestRawPayloadGenerator(TestJSONGenerator):

    ITERATION_LENGTH: 30

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("raw_payload_schema.json")
        self.validator = RawPayloadValidator()
        self.generator = RawPayloadGenerator()