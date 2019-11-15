from unittest import TestCase

from utils.clients.models import WIFIClientAppMock


class TestWIFIClientAppMock(TestCase):

    def test_gen_and_send_number(self, number = 1 ):

        client = WIFIClientAppMock()

        for r in range(number):
            res = client.gen_and_send()
            self.assertTrue(res)


    def test_gen_and_send_30(self):

        self.test_gen_and_send_number(30)


    def test_gen_and_send_60(self):

        self.test_gen_and_send_number(60)


    def test_gen_and_send_90(self):

        self.test_gen_and_send_number(90)