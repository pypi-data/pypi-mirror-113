#!/usr/bin/python3
from enum import Enum
import time

# Local imports
from tometrics.lib.influxdb import InfluxDBClient


class UnsupportedClient(Exception):
    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class ClientTypes(Enum):
    influxDB = "InfluxDB"


class ToMetrics:
    """
    A wrapper for easily pushing metrics to a backend.

    Note: current implementation is not mean for high frequency pushing (no buffering is used)
    :param bucket The bucket/table/database we are pushing data into.
    :param static_metric_name If we only are pushing one type of value, we can optionally just set the name once
    :param static_metric_tags If there are tags that do not change for all the data we are pushing, we can set those once
    """

    def __init__(
        self,
        backend_url: str,
        client_type: ClientTypes,
        # Data specific params
        bucket: str,
        static_metric_name: str = None,
        static_metric_tags: map = {},
        # Additional optional args
        username: str = None,
        password: str = None,
        verbose: bool = True,
    ):
        print(f'Initializing metrics streaming to {client_type} via "{backend_url}"')

        # Init member vars
        self.backend_url = backend_url.rstrip("/")
        self.client_type = client_type
        self.username = username
        self.password = password
        self.verbose = verbose

        self.bucket = bucket
        self.static_metric_name = static_metric_name
        self.static_metric_tags = static_metric_tags

        # Setup the client
        self.client = None
        if client_type == ClientTypes.influxDB:
            self.client = InfluxDBClient(self.backend_url, self.bucket)
        else:
            raise UnsupportedClient(f"{client_type} is currently not supported")

    def send(self, name: str, value: float, tags: map = {}, timestamp_override=None):
        """
        Simply delegate to the client to send a datum.
        TODO we could do some helpful caching of the name if we only plan to send one type of value?
        TODO ^ also for tags
        """
        timestamp = timestamp_override or time.time_ns()
        all_tags = self.static_metric_tags
        all_tags.update(tags)

        # TODO add the static stuffssss
        self.client.send(timestamp, name, value, all_tags)
