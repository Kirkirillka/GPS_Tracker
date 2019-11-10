import paho
import json
import logging

import paho.mqtt.client as mqtt

from typing import List, Callable, Tuple, Any, Mapping

from utils.validators import VALIDATOR_MAPPING, VALIDATOR_MESSAGE_TYPES

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class BrokerAdapter:
    """
        Class **BrokerAdapter** is responsible for providing an interface to fetch data from MQTT Message broker and
            pass data to DataBroker.
    """

    def __init__(self):

        """
            1. _conn - a real connection to MQTT broker
            2. _topics - a list of topics BrokerAdapter will be listening to
        """

        # Initialize MQTT Client object
        self._conn: paho.mqtt.client.Client = mqtt.Client()
        self._topics: dict = {}

        self._host = "localhost"

        self._is_initialized = False

    def _connect(self) -> bool:

        """
            Initialize connection to MQTT Message Broker server
        :return: True if connection was established successfully, otherwise raise ConnectionError
        :raise: ConnectionError if connection is not established
        """

        try:
            # Connect to MQTT Message Broker
            clt = self._conn.connect(self._host)
            # Enable action logging
            self._conn.enable_logger(logger)

        except Exception as e:
            # If some errors occurred in this stage
            return False
        else:
            # Notify that connection is successful
            return True

    def setup(self) -> bool:

        """
            Configure connection parameters and instruct a private _connect how to be executed.
            Then perform all subscriptions and callback function bindings.

            If a ConnectionError raises at _connect, it pass the exception further, so, the program may fail.

        :return: None if connection is established, pass ConnectionError from _connect otherwise
        :raise: ConnectionError
        """

        # Try to establish connection to MQTT Message broker
        con_res = self._connect()

        # Fail if cannot connect to the server
        if con_res:
            logger.info(f"Connection to MQTT Message Broker server {self._host} is established.")
        else:
            logger.error(f"Connection to MQTT Message Broker server {self._host} is not possible!")
            return False

        # Perform subscription
        for topic, callback  in self._topics.items():
            self._conn.subscribe(topic)
            self._conn.message_callback_add(topic, callback)

            logger.debug(f"Subscription on topic '{topic}' with function '{callback}' is done.")

        # Set itself as initialized instalce
        self._is_initialized = True

        return True

    def get_topics(self) -> List[str]:

        """
            Returns a list of topics which the BrokerAdapter was subscribed and listen messages from MQTT Broker.
            Internally, the list of topics is presented by _topics variable. This function should take care of
            the right formatting and checking.

        :return: A list of topics which were subscribed
        """

        return list(self._topics.keys())

    def add_topic(self, topic: str, callback: Callable[[str, str, object], None], force: bool = False) -> bool:

        """
            Perform subscription on specific **topic**. A **callback** function will be executed
            with provided parameters each time a new message is arrived on the topic.

            Steps:

                1. Execute subscribe function on MQTT connection object.
                2. Add the new topic to _topics dictionary with values {topic: callback}.

        :param topic: A string specified a topic path
        :param callback:  A function or a callable object, which takes three parameters (four in case of class methods).
        :param force: To set if rewrite an existing topic mapping
        :return: return True if subscription was made successfully.
        """
        # Check if the topic is already subscribed
        if topic in self._topics.keys():

            # Check if it's forced to rewrite the topic:callback mapping
            if force:

                logger.info(f"Rewrite callback for topic '{topic}' to callable '{callback}'")

                # Add topic into internal list
                self._topics[topic] = callback

                return True

            # Topic is already subscribed, so, it must first be unsubscribed
            return False
        else:

            logger.info(f"Added a new subscriber to  '{topic}'.")

            # Add topic into internal list
            self._topics.setdefault(topic, callback)

            return True

    def del_topic(self, topic: str) -> bool:
        """
            Exclude the specified topic to be NOT listened from MQTT Broker.
            If the specified topic is not seen to be listened in _topics, then
            topic is ignored, returns True.

            Steps:

                1. Delete subscription on the topic to MQTT Connection
                1. Delete the topic from _topics variable

        :param topic: a string specifies a topic (format : "/my/format/for/any/*")
        :return: True if unsubscription made successfully, False otherwise

        """

        # Check if there was an subscription on the topic already
        if topic in self._topics.keys():

            # Unsubscribe
            self._conn.unsubscribe(topic)

            # Delete subscription
            del self._topics[topic]

            logger.info(f"Subscription on the topic {topic} is finished.")

            return True
        else:
            return False

    def serve(self) -> int:

        """
            Run internal loop_forever function. This function is blocking, so function won't return
            until disconnect is executed on MQTT connection object
        :return: True if loop is stopped
        """

        # Check if .setup() was executed first
        if not self._is_initialized:
            logger.error("BrokerAdapter is not tuned yet. Setting up first.")

            # Setting BrokerAdapter
            self.setup()

        # Start looping
        logger.info("Start MQTT Message receiving loop pooling.")
        res = self._conn.loop_forever()

        # Loop is over
        logger.info("Loop is over, exiting...")
        return res

    def stop(self) -> int:
        """
            Stop message pooling
        :return: True if BrokerAdapter stopped successfully.
        """

        res = self._conn.disconnect()

        return res


class DataBroker:

    """ Class DataBroker

        This class is for processing raw messages from MQTT Message Broker Server and save them in Storage.
    """

    _topics = [
        "/clients",
        "wifi/#",
    ]

    def __init__(self):

        self._broker_adapter =  BrokerAdapter()
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

        return  res

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
            logging.debug(f"Can access self argument {self}",)
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
        self._is_initialized = True

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
    ALLOWED_OBJECT_TYPES = (str,dict, bytes)

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
            return  None
        else:
            _validator_class = VALIDATOR_MAPPING[message_type]



        # Validate the object
        validator = _validator_class()
        _is_valid = validator.validate(_deser_dict)

        if _is_valid:
            return _deser_dict
        else:
            return None


