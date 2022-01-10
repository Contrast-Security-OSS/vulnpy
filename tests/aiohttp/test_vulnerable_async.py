import pytest

import sys

if sys.version_info < (3, 7):
    pytest.skip("Aiohttp support is Python 3.7+ only", allow_module_level=True)

from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer, loop_context
from vulnpy.aiohttp import vulnerable_routes  # noqa: E402

from vulnpy.trigger import DATA  # noqa: E402
from tests import parametrize_root, parametrize_triggers  # noqa: E402


def _create_example_app():
    app = web.Application()
    app.add_routes(vulnerable_routes)
    return app


@parametrize_root
def test_root_views(view_path):
    with loop_context() as loop:

        @pytest.mark.asyncio
        async def test_root_views():
            app = _create_example_app()
            async with TestClient(TestServer(app), loop=loop) as client:
                response = await client.get(view_path)
                assert response.status == 200

        loop.run_until_complete(test_root_views())


@parametrize_triggers
def test_trigger_views(view_name, trigger_name):
    with loop_context() as loop:

        @pytest.mark.asyncio
        async def test_root_views():
            app = _create_example_app()
            async with TestClient(TestServer(app), loop=loop) as client:
                data = DATA[view_name]
                if view_name == "unsafe_code_exec":
                    data = "'{}'".format(data)

                response = await client.get(
                    "/vulnpy/{}/{}".format(view_name, trigger_name),
                    params={"user_input": data},
                )

                assert response.status == 200

                if view_name == "xss":
                    text = await response.text()
                    assert "<p>XSS: {}</p>".format(data) in str(text)

        loop.run_until_complete(test_root_views())
