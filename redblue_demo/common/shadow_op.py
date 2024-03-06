from bank_storage import BankStorage
from common import COLOR
from vector_clock import VectorClock
from account import Account


class ShadowOp:
    def __init__(
            self,
            aid: int,
            server_id: int,
            depend: VectorClock,
            amount: float = 0,
            color: COLOR = COLOR.BLUE,
    ) -> None:
        self.aid = aid
        self.server_id = server_id
        self.depend = depend
        self.amount = amount
        self.color = color

    def apply(self, bank: BankStorage) -> None:
        account = bank.get_account(self.aid)
        account.set_balance(account.get_balance() + self.amount)
