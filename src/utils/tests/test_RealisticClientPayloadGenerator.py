from utils.tests.test_JSONGenerator import TestJSONGenerator


from utils.validators import WIFIPayloadValidator
from utils.generators import RealisticClientPayloadGenerator

from utils.tools import read_schema_from_file


class TestRealisticClientPayloadGenerator(TestJSONGenerator):

    @classmethod
    def setUpClass(cls) -> None:
        cls.JSON_SCHEMA_PATH = "wifi_payload_schema.json"

    def setUp(self) -> None:

        self.json_schema = read_schema_from_file("wifi_payload_schema.json")
        self.validator = WIFIPayloadValidator()
        self.generator = RealisticClientPayloadGenerator()