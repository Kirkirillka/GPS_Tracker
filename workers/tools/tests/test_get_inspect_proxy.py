from unittest import TestCase

from workers.tools.stats import _get_inspector_proxy


class TestGet_inspector_proxy(TestCase):
    def test_get_inspectotr_proxy(self):
        res = _get_inspector_proxy()

        self.assertTrue(res)
