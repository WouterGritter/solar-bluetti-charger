import os
import time

from dotenv import load_dotenv

from bluetti_charge_controller import BluettiChargeController
from bluetti_device.bluetti_device import BluettiDevice
from bluetti_device.real_bluetti_device import build_real_bluetti_device
from file_power_offset import FilePowerOffset
from smart_meter.custom_smart_meter import CustomSmartMeter

load_dotenv()

UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL'))
INFO_INTERVAL = int(os.getenv('INFO_INTERVAL'))


def print_info(bluetti_device: BluettiDevice, smart_meter):
    house_power_draw = smart_meter.get_total_power_usage()
    is_charging = bluetti_device.is_charging()
    charge_percentage = bluetti_device.get_charge_percentage()
    wall_power_draw = bluetti_device.get_power_draw()
    charging_power_input = bluetti_device.get_charging_power()
    ac_output_power = bluetti_device.get_ac_output_power()
    dc_output_power = bluetti_device.get_dc_output_power()

    print(f'[I] {house_power_draw=} {is_charging=} {charge_percentage=} {wall_power_draw=} '
          f'{charging_power_input=} {ac_output_power=} {dc_output_power=}')


def main():
    print('Hello, world!')

    smart_meter = CustomSmartMeter(os.getenv('SMART_METER_ENDPOINT'))

    # Inject a variable power offset for testing
    FilePowerOffset('power_offset.txt', smart_meter)

    # bluetti_device = SimulatedBluettiDevice(smart_meter)
    bluetti_device = build_real_bluetti_device(
        tapo_plug_ip=os.getenv('TAPO_PLUG_IP'),
        tapo_plug_email=os.getenv('TAPO_PLUG_EMAIL'),
        tapo_plug_password=os.getenv('TAPO_PLUG_PASSWORD'),
        bluetti_bluetooth_mac=os.getenv('BLUETTI_BLUETOOTH_MAC'),
    )

    charge_controller = BluettiChargeController(bluetti_device, smart_meter)

    info_countdown = 0

    while True:
        update_start = time.time()
        charge_controller.update()
        try:
            pass
        except Exception as e:
            print(f'[W] Warning! Caught an exception while trying to update: {e}')

        update_elapsed = time.time() - update_start
        if update_elapsed > 1:
            print(f'[W] Warning! Update took an abnormal amount of time: {update_elapsed} seconds')

        info_countdown -= 1
        if info_countdown <= 0:
            print_info(bluetti_device, smart_meter)
            info_countdown = round(INFO_INTERVAL / UPDATE_INTERVAL)

        time.sleep(UPDATE_INTERVAL)


if __name__ == '__main__':
    main()
