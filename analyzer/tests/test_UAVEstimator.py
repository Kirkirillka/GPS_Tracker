from unittest import TestCase
import datetime

from analyzer.models import UAVEstimator

class TestUAVEstimator(TestCase):
    def test_run_estimation(self):

        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=10)
        n_clusters = 10
        method = "simplex"

        estimator = UAVEstimator(method)

        res = estimator.run_estimation(start_date, end_date, n_clusters)

