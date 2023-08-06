#!/usr/bin/python3
import requests

# Local imports
from tometrics.lib.generic_interface import GenericInterface


class FailedBucketCreation(Exception):
    def __init__(self, message="Unknown", errors={}):
        super().__init__(message)
        self.errors = errors


class InfluxDBClient(GenericInterface):
    def __init__(self, backend_url: str, bucket: str):
        self.backend_url = backend_url
        self.bucket = bucket

        # Create the db if it does not exist
        # curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE mydb"
        response = requests.post(
            f"{self.backend_url}/query",
            params={"q": f"CREATE DATABASE {self.bucket}"},
        )
        if response.status_code != 200:
            print(response.text)
            raise FailedBucketCreation(f"Failed to create database {self.bucket}")

    def send(
        self,
        timestamp_ns: int,
        name: str,
        value: float,
        tags: map = {},
    ):
        """
        curl -i -XPOST 'http://localhost:8086/write?db=mydb' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'"""
        formatted_tags = ""
        for k, v in tags.items():
            formatted_tags += f",{k}={v}"

        response = requests.post(
            f"{self.backend_url}/write?db={self.bucket}",
            f"{name}{formatted_tags} value={str(value)} {timestamp_ns}",
        )
        if response.status_code != 204:
            print(response.text, response.status_code)
            print(f"Failed to push {name} metric at {timestamp_ns}")
