import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from time import sleep
from asyncio import sleep as async_sleep
from vulnpy.fastapi import vulnerable_routes
from vulnpy.trigger.cmdi import do_os_system

app = FastAPI()
app.include_router(vulnerable_routes)

if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.fastapi import ContrastMiddleware

    app.add_middleware(ContrastMiddleware, original_app=app)


@app.get("/")
def read_root():
    return RedirectResponse("/vulnpy")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/files/upload")
async def upload_return_large_file(file: UploadFile = File(...)):
    content = await file.read()
    do_os_system(content[:20])
    return {"result": "success"}


@app.get("/cmdi")
def cmdi(user_input: str):
    cmd = "echo " + user_input + " this should be echoed"
    print("Started app view")
    for i in range(10):
        print("will echo command")
        os.system(cmd)
        print("about to sleep")
        sleep(3)
        print("done sleeping")
    print("Finished app view")


@app.get("/async_will_block")
async def async_will_block():
    # Blocking call in async route
    # Async routes run on the main thread and are expected
    # to never block for any significant period of time.
    # sleep() is blocking, so the main thread will stall
    # and all other requests will be blocked
    sleep(10)
    return {"Async Route": "This will be a blocking call"}


@app.get("/sync_no_block")
def sync_no_block():
    # Blocking calls on sync route
    # Sync routes are run in a separate thread from a threadpool,
    # so any blocking will not affect the main thread so any other
    # request will still be processed
    sleep(10)
    return {"Sync Route": "This should not be a blocking call"}


@app.get("/async_no_block")
async def async_no_block():
    # Awaiting coroutines on async routes
    # Awaiting an async function causes it to yield the main thread
    # while it's waiting for an operation to complete, so it's not blocking the thread.
    # asyncio.sleep(), unlike time.sleep(), is an async function, so it can be awaited.
    await async_sleep(10)
    return {"Async Route with async sleep": "This should not be a blocking call"}
