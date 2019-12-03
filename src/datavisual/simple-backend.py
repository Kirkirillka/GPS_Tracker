from flask import Flask, jsonify, json
from flask import request

from flask_cors import CORS


from storage import MongoDBStorageAdapter

app = Flask(__name__)
CORS(app)
app.storage = MongoDBStorageAdapter()


def sanitize_json(json_data : dict) -> dict:
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


@app.route("/aggr/by_device_id", methods=['GET'])
def aggregation_by_device_id():

    """
        HTTP Endpoint to access the records aggregated per <device.id>
    """

    limit = request.args.get("limit",default=10,type=int)

    data = app.storage.get_aggr_per_client(limit_to=limit)

    return jsonify(data)


@app.route("/estimations/all", methods=["GET"])
def all_estimations():

    raise NotImplementedError


@app.route("/estimations/last", methods=["GET"])
def last_estimations():

    raise NotImplementedError


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
