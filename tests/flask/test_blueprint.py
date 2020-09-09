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


def test_cmdi_basic(client):
    response = client.get("/vulnpy/cmdi")
    assert response.status_code == 200


def test_deserialization_basic(client):
    response = client.get("/vulnpy/deserialization")
    assert response.status_code == 200


def test_cmdi_os_system_get(client):
    response = client.get("/vulnpy/cmdi/os-system/?user_input=echo%20attack")
    assert response.status_code == 200


def test_cmdi_os_system_post(client):
    response = client.post(
        "/vulnpy/cmdi/os-system/", data={"user_input": "echo attack"}
    )
    assert response.status_code == 200


def test_cmdi_os_system_bad_command(client):
    response = client.get("/vulnpy/cmdi/os-system/?user_input=foo")
    assert response.status_code == 200


def test_cmdi_os_system_invalid_input(client):
    response = client.get("/vulnpy/cmdi/os-system/?ignored_param=bad")
    assert response.status_code == 200


def test_cmdi_subprocess_popen_get(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen/?user_input=echo%20attack")
    assert response.status_code == 200


def test_cmdi_subprocess_popen_post(client):
    response = client.post(
        "/vulnpy/cmdi/subprocess-popen/", data={"user_input": "echo attack"}
    )
    assert response.status_code == 200


def test_cmdi_subprocess_popen_bad_command(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen/?user_input=foo")
    assert response.status_code == 200


def test_cmdi_subprocess_popen_invalid_input(client):
    response = client.get("/vulnpy/cmdi/os-system/?ignored_param=bad")
    assert response.status_code == 200


def test_deserialization_pickle_load_get(client):
    response = client.get(
        "/vulnpy/deserialization/pickle-load/?user_input={}".format(
            "csubprocess\ncheck_output\n(S'ls'\ntR."
        )
    )
    assert response.status_code == 200


def test_deserialization_pickle_load_post(client):
    response = client.post(
        "/vulnpy/deserialization/pickle-load/",
        data={"user_input": "csubprocess\ncheck_output\n(" "S'ls'\ntR."},
    )
    assert response.status_code == 200


def test_deserialization_pickle_loads_get(client):
    response = client.get(
        "/vulnpy/deserialization/pickle-loads/?user_input={}".format(
            "csubprocess\ncheck_output\n(S'ls'\ntR."
        )
    )
    assert response.status_code == 200


def test_deserialization_pickle_loads_post(client):
    response = client.post(
        "/vulnpy/deserialization/pickle-loads/",
        data={"user_input": "csubprocess\ncheck_output\n(S'ls'\ntR."},
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_get(client):
    response = client.get(
        "/vulnpy/deserialization/yaml-load/?user_input={}".format(
            '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        )
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_post(client):
    response = client.post(
        "/vulnpy/deserialization/yaml-load/",
        data={
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_all_get(client):
    response = client.get(
        "/vulnpy/deserialization/yaml-load-all/?user_input={}".format(
            '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        )
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_all_post(client):
    response = client.post(
        "/vulnpy/deserialization/yaml-load-all/",
        data={
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_code == 200
