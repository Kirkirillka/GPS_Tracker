from flask import Flask, jsonify, json
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

    records = app.storage.get_all_msgs()
    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


@app.route("/messages/last", methods=["GET"])
def last_messages() -> dict:

    """
        HTTP Endpoint to access the most recent messages from clients
    """

    records = app.storage.get_last_msgs()
    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


@app.route("/clients/all", methods=['GET'])
def all_clients():

    """
        HTTP Endpoint to access the ID of registered clients
    """

    clients = app.storage.get_clients()

    return jsonify(clients)


@app.route("/coordinates/all", methods=['GET'])
def get_all_coords():

    """
        HTTP Endpoint to access the sequence of locations per client
    """

    last_coords = app.storage.get_all_coords()

    return jsonify(last_coords)


@app.route("/coordinates/last", methods=['GET'])
def get_last_coords():

    """
        HTTP Endpoint to access the most recent location per client
    """

    last_coords = app.storage.get_last_coords()

    return jsonify(last_coords)

@app.route("/estimations/all", methods=["GET"])
def all_estimations():

    raise NotImplementedError


@app.route("/estimations/last", methods=["GET"])
def last_estimations():

    raise NotImplementedError


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)
