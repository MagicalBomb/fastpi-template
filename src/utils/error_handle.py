import logging
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


def init_error_handle(app: FastAPI):

    @app.exception_handler(Exception)
    async def handle_all_errors(request: Request, exc: Exception):
        request_msg = dict(
            method=request.method,
            scheme=request.scope.get('scheme', ''),
            path=request.scope.get('path', ''),
            user=request.scope.get('user', ''),
            query_string=request.scope.get('query_string', ''),
        )
        logging.error(f"{request_msg}\n{traceback.format_exc()}")
        return JSONResponse(status_code=500, content="System Error")
