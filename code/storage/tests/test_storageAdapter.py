from unittest import TestCase

from storage.models import StorageAdapter
from utils.generators import RawPayloadGenerator


class TestStorageAdapter(TestCase):

    def setUp(self) -> None:

        self.adapter = StorageAdapter()

        self.test_setup()

        self.generated_messages = []

    def tearDown(self) -> None:

        # Check if corresponding test is working properly
        self.test_del_message()

        for message in self.generated_messages:
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




