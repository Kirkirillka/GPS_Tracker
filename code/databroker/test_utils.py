import json


def get_correct_data_with_wrong_scheme() -> str:

    test_tuple = {
        "field1": 123,
        "field2": [1,2,3,4]
    }

    return json.dumps(test_tuple)


def get_correct_data_with_correct_scheme() -> str:

    pass