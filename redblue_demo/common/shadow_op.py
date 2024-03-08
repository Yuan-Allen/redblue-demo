"""
This module contains the ShadowOp class, 
which represents a shadow operation that can be applied to a bank storage.
"""

from redblue_demo.common.bank_storage import BankStorage
from redblue_demo.common.common import COLOR
from redblue_demo.common.vector_clock import VectorClock


class ShadowOp:
    """
    Represents a shadow operation that can be applied to a bank storage.

    Attributes:
        aid (int): The account ID.
        server_id (int): The server ID.
        depend (VectorClock): The vector clock representing the
            dependencies of the shadow operation.
        amount (float): The amount to be applied to the account balance.
        color (COLOR): The color of the shadow operation.
    """

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
        """
        Applies the shadow operation to the given bank storage.

        Args:
            bank (BankStorage): The bank storage to apply the shadow operation to.

        Returns:
            None

        """
        account = bank.get_account(self.aid)
        account.balance = account.get_balance() + self.amount

    @classmethod
    def from_dict(cls, data: dict) -> "ShadowOp":
        """
        Creates a ShadowOp instance from a dictionary representation.

        Args:
            data (dict): The dictionary representation of the ShadowOp.

        Returns:
            ShadowOp: The created ShadowOp instance.

        """
        shadow_op = cls(
            data["aid"],
            data["server_id"],
            VectorClock(len(data["depend"]["b"])),
            data["amount"],
        )
        shadow_op.depend.b = data["depend"]["b"]
        shadow_op.depend.r = data["depend"]["r"]
        shadow_op.color = COLOR.BLUE if data["color"] == 0 else COLOR.RED
        return shadow_op
