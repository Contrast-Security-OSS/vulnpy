import pytest
from pyramid.config import Configurator
from webtest import TestApp

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers


@pytest.fixture(scope="module")
def client():
    config = Configurator()
    config.include("vulnpy.pyramid.vulnerable_routes")
    app = config.make_wsgi_app()
    return TestApp(app)


@parametrize_root
def test_root_views(client, view_path):
    response = client.get(view_path)
    assert response.status_int == 200


@parametrize_triggers
@pytest.mark.parametrize("request_method", ["get", "post"])
def test_trigger(client, request_method, view_name, trigger_name):
    get_or_post = getattr(client, request_method)
    response = get_or_post(
        "/vulnpy/{}/{}".format(view_name, trigger_name),
        {"user_input": DATA[view_name]},
    )
    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(DATA.get(view_name)) in str(response.text)
