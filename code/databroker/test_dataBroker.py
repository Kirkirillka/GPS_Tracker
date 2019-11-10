from unittest import TestCase
import json

from databroker.classes import DataBroker

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

        res = dbroker.initialize()

        dbroker.run_loop()


