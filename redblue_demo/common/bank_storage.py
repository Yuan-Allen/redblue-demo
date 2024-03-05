from redblue_demo.common.account import Account


NUM_ACCOUNTS = 10000


class BankStorage:
    def __init__(self) -> None:
        raise NotImplementedError("TODO: Implement this functionality")

    def get_account(self, aid: int) -> Account:
        raise NotImplementedError("TODO: Implement this functionality")
