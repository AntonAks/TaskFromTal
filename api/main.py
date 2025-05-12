import uvicorn
from fastapi import FastAPI, APIRouter
from routers.study import router as study_router
from routers.analysis import router as analysis_router

app = FastAPI(title="Scraper API", version="1.0.0")
api_router = APIRouter()

api_router.include_router(study_router)
api_router.include_router(analysis_router)

app.include_router(
    api_router,
    prefix="/api",
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8888, host="0.0.0.0", reload=True)
