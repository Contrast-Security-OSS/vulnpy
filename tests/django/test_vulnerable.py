import pytest
from django.conf import settings
from django.test import Client

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers


@pytest.fixture(scope="module")
def client():
    settings.configure(
        ROOT_URLCONF="vulnpy.django.vulnerable", ALLOWED_HOSTS=["testserver"]
    )
    return Client()


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
    response = get_or_post(
        "/vulnpy/{}/{}".format(view_name, trigger_name),
        {"user_input": DATA.get(view_name)},
    )
    assert response.status_code == 200
