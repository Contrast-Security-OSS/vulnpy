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
def test_root_views(client, view_name):
    if view_name == "home":
        response = client.get("/vulnpy")
    else:
        response = client.get("/vulnpy/{}".format(view_name))
    assert response.status_code == 200


@parametrize_triggers
@pytest.mark.parametrize("request_method", ["get", "post"])
def test_trigger(client, request_method, view_name, trigger_name):
    get_or_post = getattr(client, request_method)

    data = DATA.get(view_name)

    if view_name == "unsafe_code_exec":
        data = "'{}'".format(data)

    response = get_or_post(
        "/vulnpy/{}/{}/?user_input={}".format(view_name, trigger_name, data),
        data={"user_input": data}
    )
    assert response.status_code == 200
