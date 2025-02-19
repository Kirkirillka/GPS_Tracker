import json

from utils.generators import RawPayloadGenerator, WIFIPayloadGenerator
from utils.tools import DateTimeEncoder


def get_correct_data_with_wrong_scheme() -> str:

    test_tuple = {
        "field1": 123,
        "field2": [1,2,3,4]
    }

    return json.dumps(test_tuple)


def get_correct_data_with_correct_scheme() -> str:

    gens = RawPayloadGenerator(), WIFIPayloadGenerator()
    obj_list_len = 10
    obj_list = [ r.get() for r in gens for _  in range(obj_list_len)]

    for _obj in obj_list:

        yield json.dumps(_obj, cls=DateTimeEncoder)

