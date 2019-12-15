"""
This file contains a little functions for all fields which can occur in valid scheme.

The snippet functions are mapped into a dictionary, which is used to find how to generate a specific field in *get*
method in JSONGenerator
"""

import datetime
import random
import uuid
import math

random.seed()


#
# Field generators for Raw Empty sample
#
def time_gen():
    """
        generate value for "time" field
    :return:
    """

    return str(datetime.datetime.now().isoformat())


def raw_payload_message_gen():
    return "raw"


def wifi_payload_message_gen():
    return "wifi"


def device_type_gen():
    available_types = ["handy"]

    return random.choice(available_types)


def device_id_gen(use_uuid=False):
    PREDEFINED_UID = [
        "021e4c97-f61a-4983-82b5-a7b4d7bd6b97",
        "68ffd193-ca72-4990-ad10-9ee0f4d2e0bf",
        "7f85b2bb-f93c-4e6e-9403-bcf86cf08d94",
        "319e666a-c85d-40d9-8e66-94192f34afa9",
        "6c0273ce-443b-470b-aadb-7300e558761d",
        "eb1a5132-f764-4ed6-a8dc-af2c40deb5a5",
        "38330305-c27b-46f0-a493-7d1b514ee6bd",
        "9e9f1f3d-6523-4492-b60f-ef09b8a5c6b0",
        "a7191008-a177-4eff-b20d-bef3aea603d8",
        "e6a4fac6-ebfd-4792-8dc2-8a5eed013d86",
        "b4a44df7-6aad-4bf5-b423-db33bcaeeb8a",
        "c9dff19e-c344-4cb1-a33f-e21ce1b00a15",
        "68eaec53-9451-4e2d-8255-4928bb73d82f",
    ]

    if use_uuid:
        return str(uuid.uuid4())
    else:
        return random.choice(PREDEFINED_UID)


def longitude_gen():
    base_longitude = 10.9324852

    offset = random.gauss(1, 2)
    radians = random.randint(0, 360) * math.pi / 180

    return base_longitude + offset * math.cos(radians)


def latitude_gen():
    base_latitude = 50.6806218

    offset = random.gauss(1, 2)
    radians = random.randint(0, 360) * math.pi / 180

    return base_latitude + offset * math.sin(radians)


#
# Generators for WiFi status fields
#

def wifi_info_type_gen():
    choices = ["wifi"]

    return random.choice(choices)


def wifi_info_ssid_gen():
    number_of_aps = 10
    ap_name_template = "AP #{}"

    ap_number = random.randint(1, number_of_aps)

    return ap_name_template.format(ap_number)


def wifi_info_bssid_gen():
    mac_manufacturer_prefix = "02:00:00:"

    # https://stackoverflow.com/questions/8484877/mac-address-generator-in-python

    postfix = "%02x:%02x:%02x" % (random.randint(0, 255),
                                  random.randint(0, 255),
                                  random.randint(0, 255))

    return mac_manufacturer_prefix + postfix


def wifi_info_signal_rssi_gen():
    min_signal = -100
    max_signal = -20

    return random.randint(min_signal, max_signal)


#
# Generating payload
#


def empty_payload_gen():
    return {}


# Utilities
#

def generate_dict_by_mapping(field_map: dict):
    """
        Generates an empty dictionary, based on mapping, provided in a way

        {
            "field1": function_to_generate1,
            "field2": function_to_generate2,
            "nested.field1": func3,
            "more.deep.field": func4
        }

    :param field_map: dict
        A Dict based mapping between a field and a function to generate the value for that field
    :return: dict
    """

    target = {}

    # for each field
    for key, function in field_map.items():

        # deep field creation phase
        # https://stackoverflow.com/questions/26226056/generic-way-to-create-nested-dictionary-from-flat-dictionary-in-python

        components = key.split(".")
        value = function()

        subtarget = target

        for component in components[:-1]:
            subtarget = subtarget.setdefault(component, dict())
        subtarget[components[-1]] = value

    return target


# A dump mapping to test if our JSONGenerator and JSONParser works correctly
DUMP_PAYLOAD_FIELDS_TEMPLATE = {
    "firstName": lambda: "John",
    "lastName": lambda: 'Doe',
    "age": lambda: 1
}

# A field mapping to create a new schema-valid JSON message, but without payload
RAW_PAYLOAD_FIELDS_TEMPLATE = {
    "time": time_gen,
    "message_type": raw_payload_message_gen,
    "device.id": device_id_gen,
    "device.device_type": device_type_gen,
    "longitude": longitude_gen,
    "latitude": latitude_gen,
    "payload": empty_payload_gen
}

# A field mapping to create payload for Cellular Network status message
# //TODO: find information about what information can be taken from Android and sent in this CellularNetwork payload
CELLULAR_PAYLOAD_FIELDS_TEMPLATE = {

}

# A field mapping to create payload for Wifi status message
# //TODO: reformat field generator to create a structure like:
#   {
#        "time" : time_gen,
#        "field1" : {
#               "subfield2": gen1,
#               "subfield3": {
#                   "subfield4": gen2
#              }
#         }
#   }
#
#

# //TODO: find information about what information can be taken from Android and sent in this Wifi payload
WIFI_PAYLOAD_FIELDS_TEMPLATE = {
    "ssid": wifi_info_ssid_gen,
    "bssid": wifi_info_bssid_gen,
    "signal.rssi": wifi_info_signal_rssi_gen
}
