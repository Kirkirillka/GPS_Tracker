# Python library import
import json
from abc import ABC, abstractmethod

# Project modules
from adapters import MQTTBrokerAdapter
from utils.generators import RealisticClientPayloadGenerator
from utils.tools import DateTimeEncoder

# Logging section
import logging.config
logger = logging.getLogger(__name__)


class AbstractClientApp(ABC):

    """
    Class :py:class:`AbstractClientApp` is an abstract class to hold methods for an application which is supposed to
    generate user payload.

    Methods:

        gen_and_send () : generate a sample of user data and send it to the Broker.

    """

    @abstractmethod
    def gen_and_send(self):
        raise NotImplementedError


class WIFIClientAppMock(AbstractClientApp):

    """
    Class :py:class:`WIFIClientAppMock` implements logic to simulate an real Android user and send the data to MQTT
    Broker.

    :ivar generator: a generator to take realistic wifi-enabled Android
        user.
    :ivar mqtt_adapter: an adapter to send messages to MQTT Broker.
    """

    def __init__(self):

        self.generator = RealisticClientPayloadGenerator()
        self.mqtt_adapter = MQTTBrokerAdapter()

    def gen_and_send(self) -> bool:

        topic_name = "/messages/"

        logger.debug(f"Take a message from generator {str(self.generator.__class__)}")
        msg = self.generator.get()

        serialized_msg = json.dumps(msg, cls=DateTimeEncoder)

        logger.debug("Sending the message to MQTT Broker: " + str(serialized_msg))
        res = self.mqtt_adapter.publish(topic_name, serialized_msg)

        return res