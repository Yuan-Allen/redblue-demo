"""
This module contains the definition of the Account class, which represents a bank account.
"""

from redblue_demo.common.common import INTEREST_RATE


class Account:
    """
    Represents a bank account.

    Attributes:
        aid (int): The account ID.
        balance (float): The current account balance.
    """

    def __init__(self, aid: int, balance: float) -> None:
        """
        Initialize an Account object.

        Args:
            aid (int): The account ID.
            balance (float): The initial account balance.
        """
        self.aid = aid
        self.balance = balance

    def get_balance(self) -> float:
        """
        Get the current account balance.

        Returns:
            float: The current account balance.
        """
        return self.balance

    def set_balance(self, balance: float) -> None:
        """
        Set the account balance.

        Args:
            balance (float): The new account balance.
        """
        self.balance = balance

    def compute_interest(self) -> float:
        """
        Compute the interest earned on the account balance.

        Returns:
            float: The interest earned on the account balance.
        """
        return self.balance * INTEREST_RATE
