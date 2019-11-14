import logging

import paho.mqtt.client as mqtt

from typing import List, Callable, Any
from socket import error as SocketError

from config.utils import get_config
from utils.tools import convert_to_str

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()


class MQTTBrokerAdapter:
    """
        **MQTTBrokerAdapter** is responsible for providing an interface to MQTT Message Broker.

        It allows to specify get_topics to subscribe, set callbacks to be executed on a new message arrived
        on the get_topics. After all subscriptions are specified, BrokerAdapter.serve() can be executed to pool messages
        from MQTT Message Broker.

        General usage flow
        ======

        First, instantiate **BrokerAdapter**
        After an instance of **BrokerAdapter** is created, you should specify get_topics to subscribe and callbacks to be
        executed.
        Then execute .setup() function - that performs all subscription to MQTT MessageBroker.
        Start message polling via .serve() function. This operation is blocking, so it will release after .stop()
        will be triggered. .setup() will be executed before .serve(), if it's not done earlier

        Example
        ======

            >>> adapter = MQTTBrokerAdapter()
            >>> adapter.add_topic("any/topic/#",print)

            >>> adapter.serve()
    """

    def __init__(self):

        # MQTT client
        self._conn = mqtt.Client()

        # Storage for topic <-> callback mapping
        self._topics: dict = {}

        # Connection parameters to MQTT Message Broker
        self._host: str = CONFIG["mqtt"]["host"]
        self._port: int = int(CONFIG["mqtt"]["port"])
        self._user: str = CONFIG["mqtt"]["user"]
        self._password: str = CONFIG["mqtt"]["password"]

        # Setup the connection
        self.setup()

    def _connect(self,
                 host: str,
                 port: int = 1883,
                 user: str = None,
                 password: str = None
                 ) -> bool:

        """
            Establish connection to MQTT MessageBroker.

            Internally, executes mqtt.connect() function with configured parameters.
            If connection established, then returns True, if there is timeout, then returns False.

        :param host: argument to specify to which MQTT address to connect.

        :param port: MQTT Message Broker port to connect. Default is 1883.

        :param user: *Not implemented yet*.A user to be identified. If not specified, no authentication is used.

        :param password: *Not implemented yet*. A user's password to authenticate.

        :return: True if successful, False otherwise.

        """

        try:
            # Connect to MQTT Message Broker
            self._conn.connect(host=host, port=port,)
            # Enable action logging
            self._conn.enable_logger(logger)

        except SocketError as e:
            # If connection is timed out
            logger.error(f"Connection to {host} is timed out. {e}")
            return False
        else:
            # Notify that connection is successful
            return True

    def setup(self) -> bool:

        """

            Configure connection parameters and perform subscriptions.

        :return: True, if connection and subscriptions made successfully. otherwise, raise ConnectionError.
        :raises:
            :raise ConnectionError - connection to provided MQTT Message Broker address is not possible.
        """

        # Try to establish connection to MQTT Message broker
        con_res = self._connect(self._host, self._port, self._user, self._password)

        # Fail if cannot connect to the server
        if con_res:
            logger.info(f"Connection to MQTT Message Broker server {self._host} is established.")

            # Perform subscription
            for topic, callback in self._topics.items():

                self._conn.subscribe(topic)
                self._conn.message_callback_add(topic, callback)

                logger.debug(f"Subscription on topic '{topic}' with function '{callback}' is done.")

            # Set itself as initialized instance
            self._is_initialized = True

            return True
        else:
            raise ConnectionError(f"Connection to MQTT Message Broker server {self._host} is not possible!")

    def get_topics(self) -> List[str]:

        """
            Returns a list of registered get_topics to subscribe.

            Internally, the list of get_topics is presented by *_topics* variable.

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

        return res is 0

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

                return True

            # Topic is already registered, so nothing to do.
            return False
        else:

            logger.info(f"Added a new subscriber to  '{topic}'.")

            # Add topic into internal list
            self._topics.setdefault(topic, callback)

            return True

    def del_topic(self, topic: str) -> bool:
        """
            Cancel registration on the *topic*.

            **Actions**:

            * Unsubscribe on the topic from MQTT Message broker.
            * Delete the topic from *_topics*/

        :param topic: a string specifies a topic (format : "/my/format/for/any/*")
        :return: True if unsubscribed, False otherwise

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
            Start pooling get_topics from MQTT Message Broker.

            Run internal *loop_forever* function in *_conn*.

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
            Stop pooling.

            Execute internal *disconnect* function in *_conn*.

        :return: True if MQTTBrokerAdapter stopped.
        """

        logger.info("Disconnect from MQTT Server.")
        res = self._conn.disconnect()

        return res
