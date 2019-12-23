from flask import Flask, jsonify
from flask import request

from flask_cors import CORS

from storage import MongoDBStorageAdapter
from utils.tools import BSONClassEncoder

from workers.tools.integrations import make_celery
from workers.tasks import dispatch_estimation, add
from workers.celery import connection_string

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


@app.route("/estimations/all", methods=["POST"])
def all_estimations():
    """
        HTTP Endpoint to access the estimation made by analyzers
    """

    json_data = request.json

    if json_data:

        data = app.storage.get_raw_estimations(**json_data)
    else:
        data = app.storage.get_raw_estimations()

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

    job_id = dispatch_estimation.delay(start_date, end_date, num_clusters, method)

    return jsonify(str(job_id))


@app.route("/estimations/last", methods=["GET"])
def last_estimations():
    raise NotImplementedError


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
