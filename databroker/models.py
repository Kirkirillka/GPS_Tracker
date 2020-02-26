# Python library import
import os
from typing import Callable

# 3-td party libraries
from paho.mqtt.client import Client, MQTTMessage

# Project modules
from adapters import MQTTBrokerAdapter
from storage import MongoDBStorageAdapter
from utils.normalizers import DefaultNormalizer
from config.utils import get_project_config

# Logging section
import logging.config
from utils.logs.tools import read_logging_config

logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)

# Project configuration
DEFAULT_CONFIG = get_project_config()

# Default topics to subscribe
TOPICS = [
    "/clients",
    "/messages/#",
]


class DataBroker:
    """ Class :py:class:`DataBroker` is to encapsulate possible manipulations on data received from MQTT Message Broker
        and to specify callback function for registered get_topics.

        The class aggregate :py:class:`MQTTBrokerAdapter` and :py:class:`MongoDBStorageAdapter`.

        Usage flow:

        - Create an instance of :py:class:`DataBroker`.
        - If required, specify additional topics with callbacks or rewrite the default topics
          with :py:meth:`DataBroker.set_callback_func`.
        - Trigger :py:meth:`DataBroker.initialize` to establish connection using encaplsulated
          :py:class:`MongoDBStorageAdapter` and :py:class:`MQTTBrokerAdapter`.
        - Start loop via :py:meth:`DataBroker.run_loop`. Then the messages for the registered topics will be processed.

        The class takes parameters from the config provided by **DEFAULT_CONFIG**. Other way is to define OS
        environment variables to adjust the behaviour.

        :param string MQTT_HOST: MQTT server address
        :param int MQTT_PORT: MQTT server port
        :param string MQTT_USER: (not implemented)
        :param string MQTT_PASSWORD: (not implemented)

        Examples:

            Create an DataBroker instance, initialize with default get_topics and run loop.

                >>> dbroker = DataBroker()
                >>> dbroker.initialize()
                >>> dbroker.run_loop()

            Register unusual topic:

                >>> dbroker.set_callback_func("unusual/topic",
                                lambda x,y,z: print(x,y,z))

    """

    def __init__(self):

        self._mqtt_adapter = MQTTBrokerAdapter()
        self._store_adapter = MongoDBStorageAdapter()
        self._normalizer = DefaultNormalizer()
        self._topics = TOPICS

    def set_callback_func(self, topic: str, callback: Callable[[Client, None, MQTTMessage], None]) -> bool:

        """ Specify unusual topic or rewrite an registered topic with different callback. The method
        :py:meth:`set_callback_func` allow to set manually a callback for the specific topic.

        :param str topic: a topic name
        :param callback: a callback object to be executed on a message with topic
        :return: True if topic was set successfully, False otherwise
        """

        # Try to set topic

        logger.info(f"The topic {topic} was rewritten be {callback} function")

        res = self._mqtt_adapter.add_topic(topic, callback, forced=True)

        return res

    def get_callback_func(self, topic: str) -> Callable[[Client, None, MQTTMessage], None]:

        """
            Return callback function on a specific *topic*.

            Internally has a mapping *callback_mapping* that specify for what topic which callback to be returned.
            If the topic is not presented in *callback_mapping*, then *_default_callback* is returned.

        :param topic: a topic to get a callback for.
        :return: callable object which takes 3 parameters and returns None.
        """

        def _store_in_db(client: Client, userdata: None, message: MQTTMessage) -> None:

            logger.debug(f"Received a message on the topic {message}.")
            normalized_message = self._normalizer.normalize(message.payload)
            if normalized_message:
                logger.debug("Message is normalized, save in DB.")
                self._store_adapter.save(normalized_message)
            else:
                logger.error("Cannot normalize the message!")

        def _default_callback(client: Client, userdata: None, message: MQTTMessage) -> None:
            """

            A default callback for the topics which don't have the default handlers.

            Simply logging the input parameters.


            :param client: An MQTT client class.
            :param userdata: ?
            :param message: Message sent on the topic.
            :return: None
            """

            logger.debug("Entered in callback function")
            logger.debug(f"Can access self argument {self}", )
            logger.debug(f"ClientID: {client}")
            logger.debug(f"Userdata: {userdata}")
            logger.debug(f"Message: {message}")

            return None

        def _disconnect_callback(client: Client, userdata: None, message: MQTTMessage) -> None:

            """
                A callback function which stops looping by .disconnect from MQTT Message Broker

            :param client: An MQTT client class.
            :param userdata: ?
            :param message: Message sent on the topic.
            :return: None
            """

            logger.debug(f"Received a message on topic {message.topic}")
            logger.debug("Forced to disconnect.")
            # Force disconnect
            self._mqtt_adapter.stop()

            return None

        # Store mapping between topic names and corresponding callbacks
        callback_mapping = {
            "disconnect": _disconnect_callback,
            "/messages/#": _store_in_db
        }

        # return a callback by key, otherwise return the default callback
        mapped_callback = callback_mapping.get(topic, _default_callback)

        logger.debug(f"Callback for topic '{topic}' is '{mapped_callback}'")

        return mapped_callback

    def initialize(self) -> bool:

        """ Setup internal components.

        1. Establish connection with Storage.
        2. Register all topics and its callback function to :py:class:`MQTTBrokerAdapter`.
        3. Instruct :py:class:`MQTTBrokerAdapter` to setup connection to MQTT MessageBroker
           and perform subscriptions.

        :return: True if initialization is completed, False if an error occurred
        """

        logger.info("Start DataBroker configuration.")

        # Add topics and callback functions
        for topic in self._topics:
            _callback = self.get_callback_func(topic)
            self._mqtt_adapter.add_topic(topic, _callback)

        logger.info("All components were initialized successfully.")

        return True

    def run_loop(self) -> bool:

        """
            Start processing messages from MQTT Message Broker.

            Internally, it executes :py:meth:`*MQTTBrokerAdapter.serve` function. You can stop polling with your
            callback function that invokes :py:meth:`MQTTBrokerAdapter.stop` on :py:class:`MQTTBrokerAdapter`.

            This function is blocking.

        :return: True if loop is over, False if DataBroker is not initialized.
        """

        logger.info("Start message pooling loop. Enter the blocked section.")
        # run client forever looping
        res = self._mqtt_adapter.serve()

        return bool(res)

    def stop_loop(self) -> None:

        """
            Force to stop the loop.

        :return: None
        """

        logger.debug("Interrupting the pooling loop.")
        self._mqtt_adapter.stop()
        logger.info("Running loop was stopped.")

        return
