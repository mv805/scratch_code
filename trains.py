from typing import List, Optional
from abc import ABC


class RollingStock(ABC):
    """
    A class representing a rolling stock in a train. Engines, and Wagons and everything else.
    """

    def __init__(self, stock_base_weight, stock_id: str = "NOID") -> None:
        self.stock_base_weight = stock_base_weight
        self.previous: Optional["RollingStock"] = None
        self.next: Optional["RollingStock"] = None
        self.stock_id = stock_id

    def set_previous(self, rolling_stock: "RollingStock") -> None:
        self.previous = rolling_stock

    def set_next(self, rolling_stock: "RollingStock") -> None:
        self.next = rolling_stock

    @property
    def weight(self) -> int:
        return self.stock_base_weight

    @property
    def id(self) -> str:
        return self.stock_id


class CargoWagon(RollingStock, ABC):

    def __init__(
        self,
        stock_id: str,
        cargo_weight: int = 10,
        cargo_type: str = "FREIGHT",
        cargo_qty: int = -1,
    ) -> None:
        super().__init__(stock_base_weight=30, stock_id=stock_id)
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

    def __str__(self) -> str:
        return f"[CARGO:{self.cargo_type}-Q{self.cargo_qty}-CW{self.cargo_weight * self.cargo_qty}-TW{self.weight}/{self.MAX_CAPACITY}:{self.stock_id}]"


class Engine(RollingStock):
    def __init__(self, stock_id: str) -> None:
        super().__init__(stock_base_weight=180, stock_id=stock_id)

    def __str__(self) -> str:
        return f"[ENG:{self.stock_id}]"


class Train:

    def __init__(self, initial_train: List[RollingStock]) -> None:
        self.lead_car = None
        self.last_car = None

        if initial_train:
            for car in initial_train:
                if not self.lead_car:
                    self.lead_car = car
                    self.last_car = car
                else:
                    self.add_stock(car)

    def add_stock(self, rolling_stock: RollingStock) -> None:
        if not self.lead_car:
            self.lead_car = rolling_stock
            self.last_car = rolling_stock
        else:
            current_car = self.lead_car
            while current_car.next:
                current_car = current_car.next

            current_car.next = rolling_stock
            self.last_car = rolling_stock

    def __str__(self) -> str:
        current_car = self.lead_car
        train_str = []
        while current_car:
            train_str.append(str(current_car))
            current_car = current_car.next
        return "->\n".join(train_str)


if __name__ == "__main__":
    train = Train(
        [
            Engine("NXE-334"),
            CargoWagon(
                stock_id="UYO-892",
                cargo_weight=5,
                cargo_type="LIVESTOCK",
                cargo_qty=6,
            ),
            CargoWagon(
                stock_id="FDX-453",
                cargo_weight=5,
                cargo_type="LIVESTOCK",
                cargo_qty=20,
            ),
            CargoWagon(
                stock_id="LLK-432",
                cargo_weight=10,
                cargo_type="STEEL",
                cargo_qty=10,
            ),
            CargoWagon(
                stock_id="RTY-099", cargo_weight=3, cargo_type="LUMBER"
            ),
        ]
    )
    print(train)
