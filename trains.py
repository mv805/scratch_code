from typing import Optional
from abc import ABC


class Train:

    def __init__(self) -> None:
        pass


class RollingStock(ABC):
    """
    A class representing a rolling stock in a train. Engines, and Wagons and everything else.
    """

    def __init__(self, stock_base_weight: int) -> None:
        self.stock_base_weight = stock_base_weight
        self.previous: Optional["RollingStock"] = None
        self.next: Optional["RollingStock"] = None

    def set_previous(self, rolling_stock: "RollingStock") -> None:
        self.previous = rolling_stock

    def set_next(self, rolling_stock: "RollingStock") -> None:
        self.next = rolling_stock

    @property
    def weight(self) -> int:
        return self.stock_base_weight


class CargoWagon(RollingStock, ABC):

    def __init__(
        self,
        cargo_weight: int = 10,
        cargo_type: str = "FREIGHT",
        cargo_qty: int = -1,
    ) -> None:
        super().__init__(stock_base_weight=30)
        self.MAX_CAPACITY = 100  # tons
        self.cargo_type = cargo_type
        self.cargo_weight = cargo_weight  # tons per unit
        self.cargo_qty = (
            self.MAX_CAPACITY // cargo_weight
            if cargo_qty == -1
            else (
                cargo_qty
                if cargo_qty * cargo_weight < self.MAX_CAPACITY
                else self.MAX_CAPACITY // cargo_weight
            )
        )

    @property
    def weight(self) -> int:
        return super().weight + self.cargo_qty * self.cargo_weight


# class PassengerCar(RollingStock):
#     def __init__(
#         self, total_passengers: int = 0, max_capacity: int = 50
#     ) -> None:
#         super().__init__()
#         self.cargo_type = cargo_type
#         self.cargo_qty = cargo_qty  # in tons


class Engine(RollingStock):
    def __init__(self) -> None:
        super().__init__(stock_base_weight=180)

    def set_previous(self, rolling_stock: "RollingStock") -> None:
        raise Exception(
            "Engine cannot have a previous rolling stock as it is always the Lead Vehicle"
        )
