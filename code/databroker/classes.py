import paho
import json
import logging

from typing import List, Callable, Tuple, Any, Mapping

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

        self._conn = None
        self._topics = {}

    def _connect(self) -> bool:

        """
            Initialize connection to MQTT Message Broker server
        :return: True if connection was established successfully, otherwise raise ConnectionError
        :raise: ConnectionError if connection is not established
        """

        raise NotImplementedError

    def setup(self) -> None:

        """
            Configure connection parameters and instruct a private _connect how to be executed.
            Then perform all subscriptions and callback function bindings.

            If a ConnectionError raises at _connect, it pass the exception further, so, the program may fail.

        :return: None if connection is established, pass ConnectionError from _connect otherwise
        :raise: ConnectionError
        """

        raise NotImplementedError

    def get_topics(self) -> List[str]:

        """
            Returns a list of topics which the BrokerAdapter was subscribed and listen messages from MQTT Broker.
            Internally, the list of topics is presented by _topics variable. This function should take care of
            the right formatting and checking.

        :return: A list of topics which were subscribed
        """

        raise NotImplementedError

    def add_topic(self, topic: str, callback: Callable[[str, str, object], None]) -> bool:

        """
            Perform subscription on specific **topic**. A **callback** function will be executed
            with provided parameters each time a new message is arrived on the topic.

            Steps:

                1. Execute subscribe function on MQTT connection object.
                2. Add the new topic to _topics dictionary with values {topic: callback}.

        :param topic: A string specified a topic path
        :param callback:  A function or a callable object, which takes three parameters (four in case of class methods).
        :return: return True if subscription was made successfully.
        """

        raise NotImplementedError

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

        raise NotImplementedError

    def serve(self) -> bool:

        """
            Run internal loop_forever function. This function is blocking, so function won't return
            until disconnect is executed on MQTT connection object
        :return: True if loop is stopped
        """

        raise NotImplementedError


class DataBroker:

    """ Class DataBroker

        This class is for processing raw messages from MQTT Message Broker Server and save them in Storage.
    """

    def __init__(self):

        self._broker_adapter = None
        self._store_adapter = None
        self._normalizer = None

        raise NotImplementedError

    def _normalize(self, serialized_object: Any) -> dict:

        """Try to convert an object into an dict with follows a schema. The schema
         and checkers are defined in Normalizer, which actually performs all checks.

        :param serialized_object: An serializer JSON object string
        :return: The deserialized string as a dict if string was successfully converted
        :raises:
            :raise json.JSONDecodeError if the string cannot be deserialized
            :raise ValueError if the object has not valid schema
        """

        raise NotImplementedError

    def _store_message_callback(self, client_id: str, userdata: Any, message: Any) -> Any:

        """
            A function used as callback for every message received in the specified topics list. Has quite strict
            parameter signature. You can use any function as a callback function provided that it received 3 parameters.
        :param client_id: An client ID.
        :param userdata: ?
        :param message: Message sent in the topic. It has topic name, payload.
        :return: None
        """

        raise NotImplementedError

    def run_loop(self):

        """
            Starts pooling MQTT server with BrokerAdapter. Internally, executes _broker_adapter serve function. You
            can stop polling with your callback function and invoke stop() on _broker_adapter.

            run_loop() is a blocking function.

        :return: None
        """

        raise NotImplementedError


class Normalizer:

    """
        Class Normalizer

        Transforms serialized object into Python-comparable JSON object and check the validity of JSON scheme.
    """

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

        raise NotImplementedError

    def normalize(self, norm_object: Any) -> dict:

        """
            Cast norm_object into JSON, check the type field and apply the appropriate Validator to check the scheme
            correctness. If ll went without error, the normalized object is returned back.

        :param norm_object: a JSON-deserializable object
        :return: dict if norm_object can be trasnformed into JSON with a valid JSON schema, None otherwise
        """

        raise  NotImplementedError
