# Python library import
import json
from typing import Tuple, Any

import dateutil.parser
import datetime

# Project modules
from config.utils import get_project_config
from utils.validators import VALIDATOR_MAPPING, VALIDATOR_MESSAGE_TYPES
from utils.tools import DateTimeDecoder

# Logging section
import logging
logger = logging.getLogger(__name__)

# Project configuration
CONFIG = get_project_config()

# Currently, allow only strings to be normalized
ALLOWED_OBJECT_TYPES = (str, dict, bytes)


class DefaultNormalizer:
    """
        Class DefaultNormalizer

        Transforms serialized object into Python-comparable JSON object and check the validity of JSON scheme.

        Definitions
        =====
        In Python a JSON object is presented as dictionary, so, let me call this as **JSON Python dictionary**
    """

    def __init__(self):

        self._object_validators = {}

    @classmethod
    def _try_cast(cls, cast_object: Any) -> Tuple[dict, bool]:

        """
            Try to transform *cast_object* into JSON Python dictionary.

            There different ways a *cast_object* can be transformed. It is supposed the most trivial one is
            from *str* to *dict*.

            If *cast_object* can be transformed, then it returns the tuple (dict, True).
            If transformation is not possible, then it returns the tuple ({}, False).


        :param cast_object: an object to be casted to JSON Python dictionary.
        :return: a tuple {des_obj, True} where des_obj is deserialized object, ({}, False) otherwise
        """

        # Check if 'cast_object' is already dict
        if isinstance(cast_object, dict):
            return cast_object, True

        # Check if the object has the allowed type to be casted
        if not any(isinstance(cast_object, _type) for _type in ALLOWED_OBJECT_TYPES):
            return {}, False

        # Check if the object is bytes, then try transform it into string
        if isinstance(cast_object, bytes):

            try:
                cast_object = cast_object.decode()
            except UnicodeDecodeError:
                return {}, False

        # Try to deserialize JSON string into dict
        try:
            _casted_obj = json.loads(cast_object, cls=DateTimeDecoder)
        except json.JSONDecodeError:
            return {}, False
        else:
            return _casted_obj, True

    def normalize(self, _object: Any) -> Any:

        """
            Cast _object into JSON, check field types and apply an appropriate Validator to check the scheme
            correctness. If it went without any error, the normalized object is returned back.

        :param _object: a JSON-deserializable object.
        :return: dict if *norm_object* can be transformed into JSON with a valid JSON schema, None otherwise.
        """

        # try to deserialize the _object
        casted_dict, is_success = self._try_cast(_object)

        # check if the result is successful
        if not is_success:
            return None

        # Find message_type
        message_type = casted_dict.get("message_type", None)

        # Check if we have a validator for the type
        if message_type not in VALIDATOR_MESSAGE_TYPES:
            return None
        else:
            _validator_class = VALIDATOR_MAPPING[message_type]

        # Cast time field
        time = casted_dict['time']

        if isinstance(time, int):
            time = datetime.datetime.fromtimestamp(casted_dict['time'] / 1e3)
        elif isinstance(time, str):
            time = dateutil.parser.parse(time)

        casted_dict['time'] = time

        # Validate the object
        validator = _validator_class()
        _is_valid = validator.validate(casted_dict)

        if not _is_valid:
            return None
        else:
            return casted_dict
