import pytest
from pyramid.config import Configurator
from webtest import TestApp


@pytest.fixture(scope="module")
def client():
    config = Configurator()
    config.include("vulnpy.pyramid.vulnerable_routes")
    app = config.make_wsgi_app()
    return TestApp(app)


def test_home(client):
    response = client.get("/vulnpy/")
    assert response.status_int == 200


def test_cmdi_basic(client):
    response = client.get("/vulnpy/cmdi")
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_cmdi_os_system_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post("/vulnpy/cmdi/os-system", {"user_input": "echo attack"})
    assert response.status_int == 200


def test_cmdi_os_system_bad_command(client):
    response = client.get("/vulnpy/cmdi/os-system", {"user_input": "foo"})
    assert response.status_int == 200


def test_cmdi_os_system_invalid_input(client):
    response = client.get("/vulnpy/cmdi/os-system", {"ignored_param": "bad"})
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_cmdi_subprocess_popen_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/cmdi/subprocess-popen", {"user_input": "echo attack"}
    )
    assert response.status_int == 200


def test_cmdi_subprocess_popen_bad_command(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen", {"user_input": "foo"})
    assert response.status_int == 200


def test_cmdi_subprocess_popen_invalid_input(client):
    response = client.get("/vulnpy/cmdi/subprocess-popen", {"ignored_param": "bad"})
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_deserialization_pickle_load_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/deserialization/pickle-load",
        {"user_input": "csubprocess\ncheck_output\n(S'ls'\ntR."},
    )
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_deserialization_pickle_loads_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/deserialization/pickle-loads",
        {"user_input": "csubprocess\ncheck_output\n(S'ls'\ntR."},
    )
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_deserialization_yaml_load_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/deserialization/yaml-load",
        {
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
def test_deserialization_yaml_load_all_normal(client, method_name):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/deserialization/yaml-load-all",
        {
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_int == 200


@pytest.mark.parametrize("method_name", ["get", "post"])
@pytest.mark.parametrize("endpoint", ["eval", "exec", "compile"])
def test_unsafe_code_exec(client, method_name, endpoint):
    get_or_post = getattr(client, method_name)
    response = get_or_post(
        "/vulnpy/unsafe_code_exec/{}".format(endpoint),
        {"user_input": "1 + 2"},
    )
    assert response.status_code == 200
