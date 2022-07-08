import uvicorn
from fastapi import FastAPI
from loguru import logger

from settings import settings
from utils.datasource import setup_db
from utils.error_handle import init_error_handle
from utils.logger import use_loguru_for_logging
from routers import api_router
from utils.middlewares.sqlalchemy_ctx import DBMiddleware


use_loguru_for_logging(log_level=settings.log_level)

setup_db(settings)


def create_app():
    if settings.need_debug:
        app = FastAPI()
    else:
        app = FastAPI(docs_url=None, redoc_url=None)
    app.add_middleware(DBMiddleware, prefix_only="/api/v1")
    app.include_router(api_router, prefix="/api")
    init_error_handle(app)
    return app


app = create_app()


if __name__ == "__main__":
    logger.info(settings)

    uvicorn.run(
        "main:app",
        host=settings.host, port=settings.port,
        log_level=settings.log_level.lower(),
        debug=settings.need_debug, reload=settings.need_reload)
