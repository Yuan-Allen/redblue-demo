class Account:
    def __init__(self, aid: int, balance: float) -> None:
        self.aid = aid
        self.balance = balance

    def get_balance(self) -> float:
        return self.balance

    def compute_interest(self) -> float:
        raise NotImplementedError("TODO: Implement this functionality")
