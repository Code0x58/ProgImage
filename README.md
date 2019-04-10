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

### Local
Requirements:

* Python3 (tested on python3.7)
* [`pipenv`](https://github.com/pypa/pipenv)

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

## Questions
Some non-exhaustive responses to the questions:

### What language platform did you select to implement the microservice? Why?
Python3 on Linux/POSIX operating systems, possibly any Python3 supported OS (limited by dependencies).
 * a language mutually familiar with
 * a good environment to rapidly develop in

### How did you store the uploaded images?
In memory using a simple put/get interface which should be easy to extend with additional backends. This allows easy testing, and leaves the details/discussion on backends open.

### What would you do differently to your implementation
Given the broad bigger problem description, I would probably look at using a service like [imaginary](https://github.com/h2non/imaginary) as it already implements a lot of features, appears to have a decent community, and is written in go.

With a specific list of supported formats, and more information on use along with demands and available resources, it may be reasonable to pre-compute the different image formats and serve them via a CDN.

### How would coordinate your development environment to handle the build and test process?
I have linters integrated with my editor, so get feedback as I save changes. Running the tests locally is a single line straightforward line so I would probably run the commands by hand, but I would add a CI pipeline to GitHub (GitHub actions are really nice) so that my commits are always tested, even if not locally.

### What technologies would you use to ease the task of deploying the microservices to a production runtime environment?
If it was available, I would use a tool like Flux or Argo-CD to deploy manifests to Kubernetes custer(s) when an image/manifest repository is updated. When the CI/CD of the images is separate, it allows good disaster recovery when there are cluster issues (including a new cluster).

Testing as a part of CI/CD could occur within a container, against the container, against manifests, and against releases (e.g. through canary releases).

### What testing did (or would) you do, and why?
I started off with doctests for the in-memory backend as they are just documentation. I then did manual testing on the API, and did the rest of the automated testing for the 3rd task.

I would be tempted to add `mypy` to do type checking if the service was getting larger.

### What is the scaling capability of your solution? At what point would you need to change the architecture and why?
The current solution sould scale vertically and horizontally - the core code is pretty flexible and doesn't depend on locks/syncing. The code speed, backend choice, and deployment (e.g using horizontal pod autoscaling or kubeless' lambdas, multi-cluster ingress) would probably be parts to focus on for scaling. I imagine that the lifecycle of images may need considering, e.g. for their retention and target durability.

### What scenarios can you foresee where your solution can be misused? How would you protect your solution against such situations?
Given the lack of limitation, it could be used to store any content and serve it anyway, so very easy to abuse. If misuse would be a problem, auditing and limiting use (e.g. via authentication) could be options.

### What are the potential attack vectors on your solution and how would you protect your solution against them?
 * oversized image files - put a limit on upload sizes
 * invalid image uploads which would cause failures during the transform operation - validate the image on upload
 * payloads intended on exploiting the underlying libraries, e.g. pillow (C?) - keep libraries up to date and scan for issues + minimise access + have disaster recovery plan for data
 * DoS by saturating serving potential - offload concerns to a CDN
 * incurring excessive cost/saturating storage potential - audit and limit access to uploads
 * uploads of pathological images e.g. absurd in-memory dimensions which can be a small file due to compression - place checks on uploads
