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


def time_gen():

    """
        generate value for "time" field
    :return:
    """

    return str(datetime.datetime.now().isoformat())


def device_type_gen():

    available_types = ["handy", "UAV"]

    return random.choice(available_types)


def device_id_gen():

    return str(uuid.uuid4())


def longitude_gen():

    base_longitude = 50.6806218

    offset = random.gauss(1,2)
    radians = random.randint(0,360) * math.pi / 180

    return str(base_longitude + offset * math.cos(radians))


def latitude_gen():

    base_latitude = 10.9324852

    offset = random.gauss(1, 2)
    radians = random.randint(0, 360) * math.pi / 180

    return str(base_latitude + offset * math.sin(radians))

def empty_payload_gen():

    return []


fields_mapping = {
    "time": time_gen,
    "device.id" : device_id_gen,
    "device.device_type": device_type_gen,
    "longitude": longitude_gen,
    "latitude": latitude_gen,
    "payload": empty_payload_gen
}


def gen_empty_sample_packet():

    """
        Generates an empty telemetry message with clean payload.
    :return:
    """

    target = {}

    # for each field
    for key, function in fields_mapping.items():

        # deep field creation phase
        # https://stackoverflow.com/questions/26226056/generic-way-to-create-nested-dictionary-from-flat-dictionary-in-python

        components = key.split(".")
        value = function()

        subtarget = target

        for component in components[:-1]:
            subtarget = subtarget.setdefault(component, dict())
        subtarget[components[-1]] = value


    return target