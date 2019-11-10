from unittest import TestCase
import json

from databroker.model import DataBroker

from utils.field_gens import device_id_gen, generate_dict_by_mapping, WIFI_PAYLOAD_FIELDS_TEMPLATE


class TestDataBroker(TestCase):

    def test_get_callback_func(self):
        dbroker = DataBroker()

        test_topic = "/uri/to/topic"
        client_id = device_id_gen()
        userdata = generate_dict_by_mapping(WIFI_PAYLOAD_FIELDS_TEMPLATE)
        message = userdata

        callback = dbroker.get_callback_func(test_topic)

        res = callback(client_id, userdata, message)

        self.assertEqual(res, None)

    def test_initialize(self):

        dbroker = DataBroker()
        res = dbroker.initialize()

        self.assertTrue(res)

    def test_run_loop(self):

        dbroker = DataBroker()

        # Get callback to stop the loop
        disconnect_callback = dbroker.get_callback_func("disconnect")

        # On system messages, stop listening
        sub_topic = "$SYS/#"
        dbroker.set_callback_func(sub_topic, disconnect_callback)

        # Start looping. Must exit at any message with True
        dbroker.initialize()
        res = dbroker.run_loop()

        self.assertTrue(res)


