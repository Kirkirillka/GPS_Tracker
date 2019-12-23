from .celery import celery_app

from analyzer.models import UAVEstimator

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@celery_app.task
def add(x,y):
    return x + y


@celery_app.task
def dispatch_estimation(start_time, end_time, n_clusters, method):

    logger.debug("Preparing UAVEstimator...")
    estimator = UAVEstimator(method)

    logger.info("Starting estimation process...")
    estimator.run_estimation(start_time, end_time, n_clusters)

    logger.info("Estimation is done!")