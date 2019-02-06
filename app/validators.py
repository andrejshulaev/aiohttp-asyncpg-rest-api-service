# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module with config schema to validate it"""

import trafaret as tr

CONFIG_SCHEMA = tr.Dict({
    tr.Key('postgres'):
        tr.Dict({
            'database': tr.String(),
            'user': tr.String(),
            'password': tr.String(),
            'host': tr.String(),
            'port': tr.Int(),
            'poolsize_min': tr.Int(),
            'poolsize_max': tr.Int(),
        }),
    tr.Key('urls'):
        tr.Dict({
            'meta_url': tr.String(),
            'meta_woeid_url': tr.String(),
        }),
    tr.Key('date_const'):
        tr.Dict({
            'str_date_meta': tr.String(),
            'str_date_db': tr.String
        })
})
