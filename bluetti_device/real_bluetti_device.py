import asyncio

from PyP100.PyP110 import P110
from bluetti_mqtt.bluetooth import BluetoothClient as BluetoothBluettiClient, check_addresses
from bluetti_mqtt.core import BluettiDevice as BluetoothBluettiDevice

from bluetti_device.bluetti_device import BluettiDevice


class RealBluettiDevice(BluettiDevice):
    def __init__(self, tapo_plug: P110, bluetooth_device: BluetoothBluettiDevice,
                 bluetooth_client: BluetoothBluettiClient):
        self.tapo_plug = tapo_plug
        self.bluetooth_device = bluetooth_device
        self.bluetooth_client = bluetooth_client

    def is_charging(self) -> bool:
        tapo_info = self.tapo_plug.getDeviceInfo()
        return tapo_info['result']['device_on']

    def start_charging(self) -> None:
        self.tapo_plug.turnOn()

    def stop_charging(self) -> None:
        self.tapo_plug.turnOff()

    def get_power_draw(self) -> float:
        tapo_usage = self.tapo_plug.getEnergyUsage()
        return tapo_usage['result']['current_power'] / 1000

    def get_charge_percentage(self) -> float:
        return self._get_bluetooth_value('total_battery_percent')

    def get_charging_power(self) -> float:
        return self._get_bluetooth_value('ac_input_power')

    def get_ac_output_power(self) -> float:
        return self._get_bluetooth_value('ac_output_power')

    def get_dc_output_power(self) -> float:
        return self._get_bluetooth_value('dc_output_power')

    def _get_bluetooth_value(self, key_name):
        async def worker():
            for command in self.bluetooth_device.logging_commands:
                response = await (await self.bluetooth_client.perform(command))

                parsed = self.bluetooth_device.parse(command.page, command.offset, response.body)
                if key_name in parsed:
                    return parsed[key_name]

        return asyncio.get_event_loop().run_until_complete(worker())


def build_real_bluetti_device(tapo_plug_ip, tapo_plug_email, tapo_plug_password, bluetti_bluetooth_mac):
    async def worker():
        tapo_plug = P110(tapo_plug_ip, tapo_plug_email, tapo_plug_password)

        print('Performing tapo-plug handshake..')
        tapo_plug.handshake()
        tapo_plug.login()

        print('Searching for bluetooth device..')
        bluetooth_devices = await check_addresses({bluetti_bluetooth_mac})
        assert len(bluetooth_devices) == 1
        bluetooth_device = bluetooth_devices[0]

        bluetooth_client = BluetoothBluettiClient(bluetooth_device.address)
        asyncio.get_running_loop().create_task(bluetooth_client.run())

        print('Waiting for bluetooth connection..')
        while not bluetooth_client.is_connected:
            await asyncio.sleep(1)

        return RealBluettiDevice(tapo_plug, bluetooth_device, bluetooth_client)

    return asyncio.get_event_loop().run_until_complete(worker())
