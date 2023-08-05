from __future__ import annotations, with_statement

import functools
from contextlib import contextmanager
from contextvars import ContextVar
from logging import getLogger

from coiled.utils import random_str

logger = getLogger(__name__)

# Sessions last the entire duration of the python process
COILED_SESSION_ID = "coiled-session-" + random_str()
logger.debug(f"Coiled Session  ID : {COILED_SESSION_ID}")

# Operations are transient and more granular
COILED_OP_CONTEXT = ContextVar[str]("coiled-operation-context")


@contextmanager
def operation_context(name: str):
    reset = None
    try:
        yield COILED_OP_CONTEXT.get()
    except LookupError:
        c_id = name + "-" + random_str()
        logger.debug(f"Coiled Operation Context ID : {c_id}")
        reset = COILED_OP_CONTEXT.set(c_id)
        yield c_id
    if reset:
        COILED_OP_CONTEXT.reset(reset)


def track_context(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        with operation_context(f"{func.__module__}.{func.__name__}"):
            return await func(*args, **kwargs)

    return wrapper
