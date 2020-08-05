import pytest
from flask import Flask

from vulnpy.flask.blueprint import vulnerable_blueprint


@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)
    app.register_blueprint(vulnerable_blueprint)
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/vulnpy/")
    assert response.status_code == 200


def test_cmdi_os_system_get(client):
    response = client.get("/vulnpy/cmdi/os-system/?user_input=echo%20attack")
    assert int(response.get_data()) == 0


def test_cmdi_os_system_post(client):
    response = client.post(
        "/vulnpy/cmdi/os-system/", data={"user_input": "echo attack"}
    )
    assert int(response.get_data()) == 0


def test_cmdi_os_system_bad_command(client):
    response = client.get("/vulnpy/cmdi/os-system/?user_input=foo")
    assert int(response.get_data()) != 0


def test_cmdi_os_system_invalid_input(client):
    response = client.get("/vulnpy/cmdi/os-system/?ignored_param=bad")
    assert response.status_code == 200


def test_cmdi_subprocess_popen_get(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen/?user_input=echo%20attack")
    assert response.get_data() == b"attack\n"


def test_cmdi_subprocess_popen_post(client):
    response = client.post(
        "/vulnpy/cmdi/subprocess-popen/", data={"user_input": "echo attack"}
    )
    assert response.get_data() == b"attack\n"


def test_cmdi_subprocess_popen_bad_command(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen/?user_input=foo")
    assert response.status_code == 200


def test_cmdi_subprocess_popen_invalid_input(client):
    response = client.get("/vulnpy/cmdi/os-system/?ignored_param=bad")
    assert response.status_code == 200
