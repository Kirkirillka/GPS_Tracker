import logging

import paho.mqtt.client as mqtt

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# The callback for when the client receives a CONNACK responce from the server
def on_connect(client, userdata, flags, rc):

    logger.info("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed

    # That means subscribe for everything
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):

    logger.info(msg.topic + " " + str(msg.payload))


if __name__ == '__main__':

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    # Blocking call that processed network traffic, dispatches callbacks and handles
    # reconnecting.
    # Other loop*() functions are available that give a threaded interface
    # and a manual interface

    logger.info("Connection initialized. Start listening for new events.")

    client.loop_forever()