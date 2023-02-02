from bluetti_device.bluetti_device import BluettiDevice
from smart_meter.smart_meter import SmartMeter


class SimulatedBluettiDevice(BluettiDevice):
    def __init__(self, smart_meter: SmartMeter):
        self._is_charging = False

        self._charging_power_draw = 410  # Simulated power draw
        self._charging_efficiency = 0.90  # Simulated charging power conversion efficiency
        self._static_charge_percentage = 75.0  # Simulated static charge percentage

        # Register self.get_power_draw as smart meter modifier, because this is a simulation
        smart_meter.modifiers.append(self.get_power_draw)

    def is_charging(self) -> bool:
        return self._is_charging

    def start_charging(self) -> None:
        if self.is_charging():
            raise Exception('Already charging.')

        self._is_charging = True

    def stop_charging(self) -> None:
        if not self.is_charging():
            raise Exception('Not charging.')

        self._is_charging = False

    def get_power_draw(self) -> float:
        return self._charging_power_draw if self._is_charging else 0

    def get_charge_percentage(self) -> float:
        return self._static_charge_percentage

    def get_charging_power(self) -> float:
        return self.get_power_draw() * self._charging_efficiency

    def get_ac_output_power(self) -> float:
        return 0.0

    def get_dc_output_power(self) -> float:
        return 0.0
