"""Various utility functions to avoid boilerplate when performing common operations."""
import pathlib
import sys
from contextlib import contextmanager
from typing import Generator, Union


@contextmanager
def syspath_prepend(path: Union[pathlib.Path, str]) -> Generator:
    """Temporarily prepend `path` to `sys.path` for the duration of the `with` block."""
    # NOTE. It is not thread-safe to use as is now.
    # In the future it might require an `RLock` to avoid concurrent access to `sys.path`.
    current = sys.path[:]
    # Use `insert` to put the value to the 0th position in `sys.path`. The given path will be the first one to check.
    sys.path.insert(0, str(path))
    try:
        yield
    finally:
        sys.path[:] = current
