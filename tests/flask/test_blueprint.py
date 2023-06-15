import pytest
from flask import Flask

from vulnpy.flask.blueprint import vulnerable_blueprint

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers


@pytest.fixture(scope="module")
def client():
    app = Flask(__name__)
    app.register_blueprint(vulnerable_blueprint)
    with app.test_client() as client:
        yield client


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

    response = get_or_post(
        "/vulnpy/{}/{}/".format(view_name, trigger_name),
        query_string={"user_input": data},
        data={"user_input": data},
    )
    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(data) in str(response.get_data())


def test_trigger_header_source(client):
    data = DATA["cmdi"]

    response = client.get("/vulnpy/cmdi/os-system", headers={"user_input": data})

    assert response.status_code == 200
