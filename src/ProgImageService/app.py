#!/usr/bin/env python
# TODO: route traffic with v1 path prefix
import io
import uuid

from flask import Flask, Response, abort, request
from PIL import Image

from . import storage

app = Flask(__name__)
store = storage.InMemoryStorage()


@app.route("/storage/", methods=("PUT",))
def storage_put():
    # this is a random UUID as it avoids the need for syncronisation when generating a new identifier
    key = uuid.uuid4()
    data = request.files.get("data")
    if data is None:
        abort(400, Response("data not provided"))
    store.put(key, data.stream.read())
    return Response(str(key))


@app.route("/storage/<uuid:key>", methods=("GET",))
def storage_get(key):
    try:
        return Response(store.get(key), mimetype="image")
    except storage.ObjectNotFound:
        abort(404)


@app.route("/storage/<uuid:key>.<string:extension>", methods=("GET",))
def storage_get_transform(key, extension):
    extension = extension.lower()
    try:
        bytes_in = store.get(key)
    except storage.ObjectNotFound:
        abort(404)

    image = Image.open(io.BytesIO(bytes_in))
    bytes_out = io.BytesIO()
    try:
        # pillow raises a KeyError if the format is not known
        image.save(bytes_out, extension)
    except KeyError:
        abort(400, f"invalid extension type {extension!r}")
    return Response(bytes_out.getvalue(), mimetype=f"image/{extension}")
