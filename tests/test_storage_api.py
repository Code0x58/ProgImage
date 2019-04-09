import imghdr
import io
import os
import uuid

from ProgImageService.app import app

import pytest


@pytest.fixture(scope="function")
def client():
    yield app.test_client()


@pytest.fixture(scope="session")
def image():
    path = os.path.join(os.path.dirname(__file__), "EEEEEE-1.png")
    with open(path, "rb") as f:
        image = f.read()
    return image


def test_storage(client, image):
    key = uuid.uuid4()
    r = client.get()

    # valid PUT
    r = client.put("/storage/", data={"data": (io.BytesIO(image), "image.png")})
    assert r.status_code == 200
    key = uuid.UUID(r.get_data(as_text=True), version=4)

    # valid non-transforming GET
    r = client.get(f"/storage/{key}")
    assert r.content_type == "image"
    assert r.status_code == 200
    assert r.data == image
    assert imghdr.what(None, h=r.data) == "png"

    # valid transforming GET
    r = client.get(f"/storage/{key}.bmp")
    assert r.content_type == "image/bmp"
    assert r.status_code == 200
    assert imghdr.what(None, h=r.data) == "bmp"

    # transforming GET with invalid extension
    r = client.get(f"/storage/{key}.bad")
    assert r.status_code == 400


def test_bad_storage_calls(client):
    # bad request, no data
    r = client.put("/storage/")
    assert r.status_code == 400

    # unsupported methods
    r = client.delete(f"/storage/{uuid.uuid4()}")
    assert r.status_code == 405

    r = client.put(f"/storage/{uuid.uuid4()}")
    assert r.status_code == 405


def test_get_missing(client):
    key = uuid.uuid4()

    r = client.get(f"/storage/{key}")
    assert r.status_code == 404

    r = client.get(f"/storage/{key}.bmp")
    assert r.status_code == 404
