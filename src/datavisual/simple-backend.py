from flask import Flask, jsonify, json

from storage import StorageAdapter

app = Flask(__name__)
app.storage = StorageAdapter()


def sanitize_json(json_data):
    _san_json = json.dumps(json_data, default=str)

    return json.loads(_san_json)


@app.route("/messages/all", methods=["GET"])
def all_messages():

    records = app.storage.get_all_msgs()

    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


@app.route("/messages/last", methods=["GET"])
def last_messages():

    records = app.storage.get_last_msgs()

    sanitized_records = sanitize_json(records)

    return jsonify(sanitized_records)


@app.route("/clients/all", methods=['GET'])
def all_clients():

    clients = app.storage.get_clients()

    return jsonify(clients)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)