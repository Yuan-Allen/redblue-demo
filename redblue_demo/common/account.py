from redblue_demo.common.common import INTEREST_RATE
class Account:
    def __init__(self, aid: int, balance: float) -> None:
        self.aid = aid
        self.balance = balance

    def get_balance(self) -> float:
        return self.balance

    def set_balance(self, balance) -> None:
        self.balance = balance

    def compute_interest(self) -> float:
        return self.balance * INTEREST_RATE
