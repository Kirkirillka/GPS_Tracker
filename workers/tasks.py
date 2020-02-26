from .celery import celery_app

from analyzer.models import UAVEstimator

# Logging section
from utils.logs.tools import get_child_logger_by_name
logger = get_child_logger_by_name(__name__)


@celery_app.task
def dispatch_estimation(*args,**kwargs):

    logger.debug("Received the new estimation tasks. Parameters are:")
    logger.debug("Args: " + ",".join(args))
    logger.debug("Kwargs: " + str(kwargs))

    start_date = kwargs.get("start_date")
    end_date = kwargs.get("end_date")
    num_clusters = kwargs.get('num_clusters')
    method = kwargs.get("method")

    estimator = UAVEstimator(method)

    logger.info("Scheduling a new estimation task...")
    estimator.run_estimation(start_date, end_date, num_clusters, **kwargs)
