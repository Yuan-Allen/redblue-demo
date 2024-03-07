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

    @classmethod
    def from_dict(cls, data: dict) -> "ShadowOp":
        shadow_op = cls(
            data["aid"],
            data["server_id"],
            VectorClock(len(data["depend"]["B"])),
            data["amount"],
        )
        shadow_op.depend.B = data["depend"]["B"]
        shadow_op.depend.R = data["depend"]["R"]
        shadow_op.color = COLOR.BLUE if data["color"] == 0 else COLOR.RED
        return shadow_op
