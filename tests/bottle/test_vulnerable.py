import pytest
from bottle import Bottle
from vulnpy.bottle import add_vulnerable_routes
from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers
from webtest import TestApp


@pytest.fixture(scope="module")
def client():
    app = Bottle(__name__)
    add_vulnerable_routes(app)
    return TestApp(app)


@parametrize_root
def test_root_views(client, view_path):
    response = client.get(view_path)
    assert response.status_code == 200


@parametrize_triggers
@pytest.mark.parametrize("request_method", ["get", "post"])
def test_trigger(client, request_method, view_name, trigger_name):
    get_or_post = getattr(client, request_method)

    data = DATA[view_name]

    if view_name == "unsafe_code_exec":
        data = "'{}'".format(data)

    print(data)
    response = get_or_post(
        "/vulnpy/{}/{}?user_input={}".format(view_name, trigger_name, data),
        {"user_input": DATA[view_name]},
    )
    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(DATA.get(view_name)) in str(response.text)
