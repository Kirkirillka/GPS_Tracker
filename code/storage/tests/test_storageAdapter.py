from unittest import TestCase

from storage.models import MongoDBStorageAdapter
from utils.generators import RawPayloadGenerator


class TestStorageAdapter(TestCase):

    def setUp(self) -> None:

        self.adapter = MongoDBStorageAdapter()

        # Modify default collection_name
        self.adapter.collection_name = "test"

        self.test_setup()

        self.generated_messages = []

    def tearDown(self) -> None:

        # Check if corresponding test is working properly
        self.test_del_message()

        while self.generated_messages:
            message = self.generated_messages.pop()
            self.adapter.del_message(message)

    def test_setup(self):

        res = self.adapter.setup()

        self.assertTrue(res)

    def test_save_message(self):

        # Prepare message
        message = RawPayloadGenerator().get()

        # Save the message to delete it at the end of the tests
        self.generated_messages.append(message)

        # Save message
        res = self.adapter.save_message(message)

        self.assertTrue(res is not None)

    def test_del_message(self):

        # Prepare message
        message = RawPayloadGenerator().get()

        # Add message into database
        added_id = self.adapter.save_message(message)

        # Delete message from database
        deleted_id = self.adapter.del_message(message)

        self.assertEqual(added_id, deleted_id)

    def test_get_all_messages(self):

        # Prepare message
        messages = [RawPayloadGenerator().get() for _ in range(30)]

        # Save added messages
        self.generated_messages.extend(messages)

        # Add these messages into database
        for message in messages:
            self.adapter.save_message(message)

        # Fetch added messages
        available_messages = self.adapter.get_all_messages()

        self.assertEqual(available_messages, messages)

    def test_get_last_messages(self):

        # I don't know how to implememnt it properly :(
        # Please, Rustam
        raise NotImplementedError


    def test_get_registered_clients(self):

        # Prepare message
        messages = [RawPayloadGenerator().get() for _ in range(4)]

        # Save added messages
        self.generated_messages.extend(messages)

        # Add these messages into database
        for message in messages:
            self.adapter.save_message(message)

        clients = self.adapter.get_registered_clients()

        self.assertTrue(isinstance(clients,list))
        self.assertTrue(len(clients)> 0)