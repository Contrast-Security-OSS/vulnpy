import mock
import pytest
import falcon

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


def test_cmdi_os_system_normal(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"user_input": "echo attack"}
    )
    assert int(response.content) == 0


def test_cmdi_os_system_bad_command(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"user_input": "foo"}
    )
    assert int(response.content) != 0


def test_cmdi_os_system_invalid_input(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/os-system", params={"ignored_param": "bad"}
    )
    assert int(response.content) == 0
    assert response.status_code == 200


def test_cmdi_subprocess_popen_normal(client):
    response = client.simulate_get(
        "/vulnpy/cmdi/subprocess-popen", params={"user_input": "echo attack"}
    )
    assert response.content == b"attack\n"


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
    assert response.content == b"something bad happened"


def test_cmdi_base_class():
    handler = vulnpy.falcon.vulnerable.Cmdi()
    with pytest.raises(NotImplementedError):
        handler.trigger()
