"""
This module contains common classes and constants used in the redblue-demo project.

Classes:
- Request: Represents a request made by a user.
- Response: Represents a response returned by the system.

Constants:
- INTEREST_RATE: The interest rate used for calculations.
- SERVER_DELAY: The delay time for server responses.

Enums:
- COLOR: Represents colors.
- REQ: Represents request types.
"""

from enum import Enum, auto
from typing import Optional

INTEREST_RATE: float = 0.04
SERVER_DELAY: float = 0.2


class COLOR:
    """
    Represents the available colors.

    Attributes:
        BLUE (int): The value representing the color blue.
        RED (int): The value representing the color red.
    """

    BLUE = 0
    RED = 1


class REQ(Enum):
    """
    Represents the request class.
    """

    DEPOSIT = auto()
    WITHDRAW = auto()
    INTEREST = auto()
    CHECK = auto()


class Request:
    """
    Represents a request made by a user.

    Attributes:
    - aid: The account ID associated with the request.
    - op: The type of operation requested.
    - amount: The amount involved in the request.
    """

    def __init__(self, aid: int, op: REQ, amount: float = 0.0) -> None:
        self.aid: int = aid
        self.op: REQ = op
        self.amount: float = amount


class Response:
    """
    Represents a response returned by the system.

    Attributes:
    - status: The status code of the response.
    - balance: The account balance associated with the response.
    - message: An optional message accompanying the response.
    """

    def __init__(
        self, status: int, balance: float = 0, message: Optional[str] = ""
    ) -> None:
        self.status: int = status
        self.balance: float = balance
        self.message: str = message

    def print(self) -> None:
        """
        Prints the response details.
        """
        print(f"status {self.status}, balance {self.balance:.2f}", end="")
        if self.message:
            print(f", message: {self.message}", end="")
        print()
