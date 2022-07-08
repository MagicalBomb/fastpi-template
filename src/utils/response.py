from fastapi import HTTPException


def json_ok():
    return HTTPException(status_code=200)
