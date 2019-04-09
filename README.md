# ProgImage.com mock

## Use

This HTTP service allows you to upload an image, which can later be retrieved using the returned handle.

To upload an image, you send a PUT request to `/storage/` with a parameter called _data_ which contains the image file. The response to this will be a string that can be used to refer to the image in later requests.

To download the original image, you send a GET request to `/storage/$reference`, where _$reference_ is the string you recived from the PUT request.

To download the image in using a new container format, you send a GET request to `/storage/$reference.$extention`, where _$extension_ is one of the supported format types.

The supported input/output format types come from [pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) 6.0.0, which includes some exotic types, as well as types which can only be read from or written from.


### Common status codes

 * 200 - returned for successful requests
 * 400 - indicates that the request had invalid parameters, such as a missing the _data_ parameter, or trying to convert to an invalid file format
 * 404 - the image being refered to does not exist
 * 500 - an unsupported case was encountered


### Example
Below is an example session using [curl](https://linux.die.net/man/1/curl) in a bash shell:
```
$ host=http://127.0.0.1:5000
$ image="$HOME/Downloads/image.jpg"
$ uuid=$(curl -X PUT ${host}/storage/ -F data=@"${image}")
$ echo $uuid
72b96d40-7971-465f-ab53-746a14a68acd
$ curl $host/storage/${uuid} | file --brief --mime-type -
image/jpeg
$ curl $host/storage/${uuid}.bmp | file --brief --mime-type -
image/x-ms-bmp
```


## Running
Requirements:

 * [`pipenv`](https://github.com/pypa/pipenv)
 * Python3 (tested on python3.7)

From the repo base run:

```
pipenv install
FLASK_APP=src/ProgImageService/app.py pipenv run flask run
```
This will run the service on `http://127.0.0.1:500/`

In production you would want to run this through a WSGI server like gunicorn, which in turn reccomends using a reverse proxy like nginx or HAProxy in front.

## Tests
Currently the tests only cover linting and basic storage unit testing, integration testing is a later step.
```
pipenv install --dev
pipenv run pytest
```

The tests suite will also produce a coverage report under `./reports/coverage/index.html`.

## Note
Given the broad problem description, a service like [imaginary](https://github.com/h2non/imaginary) would probably be a part of a good solution.