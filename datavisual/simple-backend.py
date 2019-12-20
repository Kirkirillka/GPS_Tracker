from flask import Flask, jsonify, json
from flask import request

from flask_cors import CORS

from storage import MongoDBStorageAdapter

app = Flask(__name__)
CORS(app)
app.storage = MongoDBStorageAdapter()


def sanitize_json(json_data: dict) -> dict:
    """
        Allow to parse unknown objects from MongoDB, which the default JSON parser cannot
        understand
    :param json_data: python dict
    :return: dict
    """
    _san_json = json.dumps(json_data, default=str)
    return json.loads(_san_json)


@app.route("/messages/all", methods=["GET"])
def all_messages() -> dict:
    """
        HTTP Endpoint to access all received messages from clients
    """

    records = app.storage.get_raw_msgs()
    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


@app.route("/messages/last", methods=["GET"])
def last_messages() -> dict:
    """
        HTTP Endpoint to access the most recent messages from clients
    """

    records = app.storage.get_last_raw_msgs()
    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


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

    sanitized_records = sanitize_json(data)

    return jsonify(sanitized_records)


@app.route("/estimations/last", methods=["GET"])
def last_estimations():
    raise NotImplementedError


@app.route("/stat", methods=["GET"])
def get_statistics():
    stats = app.storage.get_stats()

    return jsonify(stats)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
