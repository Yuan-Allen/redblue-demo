from redblue_demo.common.bank_storage import BankStorage


class ShadowOP:
    def __init__(self) -> None:
        raise NotImplementedError("TODO: Implement this functionality")

    def apply(self, bank: BankStorage) -> None:
        raise NotImplementedError("TODO: Implement this functionality")
