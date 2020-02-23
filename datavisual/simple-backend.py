from flask import Flask, jsonify
from flask import request

from flask_cors import CORS

from storage import MongoDBStorageAdapter
from utils.tools import BSONClassEncoder
from utils.normalizers import DefaultNormalizer

from workers.tools.integrations import make_celery
from workers.tasks import dispatch_estimation, add
from workers.celery import connection_string

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
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
    json_data = request.json

    start_date = json_data["start_date"]
    end_date = json_data["end_date"]
    num_clusters = json_data['num_clusters']
    method = json_data["method"]
    explicit_ues_locations = json_data["explicit_ues_locations"]

    job_id = dispatch_estimation.delay(start_date, end_date, num_clusters, method,
                                       explicit_ues_locations = explicit_ues_locations)

    return jsonify(str(job_id))


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
    from workers.tools.stats import get_active_tasks_list, get_registered_tasks_list, get_scheduled_tasks_list

    task_type_mapping = {
        "active": get_active_tasks_list,
        "registered": get_registered_tasks_list,
        "scheduled": get_scheduled_tasks_list
    }

    def default_func(): return {}

    stat_func = task_type_mapping.get(type, default_func)

    task_list = stat_func()

    return jsonify(task_list)


@app.route("/messages/new", methods=["POST"])
def handle_new_message_directly():

    logger.debug("New message is received.")
    json_data = request.json

    _normalizer = DefaultNormalizer()
    normalized_messages = _normalizer.normalize(json_data)

    if normalized_messages:
        logger.debug("Message is normalized, save in DB.")
        app.storage.save(normalized_messages)
        return jsonify(success=True)
    else:
        logger.error("Cannot normalize the message! Drop it.")
        logger.debug("Dropped message is {}".format(json_data))
        return jsonify(success=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
