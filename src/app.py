#!/usr/bin/env python
# TODO: route traffic with v1 path prefix
import uuid

from flask import Flask, Response, abort, request

from . import storage

app = Flask(__name__)
store = storage.InMemoryStorage()


@app.route("/storage/", methods=("PUT",))
def storage_put():
    # this is a random UUID as it avoids the need for syncronisation when generating a new identifier
    key = uuid.uuid4()
    data = request.files.get("data")
    if data is None:
        abort(Response("data not provided"))
    store.put(key, data.stream.read())
    return Response(str(key))


@app.route("/storage/<uuid:key>", methods=("GET",))
def storage_get(key):
    try:
        return Response(store.get(key), mimetype="image")
    except storage.ObjectNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
