import pytest
import sys

if sys.version_info <= (3, 6):
    pytest.skip("FastAPI support is Python 3.7+ only", allow_module_level=True)


from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from vulnpy.fastapi import vulnerable_routes  # noqa: E402

from vulnpy.trigger import DATA  # noqa: E402
from tests import parametrize_root, parametrize_triggers  # noqa: E402


@pytest.fixture(scope="module")
def client():
    app = FastAPI()
    app.include_router(vulnerable_routes)
    return TestClient(app)


@parametrize_root
def test_root_views(client, view_path):
    response = client.get(view_path)
    assert response.status_code == 200


@parametrize_triggers
def test_trigger(client, view_name, trigger_name):
    data = DATA[view_name]

    if view_name == "unsafe_code_exec":
        data = "'{}'".format(data)

    response = client.get(
        "/vulnpy/{}/{}/".format(view_name, trigger_name), params={"user_input": data}
    )

    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(data) in str(response.text)
