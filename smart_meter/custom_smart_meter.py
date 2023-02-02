import requests

from smart_meter.smart_meter import SmartMeter


class CustomSmartMeter(SmartMeter):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint

    def _get_real_power_usage(self):
        res = requests.request('GET', self.endpoint).json()

        return res['power']
