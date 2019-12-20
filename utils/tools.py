import os
import json

import datetime
from dateutil import parser


class DateTimeEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                ))
            }
        return super(DateTimeEncoder, self).default(obj)


class DateTimeDecoder(json.JSONDecoder):
    # https://gist.github.com/simonw/7000493

    def __init__(self, *args, **kwargs):
        super(DateTimeDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)


    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'datetime':
            return parser.parse(obj['value'])
        return obj


def datetime_parse(date):

    if isinstance(date, str):
        return parser.parse(date)
    if isinstance(date, datetime.datetime):
        return date

    raise ValueError(f"Cannot parse the object {date}")


def read_payload_from_file(payload_filename):

    try:
        module_path = os.path.dirname(os.path.abspath(__file__))
        payload_path = os.path.join(module_path,"payloads")
        abs_path = os.path.join(payload_path,payload_filename)
        with open(abs_path) as file:
            payload = json.load(file)

    except IOError as e:
        raise FileNotFoundError("A file with schema is not found!")
    except json.JSONDecodeError as e:
        raise e

    return payload


def read_schema_from_file(schema_filename):
    """
        Reads a schema from provided file to JSON schema

    :exception IOError:
        Raise IOError if a file with scheme is not found
    :return: dict
    """

    try:
        module_path = os.path.dirname(os.path.abspath(__file__))
        scheme_path = os.path.join(module_path, "schemas")
        abs_path = os.path.join(scheme_path, schema_filename)
        with open(abs_path) as file:
            schema = json.load(file)

    except IOError as e:
        raise FileNotFoundError("A file with schema is not found!")
    except json.JSONDecodeError as e:
        raise e

    return schema


def get_dump_schema():
    _schema_name = "dump_payload_schema.json"

    return read_schema_from_file(_schema_name)


def get_raw_payload_schema():
    _schema_name = "raw_payload_schema.json"

    return read_schema_from_file(_schema_name)


def get_wifi_payload_schema():
    _schema_name = "wifi_payload_schema.json"

    return read_schema_from_file(_schema_name)


def convert_to_str(obj):
    if isinstance(obj, str):
        return obj

    if isinstance(obj, dict):
        return json.dumps(obj)

    raise NotImplementedError
