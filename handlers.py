from contextlib import contextmanager

from fastapi import HTTPException


@contextmanager
def handle_not_found():
    try:
        yield
    except ValueError as e:
        raise HTTPException(status_code=404, detail=e.args) from e
