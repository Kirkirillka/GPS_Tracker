import sys
from utils.clients.models import WIFIClientAppMock
from time import sleep

# Logging section
import logging.config
from utils.logs.tools import read_logging_config
logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)


DELAY = 0.7
MAX_MESSAGE_NUMBER = 100000

if __name__ == '__main__':

    try:
        client = WIFIClientAppMock()

        # Loop up to MAX_MESSAGE_NUMBER and count the # of loops,
        # which is equal to # of messages.
        for index in range(0, MAX_MESSAGE_NUMBER):
            logger.info(f"Iteration #{index}. Generate and send to MQTT Message Broker.")
            client.gen_and_send()
            sleep(DELAY)

        logger.info("Finish message sending.")
    except KeyboardInterrupt:

        logger.info("Mock client is interrupted. Exiting...")
        sys.exit(0)