from redblue_demo.common.account import Account

NUM_ACCOUNTS = 10000
INITIAL_BALANCE = 1000.0


class BankStorage:
    def __init__(self) -> None:
        self.accounts = []
        for i in range(NUM_ACCOUNTS):
            self.accounts.append(Account(i, INITIAL_BALANCE))

    def get_account(self, aid: int) -> Account:
        return self.accounts[aid]