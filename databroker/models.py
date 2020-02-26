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
from utils.logs.tools import get_child_logger_by_name
logger = get_child_logger_by_name(__name__)


# Project configuration
DEFAULT_CONFIG = get_project_config()

# Default topics to subscribe
TOPICS = [
    "/clients",
    "/messages/#",
]


class DataBroker:
    """ Class DataBroker

        This class is to encapsulate possible manipulations on data received from MQTT Message Broker and to specify
        callback function for registered get_topics.

        The class aggregate *MQTTBrokerAdapter* and *MongoDBStorageAdapter*.

        Usage flow
        ======

        - Create an instance of DataBroker.
        - If required, specify additional get_topics with callbacks, or rewrite defaut get_topics with .set_callback_func
        - Trigger .initialize() to establish connection to Storage and MessageBroker.
        - Start loop via .run_loop(). Then the messages with the get_topics will be processed.

        Examples
        ======

        Create an DataBroker instance, initialize with default get_topics and run loop.

        >>> dbroker = DataBroker()
        >>> dbroker.initialize()
        >>> dbroker.run_loop()

        Register unusual topic

        >>> dbroker.set_callback_func("unusual/topic",
                        lambda x,y,z: print(x,y,z))

    """

    def __init__(self):

        self._mqtt_adapter = MQTTBrokerAdapter()
        self._store_adapter = MongoDBStorageAdapter()
        #
        self._normalizer = DefaultNormalizer()
        self._topics = TOPICS

    def set_callback_func(self, topic: str, callback: Callable[[Client, None, MQTTMessage], None]) -> bool:

        """ Specify unusual topic or rewrite an registered topic with different callback.

            .set_callback_func() allow to set manually a callback for the specific topic.

        :param topic: a topic name
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

            logger.debug(f"Received a message on the topic: '{message.topic}'")
            normalized_message = self._normalizer.normalize(message.payload)
            if normalized_message:
                logger.info(f'A new message received, normalized. Client ID is {normalized_message["device"]["id"]}.'
                            f' Ready to save it. ')
                self._store_adapter.save(normalized_message)
            else:
                logger.error("Cannot normalize the message!")

        def _default_callback(client: Client, userdata: None, message: MQTTMessage) -> None:
            """
                A function used as callback for every message received in the specified get_topics list. Has quite strict
                parameter signature.
            :param client_id: An client ID.
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

            :param client_id: An client ID.
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

            - Establish connection with Storage.
            - Register all get_topics and its callback function to MQTTBrokerAdapter.
            - Instruct MQTTBrokerAdapter to setup connection to MQTT MessageBroker and subscriptions,

        :return: True if initialization is completed, False if an error occurred
        """

        logger.info("Start DataBroker configuration.")

        # Step 1. Add get_topics and callback functions
        for topic in self._topics:
            _callback = self.get_callback_func(topic)
            self._mqtt_adapter.add_topic(topic, _callback)

        logger.info("All components were initialized successfully.")

        return True

    def run_loop(self) -> bool:

        """
            Start processing messages from MQTT Message Broker.

            Internally, it executes *MQTTBrokerAdapter.serve()* function. You can stop polling with your callback function
            and invokes *stop()* on *MQTTBrokerAdapter*.

            run_loop() is a blocking function.

        :return: True if loop is over, False if DataBroker is not initialized.
        """

        logger.info("Start message pooling loop. Enter the blocked section.")
        # run client forever looping
        res = self._mqtt_adapter.serve()

        return bool(res)

    def stop_loop(self) -> None:

        """
            Force to stop the loop
        :return: None
        """

        logger.debug("Interrupting the pooling loop.")
        self._mqtt_adapter.stop()
        logger.info("Running loop was stoped.")

        return

