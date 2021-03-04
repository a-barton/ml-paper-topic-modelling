import pytest
import requests
import time

##############
## FIXTURES ##
##############

@pytest.fixture(scope="module")
def app_container(docker):
    container = docker.containers.run(
        'ml-paper-topic-modelling',
        remove=True,
        detach=True,
        ports= {5000 : 5000},
        stdout=True,
        stderr=True
    )
    time.sleep(3) # Let gunicorn boot up
    yield container
    container.kill()


###########
## TESTS ##
###########

def test_container_responds_to_ping(app_container):
    r = requests.get("http://localhost:5000/ping")
    print(r)
    if r.status_code == 200:
        assert True
    else:
        pytest.fail(f"Container ping failed.  Response message: {r.text}")


def test_predict_topics(app_container):
    headers = {'Content-Type' : 'text/xml'}
    payload = {'text' : 'neural network'}
    r = requests.post(
        'http://localhost:5000/topics',
        data=payload,
        headers=headers
    )
    pytest.fail(r.text)