from abc import ABC, abstractmethod
from typing import Callable


class SmartMeter(ABC):
    def __init__(self):
        self.modifiers: list[Callable[[], float]] = []

    @abstractmethod
    def _get_real_power_usage(self) -> float:
        pass

    def get_total_power_usage(self) -> float:
        power = self._get_real_power_usage()
        for modifier_getter in self.modifiers:
            power += modifier_getter()

        return power
