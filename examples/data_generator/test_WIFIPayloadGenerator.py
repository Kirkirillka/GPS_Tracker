from test_JSONGenerator import TestJSONGenerator

from validators import WIFIPayloadValidator
from generators import WIFIPayloadGenerator

from utilities import read_schema_from_file


class TestWIFIPayloadGenerator(TestJSONGenerator):

    @classmethod
    def setUpClass(cls) -> None:
        cls.JSON_SCHEMA_PATH = "wifi_payload_schema.json"

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("wifi_payload_schema.json")
        self.validator = WIFIPayloadValidator()
        self.generator = WIFIPayloadGenerator()