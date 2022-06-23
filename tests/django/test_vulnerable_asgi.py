import pytest
from django.conf import settings
from django.test import AsyncClient

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers


@pytest.fixture(scope="module")
def client():
    if settings.configured:
        settings.ROOT_URLCONF = "vulnpy.django.vulnerable_asgi"
    else:
        settings.configure(
            ROOT_URLCONF="vulnpy.django.vulnerable_asgi",
            ALLOWED_HOSTS=["testserver"],
            DJANGO_ALLOW_ASYNC_UNSAFE="false",
        )
    return AsyncClient()


@parametrize_root
async def test_root_views(client, view_path):
    response = await client.get(view_path)
    assert response.status_code == 200


@parametrize_triggers
@pytest.mark.parametrize("request_method", ["get", "post"])
async def test_trigger(client, request_method, view_name, trigger_name):
    get_or_post = getattr(client, request_method)
    response = await get_or_post(
        path="/vulnpy/{}/{}".format(view_name, trigger_name),
        data={"user_input": DATA[view_name]},
        secure=True,
    )
    assert response.status_code == 200
    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(DATA.get(view_name)) in str(response.content)
