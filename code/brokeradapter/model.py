import paho
import logging

import paho.mqtt.client as mqtt

from typing import List, Callable, Tuple, Any, Mapping
from socket import error as SocketError


from config.utils import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()


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

        self._host = CONFIG["brokeradapter"]["host"]
        self._port = CONFIG["brokeradapter"]["port"]
        self._user = CONFIG["brokeradapter"]["user"]
        self._password = CONFIG["brokeradapter"]["password"]

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

        except SocketError as e:
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
        for topic, callback in self._topics.items():
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