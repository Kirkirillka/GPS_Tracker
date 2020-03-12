from flask import Flask, jsonify
from flask import request

from flask_cors import CORS

from storage import MongoDBStorageAdapter
from utils.tools import BSONClassEncoder
from utils.normalizers import DefaultNormalizer

from workers.tools.integrations import make_celery
from workers.tasks import dispatch_estimation
from workers.celery import connection_string
from workers.tools.stats import get_active_tasks_list, get_registered_tasks_list, get_scheduled_tasks_list

from datavisual import APP_NAME

# Logging section
from utils.logs.tools import get_child_logger_by_name
logger = get_child_logger_by_name(APP_NAME)


app = Flask(APP_NAME)
app.config.update(
    CELERY_BROKER_URL=connection_string,
    CELERY_RESULT_BACKEND=connection_string
)
CORS(app)
app.storage = MongoDBStorageAdapter()
celery = make_celery(app)

# Make it possible to parse datetime
app.json_encoder = BSONClassEncoder


@app.route("/messages/all", methods=["GET"])
def all_messages() -> dict:
    """
        HTTP Endpoint to access all received messages from clients
    """

    records = app.storage.get_raw_msgs()

    return jsonify(records)


@app.route("/messages/last", methods=["GET"])
def last_messages() -> dict:
    """
        HTTP Endpoint to access the most recent messages from clients
    """

    records = app.storage.get_last_raw_msgs()

    return jsonify(records)


@app.route("/clients/all", methods=['GET'])
def all_clients():
    """
        HTTP Endpoint to access the ID of registered clients
    """

    clients = app.storage.get_clients_list()

    return jsonify(clients)


@app.route("/aggr/by_device_id", methods=["POST"])
def aggregation_by_device_id():
    """
        HTTP Endpoint to access the records aggregated per <device.id>
    """
    json_data = request.json

    if json_data:

        data = app.storage.get_aggr_per_client(**json_data)
    else:
        data = app.storage.get_aggr_per_client()

    return jsonify(data)


@app.route("/estimations/new", methods=["POST"])
def run_new_estimation():
    """
        Dispatch a new work for Celery.

        JSON must contains:

        - Start date of data to filterer
        - End data of data to filter
        - A number of clusters

    :return: job id
    """

    logger.info("Dispatch a new optimization task.")

    json_data = request.json
    job_id = dispatch_estimation.delay(**json_data)

    logger.debug("Scheduled task ID is {}.".format(job_id))

    return jsonify(job_id=str(job_id))


@app.route("/estimations/all", methods=["POST"])
def get_all_estimations():
    """
        HTTP Endpoint to access the estimation made by analyzers
    """

    json_data = request.json

    if json_data:

        data = app.storage.get_all_estimations(**json_data)
    else:
        data = app.storage.get_all_estimations()

    return jsonify(data)


@app.route("/estimations/recent", methods=["GET"])
def get_recent_estimation():

    """
        HTTP Endpoint to access only the most recent done estimation
    :return:
    """

    return jsonify(app.storage.get_recent_estimation())


@app.route("/db/stats", methods=["GET"])
def get_db_stats():
    stats = app.storage.get_db_stats()

    return jsonify(stats)


@app.route("/tasks/stats/<type>", methods=["GET"])
def get_tasks_stats(type: str):

    task_type_mapping = {
        "active": get_active_tasks_list,
        "registered": get_registered_tasks_list,
        "scheduled": get_scheduled_tasks_list
    }

    def default_func(): return {}

    stat_func = task_type_mapping.get(type, default_func)

    task_list = stat_func()

    return jsonify(task_list)


@app.route("/message/new", methods=["POST"])
def handle_new_message_directly():

    """
    API Entry point for directly send messages from GPS_Android to the database.
    :return: 200 if the message is normalized and saved successfully, 400 if the format is invalid.
    """

    logger.info("A new request to directly save the message to DB.")
    json_data = request.json

    _normalizer = DefaultNormalizer()
    normalized_messages = _normalizer.normalize(json_data)

    if normalized_messages:
        logger.debug("Message is successfully normalized")
        app.storage.save(normalized_messages)
        return jsonify(success=True, code=200)
    else:
        logger.error("Cannot normalize the message! Drop it.")
        logger.debug("Dropped message is {}".format(json_data))
        res = jsonify(success=False, code=400)

        return res


if __name__ == '__main__':
    logger.info("Starting GPS_Tracker datavisual backend.")
    app.run(host="0.0.0.0", port=5000,debug=True)
