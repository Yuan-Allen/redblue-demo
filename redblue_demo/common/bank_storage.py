"""
This module provides a class representing the storage for bank accounts.
"""

from redblue_demo.common.account import Account

NUM_ACCOUNTS = 10000
INIT_BALANCE = 1000.0


class BankStorage:
    """
    A class representing the storage for bank accounts.

    Attributes:
        accounts (list): A list of Account objects representing the bank accounts.
    """

    accounts: list

    def __init__(self) -> None:
        self.accounts = []
        for i in range(NUM_ACCOUNTS):
            self.accounts.append(Account(i, INIT_BALANCE))

    def get_account(self, aid: int) -> Account:
        """
        Returns the Account object with the specified account ID.

        Args:
            aid (int): The account ID.

        Returns:
            Account: The Account object with the specified account ID.
        """
        return self.accounts[aid]
