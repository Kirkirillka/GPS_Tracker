from abc import ABC, abstractmethod


from validators import  JSONValidator
from field_gens import gen_empty_sample_packet


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


class JSONGenerator(AbstractGenerator):

    """
        JSONGenerator is meant to use in case of testing or absence of real devices(Android, UAV) to generate
        valid JSON payload to be sent to ClientBroker
    """

    def __init__(self):

        self._validator = JSONValidator()

    def get(self):

        if hasattr(self,"get_with_payload"):

            # Not implemented yet
            # //TODO add implementation to generate packet with payload

            pass

        else:

            # If not implemented, then return a sample without payload
            return self.get_empty()

    def _get_empty(self):
        """
            Return a sample with in valid JSON schema, but without any payload
        :return: dict
        """

        empty_sample = gen_empty_sample_packet()

        return empty_sample
