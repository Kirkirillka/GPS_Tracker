from unittest import TestCase

from unittest import TestCase

from storage.models import MongoDBStorageAdapter
from utils.generators import RawPayloadGenerator


class TestMongoDBStorageAdapter(TestCase):

    def setUp(self) -> None:

        self.adapter = MongoDBStorageAdapter()

        # Modify default collection_name
        self.adapter.collection_name = "test"

        self.generated_messages = []

    def tearDown(self) -> None:

        while self.generated_messages:
            message = self.generated_messages.pop()
            self.adapter.delete(message)

    def test_get_last_coords(self):
        self.fail()

    def test_get_coords_by_client_id(self):
        self.fail()

    def test_get_all_msgs(self):

        # Prepare message
        messages = [RawPayloadGenerator().get() for _ in range(30)]

        # Save added messages
        self.generated_messages.extend(messages)

        # Add these messages into database
        for message in messages:
            self.adapter.save(message)

        # Fetch added messages
        available_messages = self.adapter.get_all_msgs()

        self.assertEqual(available_messages, messages)

    def test_get_last_msgs(self):
        available_messages = self.adapter.get_last_msgs()
        self.fail()

    def test_get_clients(self):
        # Prepare message
        messages = [RawPayloadGenerator().get() for _ in range(4)]

        # Save added messages
        self.generated_messages.extend(messages)

        # Add these messages into database
        for message in messages:
            self.adapter.save(message)

        clients = self.adapter.get_clients()

        self.assertTrue(isinstance(clients, list))
        self.assertTrue(len(clients) > 0)

    def test_save(self):

        # Prepare message
        message = RawPayloadGenerator().get()

        # Save the message to delete it at the end of the tests
        self.generated_messages.append(message)

        # Save message
        res = self.adapter.save(message)

        self.assertTrue(res is not None)

    def test_delete(self):

        # Prepare message
        message = RawPayloadGenerator().get()

        # Add message into database
        added_id = self.adapter.save(message)

        # Delete message from database
        deleted_id = self.adapter.delete(message)

        self.assertEqual(added_id, deleted_id)
