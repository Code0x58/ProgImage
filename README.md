# ProgImage.com mock

## Running
Requirements:

 * [`pipenv`](https://github.com/pypa/pipenv)
 * Python3 (tested on python3.7)

From the repo base run:

```
pipenv install
FLASK_APP=src/app.py pipenv run flask run
```

You can then upload an image with something like:
```
curl -X PUT http://127.0.0.1:5000/storage/ -F data=@$HOME/Downloads/image.jpg
```

The response from the above request will be a lone UUID which can be used to retrieve the image:
```
curl http://127.0.0.1:5000/storage/${response_uuid} | file -
```

In practice you'd probably want to run this through a WSGI server like gunicorn, which in turn reccomends a reverse proxy like nginx or HAProxy in front.

### Tests
Currently the tests only cover linting and basic storage unit testing, integration testing is a later step.
```
pipenv install --dev
pipenv run pytest
```

The tests suite will also produce a coverage report under `./reports/coverage/index.html`.

## Note
Given the broad problem description, a service like [imaginary](https://github.com/h2non/imaginary) would probably be a part of a good solution.
