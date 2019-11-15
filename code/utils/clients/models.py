from abc import ABC, abstractmethod

from adapters import MQTTBrokerAdapter
from generators import WIFIPayloadGenerator


import logging

logger = logging.getLogger(__name__)


class AbstractClientAppMock(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def gen_and_send(self):
        pass


class WIFIClientAppMock(AbstractClientAppMock):


    def __init__(self):

        self._generator = WIFIPayloadGenerator()
        self._mqtt_adapter = MQTTBrokerAdapter()

    def gen_and_send(self) -> bool:

        topic_name = "/messages/"

        logging.debug("Take a message from generator")
        msg = self._generator.get()

        logging.debug("Sending the message to MQTT Broker")
        res = self._mqtt_adapter.publish(topic_name, msg)

        return res