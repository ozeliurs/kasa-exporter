from ipaddress import ip_address
from os import environ

from kasa import Discover, Credentials

username = (environ.get('KASA_USERNAME') or "test")
password = (environ.get('KASA_PASSWORD') or "test")

credentials = Credentials(username, password)


class Plug:
    def __init__(self, target):
        if not ip_address(target):
            raise ValueError("Invalid IP address")

        self.target = target
        self._plug = None

    async def connect(self):
        self._plug = await Discover.discover_single(
            self.target,
            credentials=credentials,
            discovery_timeout=5
        )

        await self._plug.update()

        print(self._plug.features)

    async def scrape(self):
        await self.connect()

        return {
            "sys_info": self._plug.sys_info,
            "model": self._plug.model,
            "alias": self._plug.alias,
            "time": self._plug.time,
            "timezone": self._plug.timezone,
            "hw_info": self._plug.hw_info,
            "location": self._plug.location,
            "rssi": self._plug.rssi,
            "mac": self._plug.mac,
            "device_id": self._plug.device_id,
            "internal_state": self._plug.internal_state,
            "state_information": self._plug.state_information,
            "has_emeter": self._plug.has_emeter,
            "is_on": self._plug.is_on,
            "emeter_realtime": self._plug.emeter_realtime,
            "emeter_this_month": self._plug.emeter_this_month,
            "emeter_today": self._plug.emeter_today
        }
