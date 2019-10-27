import os
import  datetime
import uuid
import logging

from itertools import count
from time import sleep

import paho.mqtt.client as mqtt


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# A Unique (semi-unique) ID is required to remember clients telemetry
def get_id():
    if os.path.exists("/tmp/gps_uuid"):
        with open("/tmp/gps_uuid") as file:
            stored_id = file.readline()[:-1]

            if stored_id:

                logger.info(f"Found saved UUID. Use {stored_id}.")

                return stored_id

    logger.warning(f"Cannot found a UUID. Generate a new UUID.")

    new_uuid = str(uuid.uuid1())

    with open("/tmp/gps_uuid","w+") as file:
        file.write(new_uuid + "\n" )

    return new_uuid


my_id = get_id()
topic_name = "/gps/{}".format(my_id)

# Endless loop to flood MQTT Broker
def start_sending(cln: mqtt.Client ):

    # For 0 to infinity
    for next_value in count():

        # Form data payload
        current_data = datetime.datetime.now()
        payload = f"Current time is {current_data}. Message #{next_value}"

        # Publish message
        cln.publish(topic_name,payload)

        # Wait a little bit
        sleep(0.5)





if __name__ == '__main__':

    # Initialize connection with specified UUID
    client = mqtt.Client(client_id=my_id)
    client.connect("localhost", 1883, 60)

    start_sending(client)

