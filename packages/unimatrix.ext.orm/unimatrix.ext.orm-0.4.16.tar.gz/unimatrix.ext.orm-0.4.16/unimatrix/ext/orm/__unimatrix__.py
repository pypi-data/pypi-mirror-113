"""Specifies entrypoint operations for Unimatrix integration."""
from . import ENGINES
from . import ASYNC_ENGINES


# Provides a hint to unimatrix.runtime.boot.shutdown()
# to indicate when this module should run.
WEIGHT = 1000


async def on_teardown(*args, **kwargs):
    ENGINES.destroy()
    await ASYNC_ENGINES.destroy()
