from unittest import TestCase

from adapters import MQTTBrokerAdapter


class TestBrokerAdapter(TestCase):

    TOPICS = {
        "one/two/three": lambda x, y, z: print(x, y, z),
    }

    def test_setup(self):

        """
            Test how MQTTBrokerAdapter works on .setup() stage
        :return:
        """

        # Initialize broker
        mqtt_broker = MQTTBrokerAdapter()

        # Add subscription into internal topic lists
        for topic,callback in self.TOPICS.items():
            mqtt_broker.add_topic(topic, callback)

        # Make connection to Storage, MQTT and perform subscription
        res = mqtt_broker.setup()

        self.assertTrue(res)

    def test_get_topics(self):

        """
            Test get_topics() returns exactly the same topic list
        :return:
        """

        # Initialize broker
        mqtt_broker = MQTTBrokerAdapter()

        # Add subscription into internal topic lists
        for topic,callback in self.TOPICS.items():
            mqtt_broker.add_topic(topic, callback)

        # Get get_topics
        registered_topics = mqtt_broker.get_topics()

        self.assertListEqual(registered_topics, list(self.TOPICS))

    def test_add_topic(self):

        mqtt_broker = MQTTBrokerAdapter()

        for topic,callback in self.TOPICS.items():
            res = mqtt_broker.add_topic(topic, callback)

            self.assertTrue(res)

    def test_del_topic(self):

        mqtt_broker = MQTTBrokerAdapter()

        for topic,callback in self.TOPICS.items():
            res_add = mqtt_broker.add_topic(topic, callback)
            self.assertTrue(res_add)

            res_del = mqtt_broker.del_topic(topic)
            self.assertTrue(res_del)

    def test_publish(self):

        mqtt_broker = MQTTBrokerAdapter()

        topic = "simple/topic/name"
        message = {"a":1, "b":2}

        res = mqtt_broker.publish(topic, message)

        self.assertTrue(res)
