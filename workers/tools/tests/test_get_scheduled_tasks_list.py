from unittest import TestCase

from workers.tools.stats import get_scheduled_tasks_list


class TestGet_scheduled_tasks_list(TestCase):
    def test_get_scheduled_tasks_list(self):

        tasks = get_scheduled_tasks_list()

        self.assertTrue(isinstance(tasks,dict))
