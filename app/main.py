from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routers import health
from app.core.database import dispose_engine
from app.core.redis import close_redis, init_redis
from app.core.settings import settings


templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_redis()
    try:
        yield
    finally:
        await close_redis()
        await dispose_engine()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(health.router, tags=["health"], prefix=settings.API_PREFIX)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home"})
