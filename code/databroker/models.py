import logging

from typing import Callable, Any

from adapters import MQTTBrokerAdapter
from utils.normalizers import DefaultNormalizer
from config.utils import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()

TOPICS = [
    "/clients",
    "/messages/#",
]


class DataBroker:
    """ Class DataBroker

        This class is to encapsulate possible manipulations on data received from MQTT Message Broker and to specify
        callback function for registered topics.

        The class aggregate *MQTTBrokerAdapter* and *StorageAdapter*.

        Usage flow
        ======

        - Create an instance of DataBroker.
        - If required, specify additional topics with callbacks, or rewrite defaut topics with .set_callback_func
        - Trigger .initialize() to establish connection to Storage and MessageBroker.
        - Start loop via .run_loop(). Then the messages with the topics will be processed.

        Examples
        ======

        Create an DataBroker instance, initialize with default topics and run loop.

        >>> dbroker = DataBroker()
        >>> dbroker.initialize()
        >>> dbroker.run_loop()

        Register unusual topic

        >>> dbroker.set_callback_func("unusual/topic",
                        lambda x,y,z: print(x,y,z))

    """

    def __init__(self):

        self._mqtt_adapter = MQTTBrokerAdapter()
        # TODO: implement StorageAdapter
        self._store_adapter = None
        #
        self._normalizer = DefaultNormalizer()
        self._topics = TOPICS

        self._is_initialized = False

    def set_callback_func(self, topic: str, callback: Callable[[str, Any,Any], None]) -> bool:

        """ Specify unusual topic or rewrite an registered topic with different callback.

            .set_callback_func() allow to set manually a callback for the specific topic.
            Must be executed before .setup() is done

        :param topic: a topic name
        :param callback: a callback object to be executed on a message with topic
        :return: True if topic was set successfully, False otherwise
        """

        # Try to set topic
        res = self._mqtt_adapter.add_topic(topic, callback, forced=True)

        return res

    def get_callback_func(self, topic: str) -> Callable[[str, Any,Any], None]:

        """
            Return callback function on a specific *topic*.

            Internally has a mapping *callback_mapping* that specify for what topic which callback to be returned.
            If the topic is not presented in *callback_mapping*, then *_default_callback* is returned.

        :param topic: a topic to get a callback for.
        :return: callable object which takes 3 parameters and returns None.
        """

        def _default_callback(client_id: str, userdata: Any, message: Any) -> None:
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

            return None

        def _disconnect_callback(*args, **kwargs) -> None:

            """
                A callback function which stops looping by .disconnect from MQTT Message Broker

            :param args: any objects
            :param kwargs: any objects
            :return: None
            """

            # Force disconnect
            self._mqtt_adapter.stop()

            return None

        # Store mapping between topic names and corresponding callbacks
        callback_mapping = {
            "disconnect": _disconnect_callback
        }

        # return a callback by key, otherwise return the default callback
        return callback_mapping.get(topic, _default_callback)

    def initialize(self) -> bool:

        """ Setup StorageAdapter and MQTTBrokerAdapter.

            - Establish connection with Storage.
            - Register all topics and its callback function to MQTTBrokerAdapter.
            - Instruct MQTTBrokerAdapter to setup connection to MQTT MessageBroker and subscriptions,

        :return: True if initialization is completed, False if an error occurred
        """

        # Step 1. Establish connection with Storage
        # //TODO: implement StorageAdapter
        #logger.debug("Initialization StorageAdapter connection.")
        #store_setup_res = self._store_adapter.setup()

        # Step 2. Add topics and callback functions
        for topic in self._topics:
            _callback = self.get_callback_func(topic)
            self._mqtt_adapter.add_topic(topic, _callback)

        # Step 3. Ask MQTTBrokerAdapter to make subscriptions
        broker_setup_res = self._mqtt_adapter.setup()

        # Step 4. Set itself as initialized instance
        if broker_setup_res:
            self._is_initialized = True
        else:
            self._is_initialized = False

        # Finish
        return broker_setup_res

    def run_loop(self) -> bool:

        """
            Start processing messages from MQTT Message Broker.

            Internally, it executes *MQTTBrokerAdapter.serve()* function. You can stop polling with your callback function
            and invokes *stop()* on *MQTTBrokerAdapter*.

            run_loop() is a blocking function.

        :return: True if loop is over, False if DataBroker is not initialized.
        """

        # Check if .setup() first was executed
        if not self._is_initialized:
            return False

        # run client forever looping
        res = self._mqtt_adapter.serve()

        return bool(res)

