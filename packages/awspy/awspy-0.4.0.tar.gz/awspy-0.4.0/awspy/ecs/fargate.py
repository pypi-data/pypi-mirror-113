import os
import requests
import json

from awspy import AwsPy
from typing import Any


class Fargate(AwsPy):
    """
    Utilities for working with containers running on Fargate backed ECS
    NOT suitable for use with ECS tasks running on EC2 instances
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.ecs_container_metadata_uri_v4: str = os.environ.get(
            "ECS_CONTAINER_METADATA_URI_V4", ""
        )

    def get_container_metadata_v4(self) -> dict:
        """
        Extract the Fargate container metadata, injected into the running container by ECS.
        Note: This returns metadata for the current running container, NOT the task
        See https://docs.aws.amazon.com/AmazonECS/latest/userguide/task-metadata-endpoint-v4-fargate.html
        Requires Fargate platform version 1.4.0
        :return: ECS metadata dictionary:
            {
                "DockerId": "cd189a933e5849daa93386466019ab50-2495160603",
                "Name": "curl",
                "DockerName": "curl",
                "Image": "111122223333.dkr.ecr.us-west-2.amazonaws.com/curltest:latest",
                "ImageID": "sha256:25f3695bedfb454a50f12d127839a68ad3caf91e451c1da073db34c542c4d2cb",
                ...
            }
        :raises: requests.exceptions.RequestException, json.decoder.JSONDecodeError, RuntimeError
        """
        try:
            request = requests.get(self.ecs_container_metadata_uri_v4, timeout=3)
            if request.status_code == 200:
                json_metadata: str = request.json()
                return json_metadata
            else:
                raise RuntimeError(
                    f"Inappropriate response from metadata endpoint: {request.text}"
                )
        except Exception as e:
            if self._raise_errors:
                raise e
            else:
                self._logger.error(
                    f"Unable to read container metadata for endpoint: {self.ecs_container_metadata_uri_v4}: {e}"
                )
            return {}
