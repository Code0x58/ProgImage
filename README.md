# ProgImage.com mock

Requirements:

 * [`pipenv`](https://github.com/pypa/pipenv)
 * Python3 (tested on python3.7)

Useful:
 * `curl`

## Running
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

## Tests
Currently the tests only cover linting and basic storage unit testing, integration testing is a later step.
```
pipenv install --dev
pipenv run pytest
```


## Note
Given the broad problem description, a service like [imaginary](https://github.com/h2non/imaginary) would probably be a part of a good solution.
