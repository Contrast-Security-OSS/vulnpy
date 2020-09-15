import mock
import pytest
import falcon
from six.moves.urllib_parse import quote

from falcon import testing

import vulnpy
import vulnpy.falcon


@pytest.fixture(scope="module")
def client():
    app = falcon.API()
    vulnpy.falcon.add_vulnerable_routes(app)
    return testing.TestClient(app)


def test_home(client):
    response = client.simulate_get("/vulnpy")
    assert response.status_code == 200


def test_cmdi_basic(client):
    response = client.simulate_get("/vulnpy/cmdi")
    assert response.status_code == 200


def test_cmdi_os_system_normal(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"user_input": "echo attack"}
    )
    assert response.status_code == 200


def test_cmdi_os_system_bad_command(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"user_input": "foo"}
    )
    assert response.status_code == 200


def test_cmdi_os_system_invalid_input(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"ignored_param": "bad"}
    )
    assert response.status_code == 200


def test_cmdi_subprocess_popen_normal(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/subprocess-popen", params={"user_input": "echo attack"}
    )
    assert response.status_code == 200


def test_cmdi_subprocess_popen_bad_command(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/subprocess-popen", params={"user_input": "foo"}
    )
    assert response.status_code == 200


def test_cmdi_subprocess_popen_invalid_input(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/subprocess-popen", params={"ignored_param": "bad"}
    )
    assert response.status_code == 200


@mock.patch(
    "vulnpy.trigger.cmdi.do_os_system", side_effect=Exception("something bad happened")
)
def test_handle_exception(mocked_trigger, client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system",
        params={"user_input": "something", "catch_exception": True},
    )
    assert mocked_trigger.called
    assert response.status_code == 200


def test_deserialization_basic(client):
    response = client.simulate_get("/vulnpy/deserialization")
    assert response.status_code == 200


def test_deserialization_pickle_load_normal(client):
    response = client.simulate_get(
        "/vulnpy/deserialization/pickle-load",
        params={"user_input": "csubprocess\ncheck_output\n(S'ls'\ntR."},
    )
    assert response.status_code == 200


def test_deserialization_pickle_loads_normal(client):
    response = client.simulate_get(
        "/vulnpy/deserialization/pickle-loads",
        params={"user_input": "csubprocess\ncheck_output\n(S'ls'\ntR."},
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_normal(client):
    response = client.simulate_get(
        "/vulnpy/deserialization/yaml-load",
        params={
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_code == 200


def test_deserialization_yaml_load_all_normal(client):
    response = client.simulate_get(
        "/vulnpy/deserialization/yaml-load-all",
        params={
            "user_input": '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]'
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", ["eval", "exec", "compile"])
def test_unsafe_code_exec_normal(client, endpoint):
    response = client.simulate_get(
        "/vulnpy/unsafe_code_exec/{}".format(endpoint),
        params={"user_input": quote("1 + 2")},
    )
    assert response.status_code == 200


def test_xxe_lxml_etree_fromstring_normal(client):
    response = client.simulate_get(
        "/vulnpy/xxe/lxml-etree-fromstring",
        params={"user_input": "<root>attack</root>"},
    )
    assert response.status_code == 200


def test_xxe_xml_dom_pulldom_parsestring_normal(client):
    response = client.simulate_get(
        "/vulnpy/xxe/xml-dom-pulldom-parsestring",
        params={"user_input": "<root>attack</root>"},
    )
    assert response.status_code == 200


def test_xxe_xml_sax_parsestring_normal(client):
    response = client.simulate_get(
        "/vulnpy/xxe/xml-sax-parsestring",
        params={"user_input": "<root>attack</root>"},
    )
    assert response.status_code == 200
