from redblue_demo.common.bank_storage import BankStorage
from redblue_demo.common.common import COLOR
from redblue_demo.common.vector_clock import VectorClock
from redblue_demo.common.account import Account


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
        account.balance = account.get_balance() + self.amount