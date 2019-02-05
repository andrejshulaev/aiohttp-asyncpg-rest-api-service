import requests

URL_TO_GET_WOEID = 'https://www.metaweather.com/api/location/search/?query='
URL = 'https://www.metaweather.com/api/location/'

class MetaWeather:

    def __init__(self, city):
        self.woeid = self._get_woeid(city)
        self.forecast_link = URL + str(self.woeid) + '/'

    def _get_woeid(self, city: str) -> str:
        """method to get woeid to city"""
        return requests.get(URL_TO_GET_WOEID+city).json()[0]['woeid']

    async def get_forecast_to_date(self, session, date: str) -> dict:
        """method to get weather forecast to specific date"""
        async with session.get(self.forecast_link+date, allow_redirects=True) as response:
            data = await response.json()
            data = data[0]
            data.pop('id')
            return data
