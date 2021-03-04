import pytest
import docker as docker_client
import os

@pytest.fixture(scope="session")
def docker():
    return docker_client.from_env()

@pytest.fixture(scope="session")
def container_image(docker):
    docker.images.build(
        path='.',
        tag='ml-paper-topic-modelling',
        rm=False,
        nocache=False
    )