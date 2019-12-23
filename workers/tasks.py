from .celery import app

from analyzer.models import UAVEstimator

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.task
def add(x,y):
    return x + y


@app.task
def dispatch_estimation(**kwargs):

    logger.debug("Preparing UAVEstimator...")
    estimator = UAVEstimator()

    logger.info("Starting estimation process...")
    estimator.run_estimation(**kwargs)

    logger.info("Estimation is done!")