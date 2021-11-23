import os
import json
import requests
from transport_service.logging import mainLogger
from uuid import uuid4

class Valhalla:
    """Valhalla Wrapper class.

    Attributes:
        url (str): Valhalla url (default: environment variable `VALHALLA_URL`)
    """

    def __init__(self, url: str=None):
        self.url = url if url is not None else os.environ['VALHALLA_URL']


    def _createCountours(self, countourType: str, range_: list, color: list=[]) -> list:
        if countourType not in ['distance', 'time']:
            raise ValueError('`countourType` should be one of "distance", "time".')
        contours = [{countourType: d, 'color': color[i] if i < len(color) else None} for i, d in enumerate(range_)]
        return contours


    def _request(self, method: str, endpoint: str, data: dict=None) -> tuple:
        assert method in ['GET', 'POST']
        uuid = str(uuid4())
        mainLogger.info('Requesting Valhalla [id="%s", method="%s", endpoint="%s"]', uuid, method, endpoint)
        url = "{url}/{endpoint}".format(url=self.url, endpoint=endpoint)
        if method == 'GET':
            if data is not None:
                request_json = json.dumps(data)
                url = "{url}/{endpoint}?json={data}".format(url=self.url, endpoint=endpoint, data=request_json)
            r = requests.get(url)
        else:
            r = requests.post(url, json=data)
        mainLogger.info('Valhalla responded [id="%s", statusCode=%i]', uuid, r.status_code)

        return r.json(), r.status_code


    def _isoline(self, countourType: str, lat: float, lon: float, range_: list, costing: str="auto", **kwargs) -> tuple:
        color = kwargs.pop('color', [])
        contours = self._createCountours(countourType, range_, color)
        locations = [{"lat": lat, "lon": lon}]
        data = {"locations": locations, "costing": costing, "contours": contours, **kwargs}

        return self._request('GET', 'isochrone', data=data)


    def isochrone(self, lat: float, lon: float, range_: list, costing: str="auto", **kwargs) -> tuple:
        return self._isoline('time', lat, lon, range_=range_, costing=costing, **kwargs)


    def isodistance(self, lat: float, lon: float, range_: list, costing: str="auto", **kwargs) -> tuple:
        return self._isoline('distance', lat, lon, range_=range_, costing=costing, **kwargs)


    def traceRoute(self, shape: list, costing: str="auto", **kwargs) -> tuple:
        data = {"shape": shape, "costing": costing, **kwargs}
        return self._request('POST', 'trace_route', data=data)


    def traceAttributes(self, shape: list, costing: str="auto", **kwargs) -> tuple:
        data = {"shape": shape, "costing": costing, **kwargs}
        return self._request('POST', 'trace_attributes', data=data)


    def routing(self, costing: str, locations: list, directions_options: dict={}, costing_options: dict={}) -> tuple:
        data = {"costing": costing, "locations": locations, **directions_options, "costing_options": {costing: costing_options}}
        return self._request('POST', 'route', data=data)
