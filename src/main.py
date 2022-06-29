import uvicorn
from fastapi import FastAPI
from loguru import logger

from settings import settings
from utils.logger import use_loguru_for_logging
from routers import api_router

app = FastAPI()
use_loguru_for_logging(log_level=settings.log_level)
app.include_router(api_router)


if __name__ == "__main__":
    logger.info(settings)

    uvicorn.run(
        "main:app",
        host=settings.host, port=settings.port,
        log_level=settings.log_level.lower(),
        debug=settings.need_debug, reload=settings.need_reload)
