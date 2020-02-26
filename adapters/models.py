# Python library import
import os
from socket import error as SocketError
from typing import List, Callable, Any

# 3-td party libraries
import paho.mqtt.client as mqtt

# Project modules
from config.utils import get_project_config
from utils.tools import convert_to_str

# Logging section
import logging

logger = logging.getLogger(__name__)

# Project configuration
DEFAULT_CONFIG = get_project_config()


class MQTTBrokerAdapter:
    """ Description:

        **MQTTBrokerAdapter** is responsible for providing an interface to MQTT Message Broker.

        It allows to specify get_topics to subscribe, set callbacks to be executed on a new message arrived
        on the get_topics. After all subscriptions are specified, BrokerAdapter.serve() can be executed to pool messages
        from MQTT Message Broker.

        The class takes parameters from the config provided by **DEFAULT_CONFIG**. Other way is to define OS environment
        variables to adjust the behaviour.

        :param string MQTT_HOST: MQTT server address
        :param int MQTT_PORT: MQTT server port
        :param string MQTT_USER: (not implemented)
        :param string MQTT_PASSWORD: (not implemented)


        General usage flow:

            1. First, instantiate **BrokerAdapter**. After an instance of **BrokerAdapter** is created, you should
               specify :py:meth:`.get_topics` to subscribe and callbacks to be executed.
            2. Then execute :py:meth:`.setup` function - that performs all subscription to MQTT MessageBroker.
            3. Start message polling via :py:meth:`.serve` function. This operation is blocking, so it will release
               after :py:meth:`.stop` will be triggered. :py:meth:`.setup` will be executed before :py:meth:`.serve`,
               if it's not done earlier

        Example:

            >>> adapter = MQTTBrokerAdapter()
            >>> adapter.add_topic("any/topic/#",print)
            >>> adapter.serve()


    """

    def __init__(self):

        # MQTT connection
        self._conn = mqtt.Client()

        # Storage for topic <-> callback mapping
        self._topics: dict = {}

        # Connection parameters to MQTT Message Broker
        self._host: str = os.environ.get('MQTT_HOST') or DEFAULT_CONFIG["mqtt"]["host"]
        self._port: int = int(os.environ.get('MQTT_PORT') or DEFAULT_CONFIG["mqtt"]["port"])
        self._user: str = os.environ.get('MQTT_USER') or DEFAULT_CONFIG["mqtt"]["user"]
        self._password: str = os.environ.get('MQTT_USERPASS') or DEFAULT_CONFIG["mqtt"]["password"]

        # Setup the connection
        self._connect()

    def _connect(self) -> bool:

        """
        Establish connection to MQTT MessageBroker.
        Internally, executes :py:meth:`mqtt.connect` function with the provided parameters.

        :return: If connection established, then returns True, if there is timeout, then returns False.

        :raise SocketError: if the trying to connect to MQTT is timed out.

        """

        try:
            # Connect to MQTT Message Broker
            self._conn.connect(host=self._host, port=self._port, )
            # Enable action logging
            self._conn.enable_logger(logger)
        except SocketError as e:
            # If connection is timed out
            logger.error(f"Connection to {self._host} is timed out. {e}")
        else:
            # Notify that connection is successful
            return True

    def get_topics(self) -> List[str]:

        """
            Returns a list of registered get_topics to subscribe.
            Internally, the list of :py:meth:`get_topics` is presented by :py:attr:`_topics` variable.
            This function should take care of the right formatting and checking.

        :return: A list of get_topics which to subscribe on.
        """

        return list(self._topics.keys())

    def publish(self, topic: str, message: Any) -> bool:

        """
            Publish a message on the specific topic.

        :param topic: A name of topic
        :param message: A payload to send
        :return: True if sent, False otherwise
        """

        converted_msg = convert_to_str(message)

        res, _ = self._conn.publish(topic, converted_msg)

        return res == 0

    def add_topic(self, topic: str, callback: Callable[[str, str, object], None], forced: bool = False) -> bool:

        """
            Register the *topic* with *callback*.

            Record the subscription information on specific *topic*. A *callback* function is to be executed
            with  each time a new message is arrived with the topic.

            If **force** is specified, if the *topic* is already registered in *MQTTBrokerAdapter._topics*, change its
            callback function to *callback*.

        :param topic: A string specified a topic path
        :param callback:  A function or a callable object, which can take at least three parameters.
        :param forced: To set if rewrite an existing topic mapping.
        :return: True if registration is done, False otherwise
        """

        # Check if the topic is already subscribed
        if topic in self._topics.keys():

            # Check if it's forced to rewrite the topic <-> callback mapping.
            if forced:
                logger.info(f"Rewrite callback for topic '{topic}' to callable '{callback}'")

                # Add topic into internal list
                self._topics[topic] = callback

                # Re-subscribe on the topic
                self._conn.unsubscribe(topic)
                self._conn.subscribe(topic)
                self._conn.message_callback_add(topic, callback)

                logger.debug(f"The topic '{topic}' has been updated with function '{callback}'.")

                return True

            # Topic is already registered, so nothing to do.
            return False
        else:

            logger.info(f"Added a new subscriber to  '{topic}'.")

            # Add topic into internal list
            self._topics.setdefault(topic, callback)

            # Perform subscription
            self._conn.subscribe(topic)
            self._conn.message_callback_add(topic, callback)

            logger.debug(f"Subscription on topic '{topic}' with function '{callback}' is done.")

            return True

    def del_topic(self, topic: str) -> bool:
        """
            Cancel registration on the *topic*.

            * Unsubscribe on the topic from MQTT Message broker.
            * Delete the topic from *_topics*/

        :param topic: a string specifies a topic (format : "/my/format/for/any/*")
        :return: True if unsubscription is successful, False otherwise

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
            Start pooling :py:attr:`get_topics` from MQTT Message Broker.

            Run internal :py:meth:`_conn.run_forever` function in :py:attr:`_conn`.

            This function is blocking, so function won't return
            until disconnect is executed on MQTT connection object.

        :return: True if loop is stopped
        """

        # Start looping
        logger.info("Start MQTT Message receiving loop pooling.")
        res = self._conn.loop_forever()

        # Loop is over
        logger.info("Pooling loop is over, exiting...")
        return res

    def stop(self) -> int:
        """
            Stop MQTT message pooling.

            Execute internal :py:meth:`_conn.disconnect` function in :py:attr:`_conn`.

        :return: True if MQTTBrokerAdapter stopped.
        """

        logger.info("Disconnect from MQTT Server.")
        res = self._conn.disconnect()

        return res
