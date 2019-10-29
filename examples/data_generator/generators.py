from abc import ABC, abstractmethod


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



