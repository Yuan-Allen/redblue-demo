from enum import Enum, auto
from typing import Optional

# Constants
INTEREST_RATE: float = 0.04
SERVER_DELAY: float = 0.2


class COLOR:
    BLUE = 0
    RED = 1


# Enumeration for request types
class REQ(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()
    INTEREST = auto()
    CHECK = auto()


# Request class definition
class Request:
    def __init__(self, aid: int, op: REQ, amount: float = 0.0) -> None:
        self.aid: int = aid
        self.op: REQ = op
        self.amount: float = amount


# Response class definition
class Response:
    def __init__(
        self, status: int, balance: float = 0, message: Optional[str] = ""
    ) -> None:
        self.status: int = status
        self.balance: float = balance
        self.message: str = message

    def print(self) -> None:
        print(f"status {self.status}, balance {self.balance:.2f}", end="")
        if self.message:
            print(f", message: {self.message}", end="")
        print()
