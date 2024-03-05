from redblue_demo.common.bank_storage import BankStorage
from redblue_demo.common.common import COLOR
from redblue_demo.common.vector_clock import VectorClock


class ShadowOp:
    def __init__(
        self,
        aid: int,
        server_id: int,
        depend: VectorClock,
        amount: float = 0,
        color: COLOR = COLOR.BLUE,
    ) -> None:
        raise NotImplementedError("TODO: Implement this functionality")

    def apply(self, bank: BankStorage) -> None:
        raise NotImplementedError("TODO: Implement this functionality")
