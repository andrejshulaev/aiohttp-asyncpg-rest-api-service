# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to run server with routes""" # pragma: no cover
from aiohttp.web import run_app # pragma: no cover

from app.server import main # pragma: no cover

run_app(main()) # pragma: no cover
