# Python library import
import numpy as np
from abc import ABC, abstractmethod
from typing import Any

# Project modules
from utils.field_gens import *


class AbstractGenerator(ABC):
    """
    Abstract class to describe methods for a generator.

    An abstract generator must allow:

    - fetching one valid data sample
    - be used as an iterator

    """

    field_map = {}

    @abstractmethod
    def get(self) -> Any:
        """
        Generates one sample of valid data

        :return: dict
        """
        pass

    @abstractmethod
    def __iter__(self) -> Any:
        pass

    @abstractmethod
    def __next__(self) -> Any:
        pass


class JSONGenerator(AbstractGenerator):
    """
        Class JSONGenerator implements method to generate a JSON file from field mapping.
    """

    def __init__(self, field_mapping: dict):
        self.field_map = field_mapping

    def get(self) -> dict:
        """
            Return one sample in valid JSON Schema
        :return: dict
        """

        # Take a new sample
        sample = generate_dict_by_mapping(self.field_map)

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


class RawPayloadGenerator(AbstractGenerator):
    """
        Class EmptySampleGenerator generates samples with GPS positions, but without any payload.
    """

    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        return self.get()

    def __init__(self):
        self.field_map = RAW_PAYLOAD_FIELDS_TEMPLATE
        # Initialize JSON Generator to generate an empty sample
        self._empty_body_generator = JSONGenerator(self.field_map)

    def get(self):
        # Don't add any other logic, just pass through default JSONGenerator and empty field mapping
        return self._empty_body_generator.get()


class WIFIPayloadGenerator(AbstractGenerator):
    """
        Class WifiInfoGenerator returns a sample with GPS coordinates and Wifi connection status in this area.

        This works in two steps:

        - First, get an sample without payload from EmptySampleGenerator
        - Generate a WIFI payload using **WIFI_PAYLOAD_FIELDS_TEMPLATE** filed mapping
        - Update a "payload" array, insert into empty body message
    """

    def __iter__(self) -> Any:
        return self

    def __next__(self) -> Any:
        return self.get()

    def __init__(self):

        self.field_map = WIFI_PAYLOAD_FIELDS_TEMPLATE

        self._body_generator = RawPayloadGenerator()
        self._payload_generator = JSONGenerator(self.field_map)

    def get(self):
        # Generate empty body
        body = self._body_generator.get()

        # Generate WIFI status payload
        wifi = self._payload_generator.get()

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
        dump_wifi_payload['longitude'] = float(longitude)
        dump_wifi_payload['latitude'] = float(latitude)
        dump_wifi_payload["payload"]["ssid"] = self.ssid
        dump_wifi_payload["payload"]["signal"]["rssi"] = signal_quality

        return dump_wifi_payload
