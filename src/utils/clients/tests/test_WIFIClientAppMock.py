from unittest import TestCase

from utils.clients.models import WIFIClientAppMock


class TestWIFIClientAppMock(TestCase):

    def test_gen_and_send_number(self, number = 1 ):

        client = WIFIClientAppMock()

        for r in range(number):
            res = client.gen_and_send()
            self.assertTrue(res)


    def test_gen_and_send_3(self):

        self.test_gen_and_send_number(3)


    def test_gen_and_send_6(self):

        self.test_gen_and_send_number(6)


    def test_gen_and_send_9(self):

        self.test_gen_and_send_number(9)