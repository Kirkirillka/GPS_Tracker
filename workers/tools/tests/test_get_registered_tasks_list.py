from unittest import TestCase

from workers.tools.stats import get_registered_tasks_list

class TestGet_registered_tasks_list(TestCase):
    def test_get_registered_tasks_list(self):

        tasks = get_registered_tasks_list()

        self.assertTrue(isinstance(tasks,dict))
