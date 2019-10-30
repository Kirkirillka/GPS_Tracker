from abc import ABC, abstractmethod


from validators import  JSONValidator
from field_gens import generate_dict_by_mapping


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
        JSONGenerator is meant to use in case of testing or absence of real devices(Android, UAV) to generate
        valid JSON payload to be sent to ClientBroker
    """

    def __init__(self, field_mapping: dict):

        self._map = field_mapping
        self._validator = JSONValidator()
        self._num = 0

    def get(self):

        """
            Return one sample in valid JSON Schema
        :return: dict
        """

        if hasattr(self,"get_with_payload"):

            # Not implemented yet
            # //TODO add implementation to generate packet with payload

            pass

        else:

            # If not implemented, then return a sample without payload
            return self._get_empty()

    def _get_empty(self):
        """
            Return a sample with in valid JSON schema, but without any payload
        :return: dict
        """

        # Take a new sample
        empty_sample = generate_dict_by_mapping(self._map)

        # Increase counter
        self._num += 1

        return empty_sample

    def __iter__(self):
        return self

    def __next__(self):

        """
            Interface for iterating

            WARNING! There is not limits in iterations, so if you intentionally not set limits
            to take from this iterator, then it will loop infinitely

        :return: dict
        """

        # Increase counter
        self._num += 1

        # Return a sample
        return self.get()