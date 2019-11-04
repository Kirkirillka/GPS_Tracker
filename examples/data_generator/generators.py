from abc import ABC, abstractmethod

from field_gens import generate_dict_by_mapping, RAW_PAYLOAD_FIELDS_TEMPLATE, WIFI_PAYLOAD_FIELDS_TEMPLATE


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
        self.empty_body_generator = JSONGenerator(RAW_PAYLOAD_FIELDS_TEMPLATE)

    def get(self):
        # Don't add any other logic, just pass through default JSONGenerator and empty field mapping
        return self.empty_body_generator.get()


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
        self.empty_body_generator = JSONGenerator(RAW_PAYLOAD_FIELDS_TEMPLATE)
        self.wifi_payload_generator = JSONGenerator(WIFI_PAYLOAD_FIELDS_TEMPLATE)

    def get(self):
        # Generate empty body
        body = self.empty_body_generator.get()

        # Generate WIFI status payload
        wifi = self.wifi_payload_generator.get()

        # Update payload in main message
        body['payload'] = wifi

        return body
