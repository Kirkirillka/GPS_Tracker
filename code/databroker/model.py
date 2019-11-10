import json
import logging

from typing import List, Callable, Tuple, Any, Mapping

from utils.validators import VALIDATOR_MAPPING, VALIDATOR_MESSAGE_TYPES
from brokeradapter.model import BrokerAdapter
from config.utils import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()




class DataBroker:
    """ Class DataBroker

        This class is for processing raw messages from MQTT Message Broker Server and save them in Storage.
    """

    _topics = [
        "/clients",
        "wifi/#",
    ]

    def __init__(self):

        self._broker_adapter = BrokerAdapter()
        self._store_adapter = None
        self._normalizer = Normalizer()

        self._is_initialized = False

    def set_callback_func(self, topic: str, callback: Callable) -> bool:

        """
            set_callback_func allow to set manually a callback for the specific topic.
            Must be executed before .setup() is done
        :param topic: a topic name
        :param callback: a Callable object which takes 3 parameters
        :return: True if topic was set successfully, False otherwise
        """

        # Try to set topic
        res = self._broker_adapter.add_topic(topic, callback, force=True)

        return res

    def get_callback_func(self, topic: str) -> Callable:

        """
            Return callback function
        :param topic: a topic to create a callback on
        :return: function
        """

        def _default_callback(client_id: str, userdata: Any, message: Any) -> Any:
            """
                A function used as callback for every message received in the specified topics list. Has quite strict
                parameter signature.
            :param client_id: An client ID.
            :param userdata: ?
            :param message: Message sent in the topic. It has topic name, payload.
            :return: None
            """

            logging.debug("Entered in callback function")
            logging.debug(f"Can access self argument {self}", )
            logging.debug(f"ClientID: {client_id}")
            logging.debug(f"Userdata: {userdata}")
            logging.debug(f"Message: {message}")

        def _disconnect_callback(*args, **kwargs):
            # Force disconnect
            self._broker_adapter.stop()

        # Store mapping between topic names and corresponding callbacks
        callback_mapping = {
            "disconnect": _disconnect_callback
        }

        # return a callback by key, otherwise return the default callback
        return callback_mapping.get(topic, _default_callback)

    def initialize(self) -> bool:

        """
            Establish connection with Storage.
            Instruct BrokerAdapter to establish connection with MQTT,
            add all topics and its callback function to BrokerAdapter.
        :return: True if initialization is completed
        """

        # Step 1. Establish connection with Storage
        # //TODO: implement StorageAdapter
        logger.debug("Initialization StorageAdapter connection.")
        self._store_adapter = None

        # Step 2. Add topics and callback functions
        for topic in self._topics:
            _callback = self.get_callback_func(topic)
            self._broker_adapter.add_topic(topic, _callback)

        # Step 3. Ask BrokerAdapter to make subscriptions
        setup_res = self._broker_adapter.setup()

        # Step 4. Set itself as initialized instance
        if setup_res:
            self._is_initialized = True
        else:
            self._is_initialized = False

        # Finish
        return setup_res

    def run_loop(self):

        """
            Starts pooling MQTT server with BrokerAdapter. Internally, executes _broker_adapter serve function. You
            can stop polling with your callback function and invoke stop() on _broker_adapter.

            run_loop() is a blocking function.

        :return: True if loop is over, False if error occurred
        """

        # Check if .setup() first was executed
        if not self._is_initialized:
            return False

        # run client forever looping
        res = self._broker_adapter.serve()

        return res


class Normalizer:
    """
        Class Normalizer

        Transforms serialized object into Python-comparable JSON object and check the validity of JSON scheme.
    """

    # Currently, allow only strings to be normalized
    ALLOWED_OBJECT_TYPES = (str, dict, bytes)

    def __init__(self):

        self._object_validators = {}

    def _try_cast(self, cast_object: Any) -> Tuple[dict, bool]:

        """
            Try to first transform cast_object into JSON  object.
            If cast_object can be transform, then it returns {dict, True}.
            If transformation is not possible, then it returns tuple ({}, False).


        :param cast_object: a string of serialized JSON object
        :return: a tuple {des_obj, True} where des_obj is deserialized object, ({}, False) otherwise
        """

        # Check if 'cast_object' is already dict
        if isinstance(cast_object, dict):
            return cast_object, True

        # Check if the object has the allowed type to be casted
        if not any(isinstance(cast_object, _type) for _type in self.ALLOWED_OBJECT_TYPES):
            return {}, False

        # Check if the object is bytes, then try transform it into string
        if isinstance(cast_object, bytes):

            try:
                cast_object = cast_object.decode()
            except UnicodeDecodeError as e:
                return {}, False

        # Try to deserialize JSON string into dict
        try:
            _casted_obj = json.loads(cast_object)
        except json.JSONDecodeError as e:
            return {}, False
        else:
            return _casted_obj, True

    def normalize(self, _object: Any) -> Mapping[dict, None]:

        """
            Cast _object into JSON, check the type field and apply the appropriate Validator to check the scheme
            correctness. If ll went without error, the normalized object is returned back.

        :param _object: a JSON-deserializable object
        :return: dict if norm_object can be trasnformed into JSON with a valid JSON schema, None otherwise
        """

        # try to deserialize the _object
        _deser_dict, is_success = self._try_cast(_object)

        # check if the result is successful
        if not is_success:
            return None

        # Find message_type
        message_type = _deser_dict.get("message_type", None)

        # Check if we have a validator for the type
        if message_type not in VALIDATOR_MESSAGE_TYPES:
            return None
        else:
            _validator_class = VALIDATOR_MAPPING[message_type]

        # Validate the object
        validator = _validator_class()
        _is_valid = validator.validate(_deser_dict)

        if _is_valid:
            return _deser_dict
        else:
            return None
