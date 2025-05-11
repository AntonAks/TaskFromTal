from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

import asyncio
from contextlib import asynccontextmanager

from charts import SimpleCharts
from tasks import data_sync_task


# ======= Background async task ========
async def background_worker() -> None:
    while True:
        print("Background task started!")
        await data_sync_task()
        print("Background task finished.")
        await asyncio.sleep(60)


@asynccontextmanager  # type: ignore[arg-type]
async def lifespan(app: FastAPI) -> None:  # type: ignore[misc]
    bg_task = asyncio.create_task(background_worker())
    yield
    bg_task.cancel()
    try:
        await bg_task
    except asyncio.CancelledError:
        print("Background task was cancelled")


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
async def root(request: Request) -> HTMLResponse:
    top_n = int(request.query_params.get("top", 10))
    content = SimpleCharts.get_chars(top_n)
    return HTMLResponse(content=content)
