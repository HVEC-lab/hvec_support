This package contains several functions to turbo boost the use of Python in combination with Excel and sqlite.

Installation
------------

Install from GitHub::

    pip install git+https://github.com/HVEC-lab/hvec_support

Or, from a clone of the repository::

    uv sync

Tests
-----

Run the offline tests::

    uv run pytest

Run the tests that use live web services::

    uv run pytest -m network
