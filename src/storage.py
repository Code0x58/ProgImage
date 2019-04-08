import abc


class ApplicationException(Exception):
    """Base for exceptions managed within the application."""


class ObjectNotFound(ApplicationException):
    """Exception raised when an object is not found in a store."""


class StorageBackend(metaclass=abc.ABCMeta):
    """Abstract storage interface.

    Chose this over github.com/okfn/ofs just to demo simple code, plus could have debate on using
    something like ofs without futher investigation of the library, and choosing storage backends.
    Could have used something like django-storage but using django feels too heavy with a lot of
    boilerplate for this exercise.

    """

    @abc.abstractmethod
    def put(self, key: str, data: bytes) -> None:
        return None

    @abc.abstractmethod
    def get(self, key: str) -> bytes:
        return b""


class InMemoryStorage(StorageBackend):
    """In memory storage backend primarily for testing.

    >>> store = InMemoryStorage()
    >>> store.put("foo", b"bar")
    >>> store.get("foo")
    b'bar'
    >>> try:
    ...     store.get("missing")
    ... except ObjectNotFound:
    ...     print("error")
    ... else:
    ...     pass
    error
    """

    def __init__(self):
        self.store = {}

    def put(self, key: str, data: bytes) -> None:
        self.store[key] = data

    def get(self, key: str) -> bytes:
        try:
            return self.store[key]
        except KeyError:
            raise ObjectNotFound()
