from abc import ABC, abstractmethod


class AbstractValidator(ABC):

    """
        AbstractValidator class contains naming for methods as a validator, which is used to check the validity of data
        provided by GPS devices.

        All real Validators (JSONValidator, ProtobufValidator, etc.) must inherit from this abstract class
    """

    @abstractmethod
    def validate(self, sample):
        """
            Returns True if a sample is the provided data structure is in valid scheme
        :return: book
        """
        pass

    @abstractmethod
    def get_valid_schema(self):
        """
            Returns a class or description of how a valid schema should like
        :return: object
        """
        pass
