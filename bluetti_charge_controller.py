import time

from bluetti_device.bluetti_device import BluettiDevice
from smart_meter.smart_meter import SmartMeter


class BluettiChargeController:
    def __init__(self, bluetti_device: BluettiDevice, smart_meter: SmartMeter):
        self.bluetti_device = bluetti_device
        self.smart_meter = smart_meter

        self.charging_since = 0
        self.too_much_power_draw_since = 0

        self.min_charge_time = 120  # If the device starts charging, the device will charge for at least this amount of seconds
        self.start_charging_threshold = -410  # If the total power draw is less than this amount of watts, the device will start charging
        self.stop_charging_threshold = 25  # If the total power draw is more than this amount of watts, the device will stop charging
        self.stop_charging_delay = 60  # If the total power draw is more than the threshold, it will stop charging if it is still above the threshold after this amount of seconds
        self.emergency_charge_start = 20.0  # Start force-charging the bluetti device if the charge level drops below this percentage
        self.emergency_charge_stop = 30.0  # Stop force-charging the bluetti device if the charge level raises above this percentage

    def update(self):
        if self.bluetti_device.is_charging():
            should_stop = self.check_if_should_stop_charging()
            if should_stop:
                self.stop_charging()
        else:
            should_start = self.check_if_should_start_charging()
            if should_start:
                self.start_charging()

    def start_charging(self):
        self.charging_since = time.time()
        self.too_much_power_draw_since = None
        self.bluetti_device.start_charging()

    def stop_charging(self):
        self.bluetti_device.stop_charging()

    def check_if_should_start_charging(self):
        charge_percentage = self.bluetti_device.get_charge_percentage()
        if charge_percentage < self.emergency_charge_start:
            print(f'[C] Starting charge! Battery percentage is below the emergency threshold: {charge_percentage=}')
            return True

        total_power_draw = self.smart_meter.get_total_power_usage()

        if total_power_draw < self.start_charging_threshold:
            print(f'[C] Starting charge! Total power draw is below the threshold. {total_power_draw=}')
            return True

        return False

    def check_if_should_stop_charging(self):
        if time.time() - self.charging_since < self.min_charge_time:
            return False

        charge_percentage = self.bluetti_device.get_charge_percentage()
        if charge_percentage < self.emergency_charge_stop:
            return False

        total_power_draw = self.smart_meter.get_total_power_usage()

        if total_power_draw > self.stop_charging_threshold:
            if self.too_much_power_draw_since is None:
                self.too_much_power_draw_since = time.time()

            if time.time() - self.too_much_power_draw_since > self.stop_charging_delay:
                # Drew too much power for too many seconds. Stop charging.
                print(
                    f'[D] Stopping charge! Total power draw was above the threshold for too long. {total_power_draw=}')
                return True
        else:
            self.too_much_power_draw_since = None

        return False
