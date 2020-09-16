import pytest
from django.conf import settings
from django.test import Client

from vulnpy.trigger import TRIGGER_MAP, DATA

vuln_names = [x for x in TRIGGER_MAP if x != "util"]

arglist = []
for vuln_name, trigger_names in TRIGGER_MAP.items():
    if not trigger_names:
        continue
    for trigger in trigger_names:
        arglist.append((vuln_name, trigger))


@pytest.fixture(scope="module")
def client():
    settings.configure(
        ROOT_URLCONF="vulnpy.django.vulnerable", ALLOWED_HOSTS=["testserver"]
    )
    return Client()


@pytest.mark.parametrize("view_name", vuln_names)
def test_root_views(client, view_name):
    if view_name == "home":
        response = client.get("/vulnpy")
    else:
        response = client.get("/vulnpy/{}".format(view_name))
    assert response.status_code == 200


@pytest.mark.parametrize("view_name,trigger_name", arglist)
@pytest.mark.parametrize("request_method", ["get", "post"])
def test_trigger(client, request_method, view_name, trigger_name):
    get_or_post = getattr(client, request_method)
    response = get_or_post(
        "/vulnpy/{}/{}".format(view_name, trigger_name),
        {"user_input": DATA.get(view_name)},
    )
    assert response.status_code == 200
