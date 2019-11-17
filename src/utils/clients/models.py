# Python library import
from abc import ABC, abstractmethod

# Project modules
from adapters import MQTTBrokerAdapter
from utils.generators import RealisticClientPayloadGenerator

# Logging section
import logging.config
from utils.logs.tools import read_logging_config
logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)


class AbstractClientAppMock(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def gen_and_send(self):
        pass


class WIFIClientAppMock(AbstractClientAppMock):


    def __init__(self):

        self._generator = RealisticClientPayloadGenerator()
        self._mqtt_adapter = MQTTBrokerAdapter()

    def gen_and_send(self) -> bool:

        topic_name = "/messages/"

        logger.debug(f"Take a message from generator {str(self._generator.__class__)}")
        msg = self._generator.get()

        logger.debug("Sending the message to MQTT Broker: ", msg)
        res = self._mqtt_adapter.publish(topic_name, msg)

        return res