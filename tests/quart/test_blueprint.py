import pytest
from quart import Quart

from vulnpy.quart.blueprint import vulnerable_blueprint

from vulnpy.trigger import DATA
from tests import parametrize_root, parametrize_triggers


@pytest.fixture(scope="module")
def app():
    app = Quart(__name__)
    app.register_blueprint(vulnerable_blueprint)
    yield app


@pytest.mark.asyncio
@parametrize_root
async def test_root_views(app, view_path):
    client = app.test_client()
    response = await client.get(view_path)
    assert response.status_code == 200


@pytest.mark.asyncio
@parametrize_triggers
@pytest.mark.parametrize("request_method", ["get", "post"])
async def test_trigger(app, request_method, view_name, trigger_name):
    client = app.test_client()

    get_or_post = getattr(client, request_method)

    data = DATA[view_name]

    if view_name == "unsafe_code_exec":
        data = "'{}'".format(data)

    response = await get_or_post(
        "/vulnpy/{}/{}/?user_input={}".format(view_name, trigger_name, data),
        data={"user_input": data},
    )
    assert response.status_code == 200

    if view_name == "xss":
        assert "<p>XSS: {}</p>".format(data) in str(await response.get_data())


@pytest.mark.asyncio
async def test_trigger_header_source(app):
    data = DATA["cmdi"]

    client = app.test_client()
    response = await client.get("/vulnpy/cmdi/os-system", headers={"user_input": data})

    assert response.status_code == 200
