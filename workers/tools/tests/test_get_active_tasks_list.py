from unittest import TestCase

from workers.tools.stats import get_active_tasks_list

class TestGet_active_tasks_list(TestCase):
    def test_get_active_tasks_list(self):

        tasks = get_active_tasks_list()

        self.assertTrue(isinstance(tasks,dict))
