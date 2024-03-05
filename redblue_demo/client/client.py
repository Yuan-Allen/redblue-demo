from redblue_demo.common.shadow_op import ShadowOp


class Client:
    """
    Wrapper for xmlrpc client.
    """

    def __init__(self, addr: str) -> None:
        raise NotImplementedError("TODO: Implement this functionality")

    def add_shadow_op_async(self, shadow_op: ShadowOp) -> None:
        raise NotImplementedError("TODO: Implement this functionality")
