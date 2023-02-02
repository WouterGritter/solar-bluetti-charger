from abc import ABC, abstractmethod


class BluettiDevice(ABC):
    @abstractmethod
    def is_charging(self) -> bool:
        pass

    @abstractmethod
    def start_charging(self) -> None:
        pass

    @abstractmethod
    def stop_charging(self) -> None:
        pass

    @abstractmethod
    def get_power_draw(self) -> float:
        pass

    @abstractmethod
    def get_charge_percentage(self) -> float:
        pass

    @abstractmethod
    def get_charging_power(self) -> float:
        pass

    @abstractmethod
    def get_ac_output_power(self) -> float:
        pass

    @abstractmethod
    def get_dc_output_power(self) -> float:
        pass

