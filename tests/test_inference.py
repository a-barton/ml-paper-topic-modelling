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

######################
## HELPER FUNCTIONS ##
######################

def post_minimal_payload(url='http://localhost:5000/topics', payload={'text':'neural network'}):
    return requests.post(url, data=payload)

###########
## TESTS ##
###########

def test_container_responds_to_ping(app_container):
    resp = requests.get("http://localhost:5000/ping")
    if resp.status_code == 200:
        assert True
    else:
        pytest.fail(f"Container ping failed.  Response message: {resp.text}")


def test_predict_returns_topics_page(app_container):
    resp = post_minimal_payload()
    assert "<title>ML Paper Topic Modelling - Predictions</title>" in resp.text


def test_predict_topics_returns_chart(app_container):
    resp = post_minimal_payload()
    assert '<div class="chart">' in resp.text
    assert '<script type="text/javascript">window.Plotly' in resp.text