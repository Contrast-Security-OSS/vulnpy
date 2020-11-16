import pytest
from webtest import TestApp

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers

from vulnpy.wsgi import vulnerable_app


@pytest.fixture(scope="module")
def client():
    return TestApp(vulnerable_app)


@parametrize_root
def test_root_views(client, view_path):
    response = client.get(view_path)
    assert response.status_int == 200


@parametrize_triggers
def test_trigger(client, view_name, trigger_name):
    response = client.get(
        "/vulnpy/{}/{}".format(view_name, trigger_name),
        {"user_input": DATA[view_name]},
    )
    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(DATA.get(view_name)) in str(response.text)


@pytest.mark.parametrize(
    "path", ["", "/", "/notvulnpy", "/vulnpy/foo", "/vulnpy/cmdi/bar"]
)
def test_not_found(client, path):
    response = client.get(path, status=404)
    assert response.text == "The requested page does not exist"
