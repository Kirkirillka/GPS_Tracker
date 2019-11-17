# Python library import
import numpy as np
from abc import ABC, abstractmethod

# Project modules
from utils.field_gens import *


class AbstractGenerator(ABC):
    """
    Abstract class to describe methods for a generator.

    An abstract generator must allow:

    - fetching one valid data sample
    - be used as an iterator

    """

    @abstractmethod
    def get(self):
        """
        Generates one sample of valid data

        :return: dict
        """
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass


class JSONGenerator(AbstractGenerator):
    """
        Class JSONGenerator implements method to generate a JSON file from field mapping.
    """

    def __init__(self, field_mapping: dict):
        self._map = field_mapping

    def get(self):
        """
            Return one sample in valid JSON Schema
        :return: dict
        """

        # Take a new sample
        sample = generate_dict_by_mapping(self._map)

        return sample

    def __iter__(self):
        return self

    def __next__(self):
        """
            Interface for iterating

            WARNING! There is not limits in iterations, so if you intentionally not set limits
            to take from this iterator, then it will loop infinitely

        :return: dict
        """
        # Return a sample
        return self.get()


class RawPayloadGenerator(JSONGenerator):
    """
        Class EmptySampleGenerator generates samples with GPS positions, but without any payload.
    """

    FIELD_MAP = RAW_PAYLOAD_FIELDS_TEMPLATE

    def __init__(self):
        # Initialize JSON Generator to generate an empty sample
        super(RawPayloadGenerator, self).__init__(RAW_PAYLOAD_FIELDS_TEMPLATE)

    def get(self):
        # Don't add any other logic, just pass through default JSONGenerator and empty field mapping
        return super(RawPayloadGenerator, self).get()


class WIFIPayloadGenerator(RawPayloadGenerator):
    """
        Class WifiInfoGenerator returns a sample with GPS coordinates and Wifi connection status in this area.

        This works in two steps:

        - First, get an sample without payload from EmptySampleGenerator
        - Generate a WIFI payload using **WIFI_PAYLOAD_FIELDS_TEMPLATE** filed mapping
        - Update a "payload" array, insert into empty body message
    """

    FIELD_MAP = WIFI_PAYLOAD_FIELDS_TEMPLATE

    def __init__(self):
        # Initialize JSON Generator to generate an empty sample

        super(WIFIPayloadGenerator, self).__init__()

        self.wifi_payload_generator = JSONGenerator(WIFI_PAYLOAD_FIELDS_TEMPLATE)

    def get(self):
        # Generate empty body
        body = super(WIFIPayloadGenerator, self).get()

        # Generate WIFI status payload
        wifi = self.wifi_payload_generator.get()

        # Set payload type
        body["message_type"] = wifi_payload_message_gen()

        # Update payload in main message
        body['payload'] = wifi

        return body


class RealisticClientPayloadGenerator(WIFIPayloadGenerator):

    def __init__(self):
        super(RealisticClientPayloadGenerator, self).__init__()

        self.uuid = device_id_gen(use_uuid=True)
        self.ssid = wifi_info_ssid_gen()

        amount = 100

        self.base_longitude = longitude_gen()
        self.base_latitude = latitude_gen()

        offset = np.random.normal(2, 5)

        self._x_plane = np.linspace(-1 - offset, 1 + offset, amount)
        self._y_plane = np.linspace(-1 - offset, 1 + offset, amount)
        self._radius = 20

    def _get_signal(self, x, y):
        return - (y ** 2 + x ** 2 + self._radius)

    def get(self):
        _x = np.random.choice(self._x_plane)
        _y = np.random.choice(self._y_plane)

        latitude = _x + float(self.base_latitude)
        longitude = _y + float(self.base_longitude)

        signal_quality = self._get_signal(_x, _y)

        dump_wifi_payload = super(RealisticClientPayloadGenerator, self).get()

        dump_wifi_payload["device"]["id"] = self.uuid
        dump_wifi_payload['longitude'] = str(longitude)
        dump_wifi_payload['latitude'] = str(latitude)
        dump_wifi_payload["payload"]["ssid"] = self.ssid
        dump_wifi_payload["payload"]["signal"]["rssi"] = signal_quality

        return dump_wifi_payload
