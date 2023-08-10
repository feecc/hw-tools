import random


class VirtualScales:
    def __init__(self) -> None:
        self.current_weight: float = 0.0

    def check_weight(self):
        self.current_weight = round(random.uniform(0, 999.999), 3)
        return self.current_weight

    def get_current_weight(self):
        return self.current_weight


virtualscales = VirtualScales()
