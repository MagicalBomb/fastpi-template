import uvicorn
from fastapi import FastAPI
from loguru import logger

from settings import settings
from utils.logger import use_loguru_for_logging

app = FastAPI()
use_loguru_for_logging(log_level=settings.log_level)


if __name__ == "__main__":
    logger.info(settings)

    uvicorn.run(
        "main:app",
        host=settings.host, port=settings.port,
        log_level=settings.log_level.lower(),
        debug=settings.need_debug, reload=settings.need_reload)
