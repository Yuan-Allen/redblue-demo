from redblue_demo.common.shadow_op import ShadowOp
import xmlrpc.client
import asyncio
from redblue_demo.common.common import SERVER_DELAY


class Client:
    """
    Wrapper for xmlrpc client.
    """

    def __init__(self, addr: str) -> None:
        self.server = xmlrpc.client.ServerProxy(addr)

    async def add_shadow_op_async(self, shadow_op: ShadowOp) -> None:
        await asyncio.sleep(SERVER_DELAY * 0.001)
        self.server.add_shadow_op(shadow_op)
