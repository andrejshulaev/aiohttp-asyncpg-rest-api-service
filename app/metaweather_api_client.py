# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to interact with original metaweather API"""

import requests

class MetaWeather:
    """Metaweather api client"""

    def __init__(self, city, config=None):
        self.urls = config['urls']
        self.woeid = self._get_woeid(city)
        self.forecast_link = self.urls['meta_url'] + str(self.woeid) + '/'

    def _get_woeid(self, city: str) -> str:
        """method to get woeid to city"""
        return requests.get(self.urls['meta_woeid_url']+city).json()[0]['woeid']

    async def get_forecast_to_date(self, session, date: str) -> dict:
        """method to get weather forecast to specific date"""
        async with session.get(self.forecast_link+date, allow_redirects=True) as response:
            data = await response.json()
            data = data[0]
            data.pop('id')
            return data
