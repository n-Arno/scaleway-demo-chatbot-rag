#!/opt/app-root/bin/python3

from dotenv import load_dotenv

load_dotenv()

import logging, os, uvicorn, warnings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.ingest import do_ingest
from app.api.routers.chat import chat_router
from app.settings import init_settings

# Avoid ugly warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

init_settings()

app = FastAPI()

api = FastAPI(root_path="/api")
api.include_router(chat_router, prefix="/chat")


@api.get("/ingest")
async def ingester():
    do_ingest()
    return HTMLResponse(content="Done!", status_code=200)


app.mount("/api", api)
app.mount("/", StaticFiles(directory="front", html=True), name="static")


@app.on_event("startup")
async def startup():
    do_ingest()


environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8080"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)
